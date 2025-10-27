from pydantic import BaseModel
from datetime import date

class Book(BaseModel):
    title: str
    author: str
    published_date: date | None = None
    isbn: str

