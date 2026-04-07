import psycopg2
from config import DB_CONFIG


def get_connection():
    """Return a new psycopg2 connection using settings from config.py."""
    return psycopg2.connect(**DB_CONFIG)


def create_table():
    """Create the phonebook table if it does not exist."""
    sql = """
        CREATE TABLE IF NOT EXISTS phonebook (
            id         SERIAL PRIMARY KEY,
            first_name VARCHAR(50)  NOT NULL,
            phone      VARCHAR(20)  NOT NULL UNIQUE
        );
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
