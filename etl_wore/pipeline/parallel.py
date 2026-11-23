"""
Concurrent batch loader support using ThreadPoolExecutor.
"""
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from threading import Lock
from typing import List, Dict, Any
from ..loaders.base import BaseLoader

class ParallelBatchLoader(BaseLoader):
    def __init__(self, base_loader: BaseLoader, max_workers: int = 4):
        super().__init__(name=f"Parallel({base_loader.name})")
        if isinstance(max_workers, bool) or not isinstance(max_workers, int) or max_workers < 1:
            raise ValueError("max_workers must be a positive integer")
        self.base_loader = base_loader
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.futures = deque()
        self._pending_limit = max_workers * 2
        self._worker_error = None
        self._lock = Lock()
        self._closed = False

    def load(self, records: List[Dict[str, Any]]):
        with self._lock:
            if self._closed:
                raise RuntimeError("Parallel loader is closed")
            if not records:
                return
            if len(self.futures) >= self._pending_limit:
                self._collect(self.futures.popleft())
            future = self.executor.submit(self.base_loader.load, deepcopy(records))
            self.futures.append(future)

    def _collect(self, future):
        try:
            future.result()
        except Exception as exc:
            if self._worker_error is None:
                self._worker_error = exc

    def close(self):
        with self._lock:
            if self._closed:
                return
            self._closed = True
        try:
            for future in self.futures:
                self._collect(future)
        finally:
            self.executor.shutdown(wait=True)
            self.futures.clear()
            try:
                self.base_loader.close()
            except Exception:
                if self._worker_error is None:
                    raise
        if self._worker_error is not None:
            raise self._worker_error

