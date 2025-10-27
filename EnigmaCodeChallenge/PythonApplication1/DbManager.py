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
