"""
Lifecycle hooks and callbacks for pipeline execution events.
"""
from typing import Callable, List, Dict, Any

class PipelineHooks:
    def __init__(self):
        self._on_start: List[Callable[[], None]] = []
        self._on_record: List[Callable[[Dict[str, Any]], None]] = []
        self._on_finish: List[Callable[[Dict[str, Any]], None]] = []

    def register_on_start(self, callback: Callable[[], None]):
        self._on_start.append(callback)

    def register_on_finish(self, callback: Callable[[Dict[str, Any]], None]):
        self._on_finish.append(callback)

    def trigger_start(self):
        for cb in self._on_start:
            cb()

    def trigger_finish(self, summary: Dict[str, Any]):
        for cb in self._on_finish:
            cb(summary)
