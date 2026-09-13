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

    def load(self, records: List[Dict[str, Any]]):
        if not records:
            return
        future = self.executor.submit(self.base_loader.load, list(records))
        self.futures.append(future)

    def close(self):
        for f in self.futures:
            f.result()
        self.executor.shutdown(wait=True)
        self.base_loader.close()
