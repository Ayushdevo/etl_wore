"""
Command-line interface for running etl_wore pipelines.
"""

import argparse
import json
import logging
import sys
from pathlib import Path

from .builder import _same_path, build_pipeline
from .exceptions import ConfigurationError, EtlException
from .logger import setup_logger
from .metrics import write_metrics
from .spec_parser import SpecParser

logger = setup_logger("etl_wore.cli")


def main(argv=None):
    parser = argparse.ArgumentParser(description="etl_wore CLI runner")
    parser.add_argument("--spec", type=str, help="Path to pipeline specification file (JSON/YAML)")
    parser.add_argument(
        "--dry-run", action="store_true", help="Validate specification without running"
    )
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")

    parser.add_argument(
        "--summary", choices=("human", "json"), default="human", help="Summary output format"
    )

    parser.add_argument("--batch-size", type=int, help="Override the specification batch size")

    parser.add_argument("--metrics-path", help="Write successful-run metrics as JSON")

    args = parser.parse_args(argv)
    level = logging.DEBUG if args.verbose else logging.INFO
    logger.setLevel(level)
    for name in ("etl_wore.pipeline.engine", "etl_wore.utils.retry"):
        logging.getLogger(name).setLevel(level)
    if not args.spec:
        parser.print_help()
        sys.exit(1)

    try:
        spec = SpecParser.parse_file(args.spec)
        if args.batch_size is not None:
            spec["batch_size"] = args.batch_size
        pipeline = build_pipeline(spec, base_dir=Path(args.spec).resolve().parent)
        for sink in pipeline.loaders:
            destination = getattr(sink, "output_path", getattr(sink, "db_path", None))
            if destination is not None and _same_path(destination, args.spec):
                raise ConfigurationError("Output destination must not overwrite the specification")
        if args.metrics_path:
            protected = [
                getattr(component, name)
                for component in pipeline.extractors + pipeline.loaders
                for name in ("filepath", "output_path", "db_path")
                if hasattr(component, name)
            ]
            protected.append(args.spec)
            if any(_same_path(args.metrics_path, path) for path in protected):
                raise ConfigurationError(
                    "Metrics destination must differ from the specification, inputs, and outputs"
                )
    except EtlException as exc:
        parser.error(str(exc))
    logger.info(f"Loaded specification from: {args.spec}")
    if args.dry_run:
        logger.info("Dry run check passed successfully.")
        sys.exit(0)
    try:
        context = pipeline.run()
        if args.metrics_path:
            write_metrics(context, args.metrics_path)
    except (EtlException, OSError) as exc:
        parser.error(str(exc))
    if args.summary == "json":
        print(json.dumps(context.summary(), allow_nan=False))
    else:
        summary = context.summary()
        print(
            f"{summary['pipeline']}: extracted={summary['extracted']} loaded={summary['loaded']} dropped={summary['dropped']}"
        )
    return 0


if __name__ == "__main__":
    main()
