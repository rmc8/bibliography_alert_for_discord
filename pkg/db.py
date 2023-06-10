from pandas import read_sql, DataFrame
import sqlite3
from sqlite3 import Error, Connection
from functools import wraps
from typing import Callable


class SQLite:
    def __init__(self, db_path: str):
        self.conn = self.connect(db_path)

    @staticmethod
    def handle_errors(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Error as e:
                print(f"Error occurred while executing {func.__name__}: {e}")

        return wrapper

    @handle_errors
    def connect(self, db_path: str) -> Connection:
        return sqlite3.connect(db_path)

    @handle_errors
    def get_table(self) -> DataFrame:
        df = read_sql("SELECT * FROM bibliography", con=self.conn)
        return df

    @handle_errors
    def insert_many(self, records: list) -> None:
        with self.conn:
            cur = self.conn.cursor()
            cur.executemany("INSERT INTO bibliography values(?,?,?,?)", records)

    @handle_errors
    def close(self) -> None:
        self.conn.close()
