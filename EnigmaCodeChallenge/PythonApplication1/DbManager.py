import sqlite3
from BookModel import Book

DB_FILE = "books.db"

class DatabaseManager:
    def __init__(self, db_file: str = DB_FILE):
        self.db_file = db_file
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_file)

    def _init_db(self):
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                published_date TEXT,
                isbn TEXT UNIQUE NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def get_books(self):
        conn = self._connect()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM books")
        rows = cur.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def add_book(self, book: Book) -> Book:
        conn = self._connect()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO books (title, author, published_date, isbn) VALUES (?, ?, ?, ?)",
                (book.title, book.author, book.published_date, book.isbn)
            )
            conn.commit()
            book.id = cur.lastrowid
        except sqlite3.IntegrityError:
            raise ValueError("Book with this ISBN already exists")
        finally:
            conn.close()
        return book

    def update_book(self, book_id: int, book: Book) -> dict | None:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        existing = cur.fetchone()
        if not existing:
            conn.close()
            return None

        try:
            cur.execute("""
                UPDATE books
                SET title = ?, author = ?, published_date = ?, isbn = ?
                WHERE id = ?
            """, (book.title, book.author, book.published_date, book.isbn, book_id))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            raise ValueError("Book with this ISBN already exists")
        conn.row_factory = sqlite3.Row
        cur.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        updated = cur.fetchone()
        conn.close()
        return dict(updated) if updated else None

    def delete_book(self, book_id: int) -> bool:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM books WHERE id = ?", (book_id,))
        conn.commit()
        deleted = cur.rowcount > 0
        conn.close()
        return deleted