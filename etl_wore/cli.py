"""
Command-line interface for running etl_wore pipelines.
"""
import argparse
import logging
import sys
from .logger import setup_logger
from .spec_parser import SpecParser
from .exceptions import ConfigurationError

logger = setup_logger("etl_wore.cli")

def main():
    parser = argparse.ArgumentParser(description="etl_wore CLI runner")
    parser.add_argument("--spec", type=str, help="Path to pipeline specification file (JSON/YAML)")
    parser.add_argument("--dry-run", action="store_true", help="Validate specification without running")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")

    args = parser.parse_args()
    logger.setLevel(logging.DEBUG if args.verbose else logging.INFO)
    if not args.spec:
        parser.print_help()
        sys.exit(1)

    try:
        SpecParser.parse_file(args.spec)
    except ConfigurationError as exc:
        parser.error(str(exc))
    logger.info(f"Loaded specification from: {args.spec}")
    if args.dry_run:
        logger.info("Dry run check passed successfully.")
        sys.exit(0)
    parser.error("Declarative execution is not implemented; use --dry-run to validate or construct a Pipeline in Python")

if __name__ == "__main__":
    main()

