"""
Concurrent batch loader support using ThreadPoolExecutor.
"""
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any
from ..loaders.base import BaseLoader

class ParallelBatchLoader(BaseLoader):
    def __init__(self, base_loader: BaseLoader, max_workers: int = 4):
        super().__init__(name=f"Parallel({base_loader.name})")
        self.base_loader = base_loader
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.futures = []
        self._closed = False

    def load(self, records: List[Dict[str, Any]]):
        if self._closed:
            raise RuntimeError("Parallel loader is closed")
        if not records:
            return
        future = self.executor.submit(self.base_loader.load, list(records))
        self.futures.append(future)

    def close(self):
        if self._closed:
            return
        self._closed = True
        error = None
        try:
            for future in self.futures:
                try:
                    future.result()
                except Exception as exc:
                    if error is None:
                        error = exc
        finally:
            self.executor.shutdown(wait=True)
            self.futures.clear()
            try:
                self.base_loader.close()
            except Exception:
                if error is None:
                    raise
        if error is not None:
            raise error
