from typing import Optional
from fastapi import FastAPI, HTTPException, Request, status, Form, Header
from pydantic import BaseModel, Field
from uuid import UUID
from starlette.responses import JSONResponse


class NegativeNumberException(Exception):
    def __init__(self, books_to_return):
        self.books_to_return = books_to_return


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


class BookNoRating(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str
    description: Optional[str] = Field(
        None,
        title="description of the Book",
        max_length=100,
        min_length=1
    )


BOOKS = []

# Creating Custom Handlers is extremely important with an API,
# so you can clarify the air back to the client and user.


@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(request: Request,
                                            exception: NegativeNumberException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Hey, why do you want {exception.books_to_return} "
                            f"books? You need to read more!"}
    )

# Form Fields is different than query parameters and JSON and is typically sent using the HTML form tags.
# Many different types of authentication platforms want the username and password to be sent using forms and not a different type of data transfer.
# When using form data, the data is typically encoded using the media type.
# In FastAPI will automatically decode the forms for you.


@app.post("/books/login")
async def book_login(username: str = Form(...), password: str = Form(...)):
    return {"username": username, "password": password}


# Headers are a way that we can send additional information with each request
# As the API receives the headers, we can now do whatever we want the headers and do some kind of validation if needed
@app.get('/header')
async def read_header(random_header: Optional[str] = Header(None)):
    return {"Random-Header": random_header}


@app.get("/")
async def read_all_books(books_to_return: Optional[int] = None):

    if books_to_return and books_to_return < 0:
        raise NegativeNumberException(books_to_return=books_to_return)

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
    raise raise_item_cannot_be_found_exception()


@app.get('/book/rating/{book_id}', response_model=BookNoRating)
async def read_book_no_rating(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    raise raise_item_cannot_be_found_exception()

# Post Request BaseModel
# Status Code Response : status_code=status.HTTP_201_CREATED


@app.post("/", status_code=status.HTTP_201_CREATED)
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
    raise raise_item_cannot_be_found_exception()


@app.delete("/{book_id}")
async def delete_book(book_id: UUID):
    counter = 0
    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            del BOOKS[counter - 1]
            return f"ID: {book_id} deleted"
    raise raise_item_cannot_be_found_exception()
    # raise HTTPException(status_code=404, detail='Book not found',
    #                     headers={'X-Header-Error':
    #                              "Nothing to be seen at the UUID"})


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


def raise_item_cannot_be_found_exception():
    return HTTPException(status_code=404,
                         detail='Book not found',
                         headers={'X-Header_Error':
                                  "Nothing to be seen at the UUID"})
