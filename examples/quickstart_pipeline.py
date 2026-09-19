"""
Demonstration of an end-to-end user processing pipeline.
"""
from etl_wore.pipeline.engine import Pipeline
from etl_wore.extractors.csv_extractor import CsvExtractor
from etl_wore.transformers.sanitizer import DataSanitizer
from etl_wore.transformers.deduplicator import DeduplicationTransformer
from etl_wore.loaders.json_loader import JsonLinesLoader

def run_example():
    pipeline = Pipeline("quickstart_users", batch_size=100)
    pipeline.add_extractor(CsvExtractor("fixtures/sample_users.csv"))
    pipeline.add_transformer(DataSanitizer(strip_strings=True))
    pipeline.add_transformer(DeduplicationTransformer(key_fields=["email"]))
    pipeline.add_loader(JsonLinesLoader("outputs/clean_users.jsonl"))

    stats = pipeline.run()
    print("Execution complete:", stats.summary())

if __name__ == "__main__":
    run_example()
