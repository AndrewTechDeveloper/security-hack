from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from starlette.requests import Request
from pydantic import BaseModel
from db import Todo, engine, get_db

router = APIRouter()


class TodoCreate(BaseModel):
    user_id: int
    title: str
    content: str
    done: bool


class TodoUpdate(BaseModel):
    title: str
    content: str
    done: bool


@router.get("/")
def read_todos(db: Session = Depends(get_db)):
    todos = db.query(Todo).all()
    return todos


@router.get("/{todo_id}")
def read_todo_by_todo_id(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    return todo


@router.get("/user/{user_id}")
def read_todos_by_user_id(user_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == user_id).first()
    return todo


@router.post("/")
async def create_todo(todo: TodoCreate,  db: Session = Depends(get_db)):
    db_todo = Todo(user_id=todo.user_id, title=todo.title,
                   content=todo.content, done=todo.done)
    db.add(db_todo)
    db.commit()


@router.put("/{todo_id}")
async def update_todo(todo_id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    db_todo.title = todo.title
    db_todo.done = todo.done
    db.commit()


@router.delete("/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    db.delete(db_todo)
    db.commit()
