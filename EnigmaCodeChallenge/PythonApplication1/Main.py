from BookModel import Book
from fastapi import FastAPI, HTTPException
from typing import List
from DbManager import DatabaseManager

app=FastAPI("Simple Crud App")

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

