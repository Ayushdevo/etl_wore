"""
Unit tests for extractors.
"""
import tempfile
import os
import json
import pytest
from etl_wore.extractors.csv_extractor import CsvExtractor
from etl_wore.extractors.json_extractor import JsonExtractor

def test_csv_extractor():
    with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".csv") as tmp:
        tmp.write("id,name,role\n1,Alice,Engineer\n2,Bob,Manager\n")
        tmp_path = tmp.name

    try:
        extractor = CsvExtractor(tmp_path)
        records = list(extractor.extract())
        assert len(records) == 2
        assert records[0]["name"] == "Alice"
        assert records[1]["role"] == "Manager"
    finally:
        os.remove(tmp_path)

def test_json_extractor():
    with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".json") as tmp:
        data = [{"id": 101, "item": "Laptop"}, {"id": 102, "item": "Keyboard"}]
        json.dump(data, tmp)
        tmp_path = tmp.name

    try:
        extractor = JsonExtractor(tmp_path)
        records = list(extractor.extract())
        assert len(records) == 2
        assert records[0]["item"] == "Laptop"
    finally:
        os.remove(tmp_path)
