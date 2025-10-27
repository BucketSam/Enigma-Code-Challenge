from pydantic import BaseModel
from datetime import date

class BookBase(BaseModel):
    title: str
    author: str
    published_date: date | None = None
    isbn: str

