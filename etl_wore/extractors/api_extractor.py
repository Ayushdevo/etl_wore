"""
REST API extractor with pagination support.
"""

import math
import sys
from urllib.parse import urlparse, urlsplit, urlunsplit, parse_qsl
from typing import Any, Dict, Generator, Optional

import requests

from ..exceptions import ExtractionError
from ..utils.retry import retry
from .base import BaseExtractor


class _TransientHttpError(requests.HTTPError):
    """A throttling or server response that may succeed when retried."""


class RestApiExtractor(BaseExtractor):
    def __init__(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        page_param: str = "page",
        max_pages: Optional[int] = None,
        timeout: float = 10,
    ):
        super().__init__(name=f"RestApiExtractor({endpoint})")
        try:
            parts = urlparse(endpoint) if isinstance(endpoint, str) else None
            valid_url = parts is not None and parts.scheme in {"http", "https"} and bool(parts.hostname)
            if valid_url:
                _ = parts.port
                valid_url = not any(char.isspace() or ord(char) < 32 or ord(char) == 127 or char == "\\" for char in endpoint)
        except ValueError:
            valid_url = False
        if not valid_url:
            raise ValueError("endpoint must be an HTTP(S) URL with a hostname")
        if not isinstance(page_param, str) or not page_param.strip():
            raise ValueError("page_param must be a nonempty string")
        if headers is not None and (not isinstance(headers, dict) or any(not isinstance(key, str) or not key.strip() or not isinstance(value, str) for key, value in headers.items())):
            raise ValueError("headers must map nonempty strings to strings")
        self.endpoint = endpoint
        self.headers = dict(headers) if headers is not None else {}
        self.page_param = page_param
        if max_pages is not None and (
            isinstance(max_pages, bool) or not isinstance(max_pages, int) or max_pages < 1
        ):
            raise ValueError("max_pages must be a positive integer or None")
        self.max_pages = max_pages
        if isinstance(timeout, bool) or not isinstance(timeout, (int, float)):
            raise ValueError("timeout must be a finite positive number")
        try:
            self.timeout = float(timeout)
        except OverflowError as exc:
            raise ValueError("timeout must be a finite positive number") from exc
        if not math.isfinite(self.timeout) or self.timeout <= 0:
            raise ValueError("timeout must be a finite positive number")

    @retry(max_attempts=3, initial_delay=1.0, exceptions=(requests.ConnectionError, requests.Timeout, _TransientHttpError))
    def _fetch_page(self, page: int) -> Dict[str, Any]:
        parts = urlsplit(self.endpoint)
        params = [(key, value) for key, value in parse_qsl(parts.query, keep_blank_values=True)
                  if key != self.page_param]
        params.append((self.page_param, page))
        endpoint = urlunsplit((parts.scheme, parts.netloc, parts.path, "", parts.fragment))
        response = requests.get(
            endpoint, headers=self.headers, params=params, timeout=self.timeout
        )
        try:
            try:
                response.raise_for_status()
            except requests.HTTPError as exc:
                if response.status_code == 429 or 500 <= response.status_code <= 599:
                    raise _TransientHttpError(str(exc), response=response) from exc
                raise
            return response.json()
        finally:
            processing_failed = sys.exc_info()[0] is not None
            try:
                response.close()
            except Exception:
                if not processing_failed:
                    raise

    def extract(self) -> Generator[Dict[str, Any], None, None]:
        page = 1
        while True:
            if self.max_pages is not None and page > self.max_pages:
                raise ExtractionError(
                    f"REST pagination exceeded max_pages={self.max_pages} without reaching an empty page"
                )
            try:
                data = self._fetch_page(page)
            except Exception as e:
                raise ExtractionError(
                    f"Failed to fetch page {page} from {self.endpoint}: {e}"
                ) from e

            if isinstance(data, list):
                items = data
            elif isinstance(data, dict) and ("items" in data or "data" in data):
                items = data["items"] if "items" in data else data["data"]
            else:
                raise ExtractionError(f"REST page {page} must be an array or an items/data envelope")
            if not isinstance(items, list) or any(not isinstance(item, dict) for item in items):
                raise ExtractionError(f"REST page {page} must contain an array of objects")
            if not items:
                break

            for item in items:
                yield item

            page += 1
