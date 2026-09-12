"""
Core Pipeline execution engine.
"""
from typing import List
from ..extractors.base import BaseExtractor
from ..transformers.base import BaseTransformer
from ..loaders.base import BaseLoader
from .context import PipelineContext
from ..logger import setup_logger

logger = setup_logger("etl_wore.pipeline.engine")

class Pipeline:
    def __init__(self, name: str, batch_size: int = 500):
        self.name = name
        self.batch_size = batch_size
        self.extractors: List[BaseExtractor] = []
        self.transformers: List[BaseTransformer] = []
        self.loaders: List[BaseLoader] = []

    def add_extractor(self, extractor: BaseExtractor) -> 'Pipeline':
        self.extractors.append(extractor)
        return self

    def add_transformer(self, transformer: BaseTransformer) -> 'Pipeline':
        self.transformers.append(transformer)
        return self

    def add_loader(self, loader: BaseLoader) -> 'Pipeline':
        self.loaders.append(loader)
        return self

    def run(self) -> PipelineContext:
        ctx = PipelineContext(self.name)
        logger.info(f"Starting pipeline '{self.name}'...")

        batch = []
        for extractor in self.extractors:
            for record in extractor.extract():
                ctx.records_extracted += 1
                curr = record
                for transformer in self.transformers:
                    curr = transformer.transform(curr)
                    if curr is None:
                        ctx.records_dropped += 1
                        break
                if curr is not None:
                    ctx.records_transformed += 1
                    batch.append(curr)

                if len(batch) >= self.batch_size:
                    self._flush_batch(batch, ctx)
                    batch = []

        if batch:
            self._flush_batch(batch, ctx)

        for loader in self.loaders:
            loader.close()

        ctx.finish()
        logger.info(f"Pipeline '{self.name}' finished. Stats: {ctx.summary()}")
        return ctx

    def _flush_batch(self, batch: List, ctx: PipelineContext):
        for loader in self.loaders:
            loader.load(batch)
        ctx.records_loaded += len(batch)
