# Copyright Wirepas Oy 2026 licensed under Apache 2.0
#
# Please see file LICENSE for full license details.
import contextlib
import csv
from .logger import get_logger
logger = get_logger(__name__)
import openpyxl
from typing import List

import psycopg
from psycopg.rows import dict_row


class DataSource:
    """
    Interface to get data from many data sources.
    Any new data source needs to inherit from the DataSource class
    and implement the ingest function.
    """

    def __init__(self) -> None:
        pass

    def ingest(self, **kwargs) -> List[dict]:
        """
        Get data from a data source and return a list of dictionaries.
        The dictionaries inside the list represent data items.
        A dictionary is a mapping between the metadata services data parameters
        and their values.
        """
        raise NotImplementedError


class CsvDataSource(DataSource):
    """
    Module to get data from csv data sources.
    """

    def __init__(self, file) -> None:
        super().__init__()
        self._file = file

    def ingest(self, **kwargs) -> List[dict]:
        res = []
        logger.info("CsvDataSource -> Ingest data from %s", self._file)
        with open(self._file, encoding='utf-8') as csv_data:
            rows = csv.DictReader(csv_data)
            for row in rows:
                logger.debug("Ingesting: %s", row)
                res.append(row)
        return res


class XlsxDataSource(DataSource):
    """
    Module to get data from XLSX Excel data sources.
    """

    def __init__(self, file) -> None:
        super().__init__()
        self._file = file

    @staticmethod
    @contextlib.contextmanager
    def read_excel(filename, **kwargs):
        """
        Open an openpyxl worksheet and automatically close it when finished.
        """
        workbook = openpyxl.load_workbook(filename, **kwargs)
        yield workbook
        workbook.close()

    def ingest(self, **kwargs) -> List[dict]:
        res = []
        logger.info("XlsxDataSource -> Ingest data from %s", self._file)
        with self.read_excel(self._file, **kwargs) as workbook:
            worksheet = workbook[workbook.sheetnames[0]]
            rows = worksheet.values
            headers = next(rows)
            res = [dict(zip(headers, r)) for r in rows]
        return res


class PostgresDataSource(DataSource):
    """
    Module to get data from Postgres database data sources.
    """

    def __init__(self, conn_str) -> None:
        """

        Args:
            conn_str: The connection string (a postgresql:// url or a list of key=value pairs)
                      to specify where and how to connect.
                      See https://www.psycopg.org/psycopg3/docs/api/connections.html#psycopg.Connection
        """
        super().__init__()
        self.conn_str = conn_str

    def test_connection(self):
        try:
            with psycopg.connect(self.conn_str, connect_timeout=3) as _:
                return True
        except psycopg.Error as e:
            logger.info(f"DB unreachable: {e}")
            return False

    def ingest(self, query, **kwargs) -> List[dict]:
        """
        Fetches query results and returns rows as a list of dictionaries

        Args:
            query: SQL query
            **kwargs:
        """
        with psycopg.connect(self.conn_str) as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(query)
                return cur.fetchall()
