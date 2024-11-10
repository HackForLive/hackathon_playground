import sqlite3
from pathlib import Path
from typing import List, Optional, Tuple

from genai_hackathon.utils.logger import app_logger



class FinancialReportDbManager:
    def __init__(self, sqlite_db_path: Path):
        self._sqlite_db_path = sqlite_db_path
        self._create_table_if_not_exists()

    def _connect_to_sqlite(self):
        try:
            connection = sqlite3.connect(self._sqlite_db_path.as_posix())
            return connection
        except sqlite3.Error as e:
            print(f"Error while connecting to SQLite: {e}")
            return None
        
    def _create_table_if_not_exists(self):
        conn = self._connect_to_sqlite()
        create_companies_table_query = """
        CREATE TABLE IF NOT EXISTS companies (
            company_name TEXT PRIMARY KEY,
            sector TEXT
        )
        """
        create_summaries_table_query = """
        CREATE TABLE IF NOT EXISTS summaries (
            company_name TEXT PRIMARY KEY,
            summary TEXT,
            FOREIGN KEY (company_name) REFERENCES companies (company_name)
        )
        """
        cursor = conn.cursor()
        cursor.execute(create_companies_table_query)
        cursor.execute(create_summaries_table_query)
        conn.commit()
        conn.close()

    def upsert_company(self, company_name: str, sector: str):
        conn = self._connect_to_sqlite()
        upsert_query = """
        INSERT INTO companies (company_name, sector)
        VALUES (?, ?)
        ON CONFLICT(company_name) DO UPDATE SET
        sector=excluded.sector
        """
        cursor = conn.cursor()
        cursor.execute(upsert_query, (company_name, sector))
        conn.commit()
        conn.close()

    def get_company_by_name(self, company_name: str) -> Tuple[str, str]:
        conn = self._connect_to_sqlite()
        select_query = """
        SELECT company_name, sector FROM companies WHERE company_name = ?
        """
        cursor = conn.cursor()
        cursor.execute(select_query, (company_name,))
        row = cursor.fetchone()
        conn.close()
        return row
    
    def get_companies_by_sector(self, sector: str) -> List[Tuple[str, str]]:
        conn = self._connect_to_sqlite()
        select_query = """
        SELECT company_name, sector FROM companies WHERE sector = ?
        """
        cursor = conn.cursor()
        cursor.execute(select_query, (sector,))
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def upsert_summary(self, company_name, summary):
        conn = self._connect_to_sqlite()
        upsert_query = """
        INSERT INTO summaries (company_name, summary)
        VALUES (?, ?)
        ON CONFLICT(company_name) DO UPDATE SET
        summary=excluded.summary
        """
        cursor = conn.cursor()
        cursor.execute(upsert_query, (company_name, summary))
        conn.commit()
        conn.close()

    def get_all_companies(self) -> List[Tuple[str, str]]:
        conn = self._connect_to_sqlite()
        select_query = """
        SELECT company_name, sector FROM companies
        """
        cursor = conn.cursor()
        cursor.execute(select_query)
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_all_summaries(self):
        conn = self._connect_to_sqlite()
        select_query = """
        SELECT company_name, summary FROM summaries
        """
        cursor = conn.cursor()
        cursor.execute(select_query)
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_summary_for_company(self, company_name: str) -> Optional[str]:
        conn = self._connect_to_sqlite()
        select_query = """
        SELECT summary FROM summaries WHERE company_name = ?
        """
        cursor = conn.cursor()
        cursor.execute(select_query, (company_name,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None
