from typing import Annotated

from fastapi import Depends, FastAPI
from sqlmodel import Session, create_engine, SQLModel
from app.core.config import settings

# sqlite_name = "db.sqlite3"
# sqlite_url = f"sqlite:///{sqlite_name}"

engine = create_engine(settings.DATABASE_URL,echo=settings.DEBUG)


def create_all_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
