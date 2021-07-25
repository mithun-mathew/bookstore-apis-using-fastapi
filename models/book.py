from pydantic import BaseModel, Field
from models.author import Author
from utils.const import ISBN_DESCRIPTION


class Book(BaseModel):
    isbn: str = Field(None, description=ISBN_DESCRIPTION)
    name: str
    author: Author
    year: int = Field(None, lt=2100, gt=1900)
