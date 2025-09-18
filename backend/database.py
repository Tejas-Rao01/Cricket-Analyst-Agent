import sqlite3
import logging

logger = logging.getLogger(__name__)

DB_NAME = 'cricket_data_yaml.db'

def get_db_connection():
    """Establishes and returns a connection to the database."""
    conn = sqlite3.connect(DB_NAME)
    return conn

def execute_query(sql_query):
    """Executes an SQL query and returns the results."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        return results
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        raise
    finally:
        conn.close()