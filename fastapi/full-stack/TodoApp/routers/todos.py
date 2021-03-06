from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from .auth import get_current_user, get_user_exception
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models
from fastapi import Depends, HTTPException, APIRouter, Request
from typing import Optional
import sys
sys.path.append("..")


router = APIRouter(
    # 먼저 prefix로 /todos가 있기 때문에 우선적으로 todos를 들어가야 어떠한 페이지라도 나온다.
    prefix="/todos",
    tags=["todos"],
    responses={404: {"description": "Not found"}}
)

models.Base.metadata.create_all(bind=engine)

# HTML을 연결해준다. templates라는 폴더 안에 home.html이라는 HTML 파일이 있으므로
# directory='templates'라는 것을 이용해서 HTML을 서로 연결해준다.
templates = Jinja2Templates(directory='templates')


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get('/', response_class=HTMLResponse)
async def read_all_by_user(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})


@router.get('/add-todo', response_class=HTMLResponse)
async def add_new_todo(request: Request):
    return templates.TemplateResponse('add-todo.html', {'request': request})


@router.get('/edit-todo/{todo_id}', response_class=HTMLResponse)
async def edit_todo(request: Request):
    return templates.TemplateResponse('edit-todo.html', {'request': request})

# class Todo(BaseModel):
#     title: str
#     description: Optional[str]
#     priority: int = Field(
#         gt=0, lt=6, description="The priority must be between 1-5")
#     complete: bool


# @router.get('/test')
# async def test(request: Request):
#     # "home.html", {"request": request}는  context라고 불린다.
#     # return templates.TemplateResponse("home.html", {"request": request})
#     # return templates.TemplateResponse("add-todo.html", {"request": request})
#     # return templates.TemplateResponse("edit-todo.html", {"request": request})
#     # return templates.TemplateResponse("login.html", {"request": request})
#     return templates.TemplateResponse("register.html", {"request": request})


# @router.get("/")
# async def read_all(db: Session = Depends(get_db)):
#     return db.query(models.Todos).all()


# @router.get("/user")
# async def read_all_by_user(user: dict = Depends(get_current_user),
#                            db: Session = Depends(get_db)):
#     if user is None:
#         raise get_user_exception()
#     return db.query(models.Todos)\
#         .filter(models.Todos.owner_id == user.get("id"))\
#         .all()


# @router.get("/{todo_id}")
# async def read_todo(todo_id: int,
#                     user: dict = Depends(get_current_user),
#                     db: Session = Depends(get_db)):
#     if user is None:
#         raise get_user_exception()
#     todo_model = db.query(models.Todos)\
#         .filter(models.Todos.id == todo_id)\
#         .filter(models.Todos.owner_id == user.get("id"))\
#         .first()
#     if todo_model is not None:
#         return todo_model
#     raise http_exception()


# @router.post("/")
# async def create_todo(todo: Todo,
#                       user: dict = Depends(get_current_user),
#                       db: Session = Depends(get_db)):
#     if user is None:
#         raise get_user_exception()
#     todo_model = models.Todos()
#     todo_model.title = todo.title
#     todo_model.description = todo.description
#     todo_model.priority = todo.priority
#     todo_model.complete = todo.complete
#     todo_model.owner_id = user.get("id")

#     db.add(todo_model)
#     db.commit()

#     return successful_response(201)


# @router.put("/{todo_id}")
# async def update_todo(todo_id: int,
#                       todo: Todo,
#                       user: dict = Depends(get_current_user),
#                       db: Session = Depends(get_db)):
#     if user is None:
#         raise get_user_exception()

#     todo_model = db.query(models.Todos)\
#         .filter(models.Todos.id == todo_id)\
#         .filter(models.Todos.owner_id == user.get("id"))\
#         .first()

#     if todo_model is None:
#         raise http_exception()

#     todo_model.title = todo.title
#     todo_model.description = todo.description
#     todo_model.priority = todo.priority
#     todo_model.complete = todo.complete

#     db.add(todo_model)
#     db.commit()

#     return successful_response(200)


# @router.delete("/{todo_id}")
# async def delete_todo(todo_id: int,
#                       user: dict = Depends(get_current_user),
#                       db: Session = Depends(get_db)):
#     if user is None:
#         raise get_user_exception()

#     todo_model = db.query(models.Todos)\
#         .filter(models.Todos.id == todo_id)\
#         .filter(models.Todos.owner_id == user.get("id"))\
#         .first()

#     if todo_model is None:
#         raise http_exception()

#     db.query(models.Todos)\
#         .filter(models.Todos.id == todo_id)\
#         .delete()

#     db.commit()

#     return successful_response(200)


# def successful_response(status_code: int):
#     return {
#         'status': status_code,
#         'transaction': 'Successful'
#     }


# def http_exception():
#     return HTTPException(status_code=404, detail="Todo not found")
