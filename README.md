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
- **Versatile Sinks**: CSV, JSON Lines, and SQLite with transactional column additions.
- **Reliable Execution**: Built-in exponential backoff retries, parallel processing, and progress telemetry.
- **Declarative CLI**: JSON/YAML pipelines with component validation, dry runs, JSON summaries, and metrics reports.

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

## Run a JSON or YAML specification

The checked-in customer example strips strings, masks emails, casts IDs, normalizes
dates to UTC, and removes duplicate customer/date pairs:

```bash
etl-wore --spec examples/customers.yaml --dry-run
etl-wore --spec examples/customers.yaml --summary json --metrics-path output/run.json
# The module entry point is equivalent:
python -m etl_wore --spec examples/customers.yaml --batch-size 100
```

File paths in a specification are relative to that file's directory, regardless
of the current working directory. `--metrics-path` is relative to the command's
working directory. A dry run validates component types, options and destination
collisions without reading records, contacting REST APIs, or creating outputs;
it does not prove that a source exists or that credentials work.

Each specification requires a nonempty `name`, `extractors` list and `loaders`
list. `transformers` defaults to an empty list and `batch_size` defaults to 500.
Unknown fields, duplicate JSON/YAML mapping keys and invalid option types are
errors. YAML uses a safe loader; duplicate keys introduced by YAML merges are
also rejected. UTF-8 BOM files are supported.

| Section | `type` | Required options | Optional options |
| --- | --- | --- | --- |
| extractors | `csv` | `filepath` | `delimiter`, `encoding` |
| extractors | `json` | `filepath` | `is_lines`, `encoding` |
| extractors | `rest` | `endpoint` | `headers`, `page_param`, `max_pages`, `timeout` |
| transformers | `sanitize` | — | `strip_strings`, `mask_fields` |
| transformers | `schema` | `schema` | `drop_invalid` |
| transformers | `deduplicate` | `key_fields` | — |
| transformers | `dates` | `date_fields` | `output_format` |
| loaders | `csv` | `output_path` | `delimiter` |
| loaders | `jsonl` | `output_path` | — |
| loaders | `sqlite` | `db_path`, `table_name` | — |

`schema` maps field names to `str`, `int`, `float` or `bool`. For example,
`{"type": "schema", "schema": {"id": "int", "active": "bool"}}` casts those
fields; `drop_invalid: true` drops records that cannot be cast. Date parsing
keeps unparseable values unchanged, treats naive dates as UTC, and converts
aware dates to UTC before formatting.

REST pagination starts at page 1 and stops on an empty page. `timeout` is a
finite positive number of seconds per request (default 10). `max_pages` is an
optional positive request limit, including the terminal empty page: if the
endpoint has not terminated within that limit, extraction fails explicitly.

Outputs append to existing files/tables; running a specification again appends
another run. Deduplication applies within a newly built pipeline, not against
previously saved output. SQLite can add new TEXT columns between batches;
rows with additional columns within the same batch are rejected. Multiple
outputs and batches do not share a transaction, so a failure can leave earlier
writes in place. Successful runs can write an atomic JSON metrics report.

Logs go to stderr. `--summary json` writes only the summary object to stdout.
Configuration and built-in processing errors return a nonzero exit code.
The console script and `python -m etl_wore` expose the same options.

For Python callers:

```python
from pathlib import Path
from etl_wore.builder import build_pipeline
from etl_wore.spec_parser import SpecParser

path = Path("examples/customers.yaml")
pipeline = build_pipeline(SpecParser.parse_file(path), base_dir=path.resolve().parent)
context = pipeline.run()
print(context.summary())
```

---

## Testing

```bash
pytest -v
```


---

## License

Released under the [MIT License](LICENSE).

## Additional record transformations

These optional built-ins work in Python and JSON/YAML specifications. Each transform returns a copy; field operations preserve missing/null fields unless stated otherwise. Invalid configuration fails during dry run. Invalid non-null data raises `TransformationError`.

| Type | Options (required first) | Behavior |
| --- | --- | --- |
| `select_fields` | `fields` (required), `require_all` | Project ordered fields; optionally require every selected field. |
| `drop_fields` | `fields` (required) | Remove selected fields, ignoring absent names. |
| `rename_fields` | `mapping` (required) | Rename fields simultaneously, support swaps, and reject overwrites. |
| `copy_fields` | `mapping` (required), `overwrite` | Copy original field values to new destinations; reject overwrites by default. |
| `defaults` | `values` (required), `replace_null` | Fill absent fields with independent default values; optionally replace nulls. |
| `constants` | `values` (required), `overwrite` | Attach constant fields such as source provenance, with optional overwrite protection. |
| `coalesce` | `fields` (required), `target` (required), `skip_empty` | Choose the first present non-null input field, preserving zero and false. |
| `require_fields` | `fields` (required), `drop_invalid`, `allow_null` | Require selected fields with explicit null and drop policies. |
| `filter_value` | `field` (required), `value` (required), `exclude` | Keep or exclude records matching one field value; distinguish missing, null, and booleans. |
| `map_values` | `field` (required), `mapping` (required), `strict` | Map string categories to copied values; optionally reject unmapped values. |
| `string_case` | `fields` (required), `mode` | Normalize string case using lower, upper, Unicode casefold, or title. |
| `replace_text` | `fields` (required), `old` (required), `new` (required), `count` | Replace literal text with an optional nonnegative replacement limit. |
| `regex_replace` | `fields` (required), `pattern` (required), `replacement` (required), `count` | Replace regular-expression matches; validate patterns and backreferences during dry run. |
