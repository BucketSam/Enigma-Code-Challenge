
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from main import app, db
from BookModel import Book

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_db(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr("main.db", mock)
    return mock

def test_get_books(mock_db):
    mock_db.get_books.return_value = [
        Book(id=1, title="Book1", author="Author1", published_date=None, isbn="123")
    ]
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json()[0]["title"] == "Book1"

def test_add_book_success(mock_db):
    book = Book(id=1, title="Book1", author="Author1", published_date=None, isbn="123")
    mock_db.add_book.return_value = book
    response = client.post("/books", json=book.dict())
    assert response.status_code == 201
    assert response.json()["title"] == "Book1"

def test_add_book_failure(mock_db):
    mock_db.add_book.side_effect = ValueError("Invalid book")
    response = client.post("/books", json={"id":1,"title":"","author":"", "published_date":None,"isbn":"123"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid book"

def test_get_book_not_found(mock_db):
    mock_db.get_book_by_id.return_value = None
    response = client.get("/books/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"

def test_update_book_not_found(mock_db):
    mock_db.update_book.return_value = None
    response = client.put("/books/999", json={"id":999,"title":"X","author":"Y","published_date":None,"isbn":"Z"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"

def test_delete_book_not_found(mock_db):
    mock_db.delete_book.return_value = False
    response = client.delete("/books/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"



