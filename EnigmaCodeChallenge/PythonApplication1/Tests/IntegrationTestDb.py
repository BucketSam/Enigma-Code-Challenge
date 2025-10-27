import pytest
from fastapi.testclient import TestClient
from main import app, db
from BookModel import Book

client = TestClient(app)

@pytest.fixture
def cleanup_db():
    yield
    all_books = db.get_books()
    for book in all_books:
        db.delete_book(book.id)

def test_add_and_get_book(cleanup_db):
    book_data = Book(id=None, title="Integration Test Book", author="Tester", published_date=None, isbn="9esfvr4429feef9")

   
    response = client.post("/books", json=book_data.dict())
    assert response.status_code == 201
    added_book = response.json()
    assert added_book["title"] == "Integration Test Book"

    # 2️⃣ Recupera il libro tramite ID
    response = client.get(f"/books/{added_book['id']}")
    assert response.status_code == 200
    fetched_book = response.json()
    assert fetched_book["title"] == "Integration Test Book"

    # 3️⃣ Pulizia: cancella il libro
    response = client.delete(f"/books/{added_book['id']}")
    assert response.status_code == 204
