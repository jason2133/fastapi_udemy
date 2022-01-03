from typing import Optional
from fastapi import FastAPI, Depends
from fastapi.exceptions import HTTPException
from database import SessionLocal
import models
from database import engine
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from auth import get_current_user, get_user_exception

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# Post Request (Todo Project)


class Todo(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(
        gt=0, lt=6, description="The priority must be between 1-5")
    complete: bool


@app.get("/")
# async def create_database():
#     return {"Database": "Created"}
async def read_all(db: Session = Depends(get_db)):
    # return {"Database": "Created"}
    return db.query(models.Todos).all()


@app.get("/todos/user")
async def read_all_by_user(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    return db.query(models.Todos).filter(models.Todos.owner_id == user.get('id')).all()


@app.get("/todo/{todo_id}")
async def read_todo(todo_id: int,
                    # user가 그 Postman 용도로 추가된 것임.
                    user: dict = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    # Postman 용도로 추가된 if문
    if user is None:
        raise get_user_exception()
    todo_model = db.query(models.Todos)\
        .filter(models.Todos.id == todo_id)\
        .filter(models.Todos.owner_id == user.get('id'))\
        .first()
    # 여기서 2번째 줄인 filter(models.Todos.owner_id == user.get('id))는 Postman 용도로 추가된 것임.

    if todo_model is not None:
        return todo_model
    # raise HTTPException(status_code=404, detail="Todo not found")
    raise http_exception()

# Post Request (Todo Project)
# Create


@app.post("/")
async def create_todo(todo: Todo,
                      # user가 그 Postman 용도로 추가된 것임.
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    # Postman 용도로 추가된 if문
    if user is None:
        raise get_user_exception()
    todo_model = models.Todos()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    todo_model.owner_id = user.get('id')

    db.add(todo_model)
    db.commit()

    successful_response(201)
    # return {
    #     'status': 201,
    #     'transaction': 'Successful'
    # }

# Put Request (Todo Project)
# Update


@app.put("/{todo_id}")
async def update_todo(todo_id: int,
                      todo: Todo,
                      # user가 그 Postman 용도로 추가된 것임.
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    # Postman 용도로 추가된 if문
    if user is None:
        raise get_user_exception()
    todo_model = db.query(models.Todos)\
        .filter(models.Todos.id == todo_id)\
        .filter(models.Todos.owner_id == user.get('id'))\
        .first()
    # 여기서 2번째 줄인 filter(models.Todos.owner_id == user.get('id))는 Postman 용도로 추가된 것임.

    if todo_model is None:
        raise http_exception()

    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete

    db.add(todo_model)
    db.commit()

    successful_response(200)
    # return {
    #     'status': 200,
    #     'transaction': 'Successful'
    # }


# Delete Request (Todo Project)
# Delete
@app.delete("/{todo_id}")
async def delete_todo(todo_id: int,
                      # user가 그 Postman 용도로 추가된 것임.
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    # if 여기도 Postman 용도로 추가된 것임.
    if user is None:
        raise get_user_exception()
    todo_model = db.query(models.Todos)\
        .filter(models.Todos.id == todo_id)\
        .filter(models.Todos.owner_id == user.get('id'))\
        .first()
    # 여기서 2번째 줄인 filter(models.Todos.owner_id == user.get('id))는 Postman 용도로 추가된 것임.

    if todo_model is None:
        raise http_exception()

    db.query(models.Todos)\
        .filter(models.Todos.id == todo_id)\
        .delete()

    db.commit()

    successful_response(200)
    # return {
    #     'status': 201,
    #     'transaction': 'Successful'
    # }


def successful_response(status_code: int):
    return {
        'status': status_code,
        'transaction': 'Successful'
    }


def http_exception():
    return HTTPException(status_code=404, detail="Todo not found")
