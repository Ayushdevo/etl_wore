"""
Pipeline execution context and metrics tracker.
"""
import time
from typing import Dict, Any

class PipelineContext:
    def __init__(self, pipeline_name: str = "default_pipeline"):
        self.pipeline_name = pipeline_name
        self.start_time = time.time()
        self.end_time = None
        self.records_extracted = 0
        self.records_transformed = 0
        self.records_loaded = 0
        self.records_dropped = 0
        self.metadata: Dict[str, Any] = {}

    def finish(self):
        self.end_time = time.time()

    @property
    def duration_seconds(self) -> float:
        end = self.end_time or time.time()
        return round(end - self.start_time, 3)

    def summary(self) -> Dict[str, Any]:
        return {
            "pipeline": self.pipeline_name,
            "duration_sec": self.duration_seconds,
            "extracted": self.records_extracted,
            "transformed": self.records_transformed,
            "loaded": self.records_loaded,
            "dropped": self.records_dropped
        }
