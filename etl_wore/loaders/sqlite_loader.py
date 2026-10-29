"""
SQLite destination loader with dynamic table creation.
"""
import sqlite3
import os
from typing import List, Dict, Any
from .base import BaseLoader
from ..exceptions import LoadingError

class SqliteLoader(BaseLoader):
    def __init__(self, db_path: str, table_name: str):
        super().__init__(name=f"SqliteLoader({table_name})")
        self.db_path = db_path
        self.table_name = table_name
        self._conn = None

    def _get_connection(self):
        if self._conn is None:
            os.makedirs(os.path.dirname(os.path.abspath(self.db_path)), exist_ok=True)
            self._conn = sqlite3.connect(self.db_path)
        return self._conn

    def load(self, records: List[Dict[str, Any]]):
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
                conn.execute(create_sql)
                rows = [[None if r.get(c, "") is None else str(r.get(c, "")) for c in columns] for r in records]
                conn.executemany(insert_sql, rows)
        except Exception as e:
            raise LoadingError(f"Failed to insert into SQLite table {self.table_name}: {e}") from e

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None

