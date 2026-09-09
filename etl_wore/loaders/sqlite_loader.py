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

        conn = self._get_connection()
        columns = list(records[0].keys())
        col_defs = ", ".join(f'"{col}" TEXT' for col in columns)
        create_sql = f'CREATE TABLE IF NOT EXISTS "{self.table_name}" ({col_defs})'

        placeholders = ", ".join("?" for _ in columns)
        insert_sql = f'INSERT INTO "{self.table_name}" ({", ".join(f"`{c}`" for c in columns)}) VALUES ({placeholders})'

        try:
            with conn:
                conn.execute(create_sql)
                rows = [[str(r.get(c, "")) for c in columns] for r in records]
                conn.executemany(insert_sql, rows)
        except Exception as e:
            raise LoadingError(f"Failed to insert into SQLite table {self.table_name}: {e}") from e

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None
