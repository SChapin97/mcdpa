import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Optional

from src.data_models.company_mcdpa_metadata_model import CompanyPrivacyRecord


DB_PATH = Path(__file__).parent / "company_privacy.sqlite"


def _connect():
    """Open a connection; `detect_types` lets us store/retrieve datetime objects."""
    return sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)


def init_db():
    """Create the table if it does not exist yet."""
    with _connect() as con:
        cur = con.cursor()
        cur.execute(
            f"""
            CREATE TABLE IF NOT EXISTS company_privacy (
                company_name   TEXT PRIMARY KEY,
                metadata_json  TEXT NOT NULL,
                created_at     TIMESTAMP NOT NULL,
                updated_at     TIMESTAMP NOT NULL
            );
            """
        )
        con.commit()


# --------------------------------------------------------------
# Decorators – they simply forward the call to the underlying method
# but give us a clean, declarative syntax for the public API.
# --------------------------------------------------------------

def crud_operation(func):
    """Simple decorator that prints what is happening (helps debugging)."""
    def wrapper(*args, **kwargs):
        print(f"[CRUD] Executing {func.__name__} …")
        return func(*args, **kwargs)
    return wrapper


class CompanyPrivacyRepo:
    """High‑level CRUD interface for the single‑table key/value store."""

    @crud_operation
    def create(self, company: str, metadata: CompanyPrivacyRecord) -> None:
        """Insert a new row. Raises sqlite3.IntegrityError if the key exists."""
        now = datetime.utcnow()
        with _connect() as con:
            cur = con.cursor()
            cur.execute(
                """
                INSERT INTO company_privacy
                (company_name, metadata_json, created_at, updated_at)
                VALUES (?, ?, ?, ?);
                """,
                (company, metadata.to_json(), now, now),
            )
            con.commit()

    @crud_operation
    def read(self, company: str) -> Optional[CompanyPrivacyRecord]:
        """Return the CompanyPrivacyRecord for *company* or None if not found."""
        with _connect() as con:
            cur = con.cursor()
            cur.execute(
                """
                SELECT metadata_json FROM company_privacy
                WHERE company_name = ?;
                """,
                (company,),
            )
            row = cur.fetchone()
            if row:
                return CompanyPrivacyRecord.from_json(row[0])
            return None

    @crud_operation
    def update(self, company: str, new_metadata: CompanyPrivacyRecord) -> bool:
        """
        Replace the JSON payload for *company*.
        Returns True if a row was updated, False if the key does not exist.
        """
        now = datetime.utcnow()
        with _connect() as con:
            cur = con.cursor()
            cur.execute(
                """
                UPDATE company_privacy
                SET metadata_json = ?, updated_at = ?
                WHERE company_name = ?;
                """,
                (new_metadata.to_json(), now, company),
            )
            con.commit()
            return cur.rowcount > 0

    @crud_operation
    def delete(self, company: str) -> bool:
        """Delete the row for *company*. Returns True if something was removed."""
        with _connect() as con:
            cur = con.cursor()
            cur.execute(
                "DELETE FROM company_privacy WHERE company_name = ?;",
                (company,),
            )
            con.commit()
            return cur.rowcount > 0

    @crud_operation
    def list_all(self) -> dict[str, CompanyPrivacyRecord]:
        """Return a dict mapping company → CompanyPrivacyRecord for every row."""
        result: dict[str, CompanyPrivacyRecord] = {}
        with _connect() as con:
            cur = con.cursor()
            cur.execute(
                "SELECT company_name, metadata_json FROM company_privacy;"
            )
            for company, json_blob in cur.fetchall():
                result[company] = CompanyPrivacyRecord.from_json(json_blob)
        return result