# Copyright Wirepas Oy 2026 licensed under Apache 2.0
#
# Please see file LICENSE for full license details.
import csv
import os
import tempfile
import unittest
from unittest.mock import MagicMock, mock_open, patch

import psycopg

from nms_integration_tool.data_source import CsvDataSource, DataSource, PostgresDataSource, XlsxDataSource


class DataSourceBaseTest(unittest.TestCase):
    def test_ingest_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            DataSource().ingest()


class CsvDataSourceTest(unittest.TestCase):
    def test_ingest_returns_rows_as_list_of_dicts(self):
        csv_content = "name,address\nfoo,1\nbar,2\n"
        with patch("builtins.open", mock_open(read_data=csv_content)):
            result = CsvDataSource("dummy.csv").ingest()
        self.assertEqual(result, [{"name": "foo", "address": "1"}, {"name": "bar", "address": "2"}])

    def test_ingest_header_only_returns_empty_list(self):
        with patch("builtins.open", mock_open(read_data="name,address\n")):
            result = CsvDataSource("dummy.csv").ingest()
        self.assertEqual(result, [])

    def test_ingest_preserves_all_columns(self):
        csv_content = "a,b,c\n1,2,3\n"
        with patch("builtins.open", mock_open(read_data=csv_content)):
            result = CsvDataSource("dummy.csv").ingest()
        self.assertEqual(result, [{"a": "1", "b": "2", "c": "3"}])

    def test_ingest_real_file(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["name", "value"])
            writer.writeheader()
            writer.writerow({"name": "alpha", "value": "10"})
            writer.writerow({"name": "beta", "value": "20"})
            f_name = f.name
        try:
            result = CsvDataSource(f_name).ingest()
            self.assertEqual(result, [{"name": "alpha", "value": "10"}, {"name": "beta", "value": "20"}])
        finally:
            os.unlink(f_name)

    def test_ingest_missing_file_raises_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            CsvDataSource("__nonexistent_file_xyz__.csv").ingest()


class XlsxDataSourceTest(unittest.TestCase):
    def _make_workbook(self, rows):
        ws = MagicMock()
        ws.values = iter(rows)
        wb = MagicMock()
        wb.sheetnames = ["Sheet1"]
        wb.__getitem__ = MagicMock(return_value=ws)
        return wb

    def test_ingest_returns_rows_as_list_of_dicts(self):
        rows = [("name", "address"), ("site-a", 10), ("site-b", 20)]
        with patch("openpyxl.load_workbook", return_value=self._make_workbook(rows)):
            result = XlsxDataSource("dummy.xlsx").ingest()
        self.assertEqual(result, [{"name": "site-a", "address": 10}, {"name": "site-b", "address": 20}])

    def test_ingest_header_only_returns_empty_list(self):
        rows = [("name", "address")]
        with patch("openpyxl.load_workbook", return_value=self._make_workbook(rows)):
            result = XlsxDataSource("dummy.xlsx").ingest()
        self.assertEqual(result, [])

    def test_ingest_passes_kwargs_to_load_workbook(self):
        rows = [("col",)]
        with patch("openpyxl.load_workbook", return_value=self._make_workbook(rows)) as mock_load:
            XlsxDataSource("data.xlsx").ingest(read_only=True, data_only=True)
        mock_load.assert_called_once_with("data.xlsx", read_only=True, data_only=True)

    def test_read_excel_closes_workbook_on_normal_exit(self):
        wb = MagicMock()
        with patch("openpyxl.load_workbook", return_value=wb):
            with XlsxDataSource.read_excel("dummy.xlsx") as opened:
                self.assertIs(opened, wb)
        wb.close.assert_called_once()


class PostgresDataSourceTest(unittest.TestCase):
    def _make_conn(self, cur):
        conn = MagicMock()
        conn.__enter__ = MagicMock(return_value=conn)
        conn.__exit__ = MagicMock(return_value=False)
        conn.cursor.return_value = cur
        return conn

    def _make_cur(self, rows):
        cur = MagicMock()
        cur.__enter__ = MagicMock(return_value=cur)
        cur.__exit__ = MagicMock(return_value=False)
        cur.fetchall.return_value = rows
        return cur

    def test_conn_str_is_stored(self):
        conn_str = "postgresql://u:p@host:5432/db"
        self.assertEqual(PostgresDataSource(conn_str).conn_str, conn_str)

    def test_test_connection_returns_true_on_success(self):
        conn = MagicMock()
        conn.__enter__ = MagicMock(return_value=conn)
        conn.__exit__ = MagicMock(return_value=False)
        with patch("psycopg.connect", return_value=conn):
            self.assertTrue(PostgresDataSource("postgresql://u:p@h/db").test_connection())

    def test_test_connection_returns_false_on_psycopg_error(self):
        with patch("psycopg.connect", side_effect=psycopg.Error("refused")):
            self.assertFalse(PostgresDataSource("postgresql://u:p@h/db").test_connection())

    def test_ingest_returns_query_results(self):
        expected = [{"name": "n1", "address": 1}, {"name": "n2", "address": 2}]
        cur = self._make_cur(expected)
        conn = self._make_conn(cur)
        with patch("psycopg.connect", return_value=conn):
            result = PostgresDataSource("postgresql://u:p@h/db").ingest("SELECT * FROM nodes")
        cur.execute.assert_called_once_with("SELECT * FROM nodes")
        self.assertEqual(result, expected)

    def test_ingest_empty_query_result(self):
        cur = self._make_cur([])
        conn = self._make_conn(cur)
        with patch("psycopg.connect", return_value=conn):
            result = PostgresDataSource("postgresql://u:p@h/db").ingest("SELECT 1 WHERE false")
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
