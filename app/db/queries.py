import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

from app.config import DATABASE_URL


def _conn():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


def get_products() -> list[dict]:
    with _conn() as conn:
        return conn.execute(
            "SELECT id, sku, name FROM products ORDER BY id"
        ).fetchall()


def get_branches() -> list[str]:
    with _conn() as conn:
        rows = conn.execute(
            "SELECT DISTINCT branch FROM stock ORDER BY branch"
        ).fetchall()
    return [r["branch"] for r in rows]


def get_stock(product_id: int, branch: str) -> dict | None:
    with _conn() as conn:
        return conn.execute(
            "SELECT quantity, reorder_level FROM stock "
            "WHERE product_id = %s AND branch = %s",
            (product_id, branch),
        ).fetchone()


def create_request(request_text: str, branch: str, requested_by: str = "employee") -> int:
    with _conn() as conn:
        row = conn.execute(
            "INSERT INTO purchase_requests (requested_by, branch, request_text) "
            "VALUES (%s, %s, %s) RETURNING id",
            (requested_by, branch, request_text),
        ).fetchone()
    return row["id"]


def log_event(entity: str, entity_id: int | None, action: str,
              actor: str, details: dict) -> None:
    with _conn() as conn:
        conn.execute(
            "INSERT INTO audit_log (entity, entity_id, action, actor, details) "
            "VALUES (%s, %s, %s, %s, %s)",
            (entity, entity_id, action, actor, Jsonb(details)),
        )