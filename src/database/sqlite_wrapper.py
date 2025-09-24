import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Optional

from src.data_models.simple_company_model import CompanyMetadata


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


class SqliteWrapper:
    """High‑level CRUD interface for the single‑table key/value store."""

    @crud_operation
    def create(self, company_name: str, metadata: CompanyMetadata) -> None:
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
                (company_name, metadata.to_json(), now, now),
            )
            con.commit()

    @crud_operation
    def read(self, company_name: str) -> Optional[CompanyMetadata]:
        """Return the CompanyMetadata for *company_name* or None if not found."""
        with _connect() as con:
            cur = con.cursor()
            cur.execute(
                """
                SELECT metadata_json FROM company_privacy
                WHERE company_name = ?;
                """,
                (company_name,),
            )
            row = cur.fetchone()
            if row:
                return CompanyMetadata.from_json(row[0])
            return None

    @crud_operation
    def update(self, company_name: str, new_metadata: CompanyMetadata) -> bool:
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
                (new_metadata.to_json(), now, company_name),
            )
            con.commit()
            return cur.rowcount > 0

    @crud_operation
    def delete(self, company_name: str) -> bool:
        """Delete the row for *company*. Returns True if something was removed."""
        with _connect() as con:
            cur = con.cursor()
            cur.execute(
                "DELETE FROM company_privacy WHERE company_name = ?;",
                (company_name,),
            )
            con.commit()
            return cur.rowcount > 0

    @crud_operation
    def list_all(self) -> dict[str, CompanyMetadata]:
        """Return a dict mapping company_name → CompanyMetadata for every row."""
        result: dict[str, CompanyMetadata] = {}
        with _connect() as con:
            cur = con.cursor()
            cur.execute(
                "SELECT company_name, metadata_json FROM company_privacy;"
            )
            for company_name, json_blob in cur.fetchall():
                result[company_name] = CompanyMetadata.from_json(json_blob)
        return result
