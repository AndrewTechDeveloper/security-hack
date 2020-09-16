from fastapi import FastAPI, Header, HTTPException, Depends
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from sqlalchemy.orm import Session
from routers import users, todos
from db import engine, SessionLocal

app = FastAPI()


app.include_router(
    users.router,
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


app.include_router(
    todos.router,
    prefix="/todos",
    tags=["todos"],
    responses={404: {"description": "Not found"}},
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response
