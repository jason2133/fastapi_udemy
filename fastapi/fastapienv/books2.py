from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field
from uuid import UUID

app = FastAPI()

# Create BOOKS object
# FastAPI Project : BaseModel
# [AWESOME] FastAPI and Pydantic are doing all of this data validation without any extra coding effort from you.


class Book(BaseModel):
    id: UUID
    # 제목은 최소한 1자 이상이어야 한다는 조건을 걸은거임.
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    # Description의 제목은 Description of the book이며, 최소 1자, 최대 100자라는 조건을 걸음.
    # Optional[str]을 추가함으로써 이 변수가 필수는 아니라고 지정하고 있음. 다른 변수들은 필수로 채워야하는 요소임.
    description: Optional[str] = Field(title='Description of the book',
                                       max_length=100,
                                       min_length=1)
    # gt : greater than 초과
    # lt : less than 미만
    rating: int = Field(gt=-1, lt=101)

    class Config:
        schema_extra = {
            "example": {
                "id": "17a139dd-b20e-40ac-8b8d-8dd96619a17e",
                "title": "Data Science 101",
                "author": "Jason Lee",
                "description": "Ensemble SVM Kernel LightGBM CatBoost AdaBoost Regression Classification",
                "rating": 99
            }
        }


BOOKS = []


@app.get("/")
async def read_all_books(books_to_return: Optional[int] = None):
    if len(BOOKS) < 1:
        create_books_no_api()

    if books_to_return and len(BOOKS) >= books_to_return > 0:
        i = 1
        new_books = []
        while i <= books_to_return:
            new_books.append(BOOKS[i - 1])
            i += 1
        return new_books
    return BOOKS

# Get by UUID


@app.get('/book/{book_id}')
async def read_book(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x

# Post Request BaseModel


@app.post("/")
async def create_book(book: Book):
    BOOKS.append(book)
    return book


@app.put("/{book_id}")
async def update_book(book_id: UUID, book: Book):
    counter = 0
    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            BOOKS[counter - 1] = book
            return BOOKS[counter - 1]


@app.delete("/{book_id}")
async def delete_book(book_id: UUID):
    counter = 0
    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            del BOOKS[counter - 1]
            return f"ID: {book_id} deleted"


def create_books_no_api():
    book_1 = Book(id='87a039dd-b20e-40ac-8b8d-8dd96619a17e',
                  title="Title 1",
                  author="Author 1",
                  description="Description 1",
                  rating=60)
    book_2 = Book(id='27a039dd-b20e-40ac-8b8d-8dd96619a17e',
                  title="Title 2",
                  author="Author 2",
                  description="Description 2",
                  rating=70)
    book_3 = Book(id='37a039dd-b20e-40ac-8b8d-8dd96619a17e',
                  title="Title 3",
                  author="Author 3",
                  description="Description 3",
                  rating=80)
    book_4 = Book(id='47a039dd-b20e-40ac-8b8d-8dd96619a17e',
                  title="Title 4",
                  author="Author 4",
                  description="Description 4",
                  rating=90)
    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)
