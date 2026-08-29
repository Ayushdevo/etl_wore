"""
REST API extractor with pagination support.
"""
from typing import Generator, Dict, Any, Optional
import requests
from .base import BaseExtractor
from ..exceptions import ExtractionError
from ..utils.retry import retry

class RestApiExtractor(BaseExtractor):
    def __init__(self, endpoint: str, headers: Optional[Dict[str, str]] = None, page_param: str = "page"):
        super().__init__(name=f"RestApiExtractor({endpoint})")
        self.endpoint = endpoint
        self.headers = headers or {}
        self.page_param = page_param

    @retry(max_attempts=3, initial_delay=1.0)
    def _fetch_page(self, page: int) -> Dict[str, Any]:
        params = {self.page_param: page}
        response = requests.get(self.endpoint, headers=self.headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    def extract(self) -> Generator[Dict[str, Any], None, None]:
        page = 1
        while True:
            try:
                data = self._fetch_page(page)
            except Exception as e:
                raise ExtractionError(f"Failed to fetch page {page} from {self.endpoint}: {e}") from e

            items = data if isinstance(data, list) else data.get("items", data.get("data", []))
            if not items:
                break

            for item in items:
                yield item

            page += 1
