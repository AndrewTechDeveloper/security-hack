from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session

user_name = "root"
password = "password"
host = "db"
database_name = "security_hack_development"

DATABASE = f'mysql://{user_name}:{password}@{host}/{database_name}'

engine = create_engine(
    DATABASE,
    encoding="utf-8",
    echo=True
)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(30), nullable=False)
    email = Column(String(30), unique=True, index=True)
    hashed_password = Column(String(200), nullable=False)
    todos = relationship("Todo", back_populates="user")


class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(30), nullable=False)
    content = Column(String(300), nullable=False)
    done = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="todos")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def main():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    main()
