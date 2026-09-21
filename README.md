# etl_wore

> Lightweight, extensible ETL (Extract, Transform, Load) Workflow and Orchestration Engine in Python.

[![CI](https://github.com/Ayushdevo/etl_wore/actions/workflows/ci.yml/badge.svg)](https://github.com/Ayushdevo/etl_wore/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

---

## Features

- **Extensible Architecture**: Clean object-oriented contracts (`BaseExtractor`, `BaseTransformer`, `BaseLoader`).
- **Built-in Extractors**: CSV (auto-sniffer), JSON, JSON Lines, and REST API with pagination.
- **Robust Transformers**: Type validation, schema casting, PII masking, deduplication, and ISO datetime normalization.
- **Versatile Sinks**: CSV, JSON Lines, and SQLite with auto-table migration.
- **Reliable Execution**: Built-in exponential backoff retries, parallel processing, and progress telemetry.
- **Zero Heavy Dependencies**: Runs lightweight out of the box with standard library fallbacks.

---

## Quickstart

```bash
git clone https://github.com/Ayushdevo/etl_wore.git
cd etl_wore
pip install -e .
```

### Python Example

```python
from etl_wore.pipeline.engine import Pipeline
from etl_wore.extractors.csv_extractor import CsvExtractor
from etl_wore.transformers.sanitizer import DataSanitizer
from etl_wore.loaders.json_loader import JsonLinesLoader

pipeline = Pipeline("clean_customers")
pipeline.add_extractor(CsvExtractor("data/customers.csv"))
pipeline.add_transformer(DataSanitizer(strip_strings=True, mask_fields=["ssn"]))
pipeline.add_loader(JsonLinesLoader("data/output.jsonl"))

result = pipeline.run()
print(result.summary())
```

---

## Testing

```bash
pytest -v
```

---

## License

Released under the [MIT License](LICENSE).
