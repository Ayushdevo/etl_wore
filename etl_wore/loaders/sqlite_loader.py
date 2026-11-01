"""
SQLite destination loader with dynamic table creation.
"""

import os
import sqlite3
from threading import RLock
from typing import Any, Dict, List

from ..exceptions import LoadingError
from .base import BaseLoader


def _identifier_key(value):
    # SQLite identifiers fold ASCII letters only, not Unicode case variants.
    return value.translate(str.maketrans('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))


class SqliteLoader(BaseLoader):
    def __init__(self, db_path: str, table_name: str):
        super().__init__(name=f"SqliteLoader({table_name})")
        self.db_path = db_path
        self.table_name = table_name
        self._conn = None
        self._lock = RLock()

    def _get_connection(self):
        if self._conn is None:
            os.makedirs(os.path.dirname(os.path.abspath(self.db_path)), exist_ok=True)
            self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        return self._conn

    def load(self, records: List[Dict[str, Any]]):
        # A shared connection needs serialization across worker loads and close.
        with self._lock:
            return self._load_locked(records)

    def _load_locked(self, records):
        if not records:
            return

        columns = list(records[0].keys())
        if any(set(record) - set(columns) for record in records):
            raise LoadingError("Record contains columns absent from the first SQLite batch record")

        def quote(identifier):
            return '"' + identifier.replace('"', '""') + '"'

        table = quote(self.table_name)
        col_defs = ", ".join(f"{quote(col)} TEXT" for col in columns)
        create_sql = f"CREATE TABLE IF NOT EXISTS {table} ({col_defs})"

        placeholders = ", ".join("?" for _ in columns)
        column_names = ", ".join(quote(col) for col in columns)
        insert_sql = f"INSERT INTO {table} ({column_names}) VALUES ({placeholders})"

        try:
            conn = self._get_connection()
            with conn:
                # Include schema changes in the same transaction as the batch.
                conn.execute("BEGIN")
                conn.execute(create_sql)
                existing_columns = {
                    _identifier_key(row[1]) for row in conn.execute(f"PRAGMA table_info({table})")
                }
                for column in columns:
                    if _identifier_key(column) not in existing_columns:
                        conn.execute(f"ALTER TABLE {table} ADD COLUMN {quote(column)} TEXT")
                rows = [
                    [None if r.get(c) is None else str(r[c]) for c in columns]
                    for r in records
                ]
                conn.executemany(insert_sql, rows)
        except Exception as e:
            raise LoadingError(f"Failed to insert into SQLite table {self.table_name}: {e}") from e

    def close(self):
        with self._lock:
            if self._conn:
                self._conn.close()
                self._conn = None
