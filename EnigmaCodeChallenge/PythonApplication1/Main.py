from BookModel import Book
from fastapi import FastAPI, HTTPException
from typing import List
from DbManager import DatabaseManager

app=FastAPI()

db = DatabaseManager()

@app.get("/books", response_model=List[Book])
def get_books():
    return db.get_books()

@app.post("/books", response_model=Book, status_code=201)
def add_book(book: Book):
    try:
        return db.add_book(book)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    """Get a single book by ID"""
    book = db.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, updated: Book):
    try:
        book = db.update_book(book_id, updated)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return book
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int):
    """Delete a book by ID"""
    deleted = db.delete_book(book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return None

