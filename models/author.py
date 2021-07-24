from pydantic import BaseModel
from fastapi import Query
from typing import List


# from models.book import Book


class Author(BaseModel):
    name: str
    book: List[str]
