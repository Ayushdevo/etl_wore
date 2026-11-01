"""
Core Pipeline execution engine.
"""

import sys
from copy import deepcopy
from typing import List

from ..exceptions import ExtractionError, TransformationError
from ..extractors.base import BaseExtractor
from ..loaders.base import BaseLoader
from ..logger import setup_logger
from ..transformers.base import BaseTransformer
from .context import PipelineContext

logger = setup_logger("etl_wore.pipeline.engine")


class Pipeline:
    def __init__(self, name: str, batch_size: int = 500):
        if isinstance(batch_size, bool) or not isinstance(batch_size, int) or batch_size < 1:
            raise ValueError("batch_size must be a positive integer")
        self.name = name
        self.batch_size = batch_size
        self.extractors: List[BaseExtractor] = []
        self.transformers: List[BaseTransformer] = []
        self.loaders: List[BaseLoader] = []

    def add_extractor(self, extractor: BaseExtractor) -> "Pipeline":
        self.extractors.append(extractor)
        return self

    def add_transformer(self, transformer: BaseTransformer) -> "Pipeline":
        self.transformers.append(transformer)
        return self

    def add_loader(self, loader: BaseLoader) -> "Pipeline":
        self.loaders.append(loader)
        return self

    def run(self) -> PipelineContext:
        ctx = PipelineContext(self.name)
        logger.info(f"Starting pipeline '{self.name}'...")

        try:
            batch = []
            for extractor in self.extractors:
                iterator = iter(extractor.extract())
                try:
                    for record in iterator:
                        ctx.records_extracted += 1
                        if not isinstance(record, dict):
                            raise ExtractionError("Extractor records must be objects")
                        curr = deepcopy(record)
                        for transformer in self.transformers:
                            curr = transformer.transform(curr)
                            if curr is None:
                                ctx.records_dropped += 1
                                break
                            if not isinstance(curr, dict):
                                raise TransformationError("Transformers must return an object or None")
                        if curr is not None:
                            ctx.records_transformed += 1
                            batch.append(curr)

                        if len(batch) >= self.batch_size:
                            self._flush_batch(batch, ctx)
                            batch = []
                finally:
                    close = getattr(iterator, "close", None)
                    if close is not None:
                        processing_failed = sys.exc_info()[0] is not None
                        try:
                            close()
                        except Exception:
                            if not processing_failed:
                                raise

            if batch:
                self._flush_batch(batch, ctx)

        finally:
            # Attempt every close, preserve an active processing error, and finalize metrics.
            processing_failed = sys.exc_info()[0] is not None
            close_error = None
            for loader in self.loaders:
                try:
                    loader.close()
                except Exception as exc:
                    if close_error is None:
                        close_error = exc
            ctx.finish()
            if close_error is not None and not processing_failed:
                raise close_error

        logger.info(f"Pipeline '{self.name}' finished. Stats: {ctx.summary()}")
        return ctx

    def _flush_batch(self, batch: List, ctx: PipelineContext):
        for loader in self.loaders:
            loader.load(deepcopy(batch))
        ctx.records_loaded += len(batch)
