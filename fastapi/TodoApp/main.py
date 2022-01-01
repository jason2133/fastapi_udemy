from typing import Optional
from fastapi import FastAPI, Depends
from fastapi.exceptions import HTTPException
from database import SessionLocal
import models
from database import engine
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

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


@app.get("/todo/{todo_id}")
async def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos)\
        .filter(models.Todos.id == todo_id)\
        .first()
    if todo_model is not None:
        return todo_model
    # raise HTTPException(status_code=404, detail="Todo not found")
    raise http_exception()

# Post Request (Todo Project)
# Create


@app.post("/")
async def create_todo(todo: Todo, db: Session = Depends(get_db)):
    todo_model = models.Todos()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete

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
async def update_todo(todo_id: int, todo: Todo, db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos)\
        .filter(models.Todos.id == todo_id)\
        .first()
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
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos)\
        .filter(models.Todos.id == todo_id)\
        .first()

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
