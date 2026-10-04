import sqlite3
import os

DB_PATH = "data.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_file TEXT,
                code TEXT,
                name TEXT,
                size TEXT,
                unit_price REAL,
                search_text TEXT,
                loaded_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Create an index to speed up search queries
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_search_text ON products(search_text)')
        conn.commit()

def insert_products(products):
    """
    Insert a list of product tuples into the database.
    Each tuple should be (source_file, code, name, size, unit_price, search_text)
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.executemany('''
            INSERT INTO products (source_file, code, name, size, unit_price, search_text)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', products)
        conn.commit()

def get_loaded_files():
    """
    Returns a list of dictionaries with info about loaded files.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT source_file, COUNT(*) as row_count, MAX(loaded_on) as loaded_on
            FROM products
            GROUP BY source_file
        ''')
        return [{"source_file": row[0], "row_count": row[1], "loaded_on": row[2]} for row in cursor.fetchall()]

def remove_file_data(source_file):
    """
    Removes all rows associated with a specific file.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM products WHERE source_file = ?', (source_file,))
        conn.commit()

def search_products(query, limit=15):
    """
    Searches for products matching the query in their code or name.
    """
    query = query.lower().strip()
    if not query:
        return []
        
    with get_connection() as conn:
        cursor = conn.cursor()
        # Simple LIKE search. For SQLite, %query% works well.
        cursor.execute('''
            SELECT id, code, name, size, unit_price
            FROM products
            WHERE search_text LIKE ?
            LIMIT ?
        ''', (f'%{query}%', limit))
        
        columns = ["id", "code", "name", "size", "unit_price"]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
