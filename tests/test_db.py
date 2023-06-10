from unittest.mock import patch, MagicMock

import add_path  # noqa: F401
from pkg.db import SQLite


@patch("sqlite3.connect")
def test_connect(mock_connect):
    SQLite("test_db_path")
    mock_connect.assert_called_once_with("test_db_path")


@patch("sqlite3.connect")
def test_close(mock_connect):
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn
    mock_db = SQLite("test_db_path")
    mock_db.close()
    mock_conn.close.assert_called_once()
