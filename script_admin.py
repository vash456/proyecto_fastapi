from sqlmodel import Session
from db import engine
from app.models.user import User
from app.core.security import hash_password

with Session(engine) as session:
    user = User(
        username="admin",
        hashed_password=hash_password("admin123"),
        role="admin"
    )
    session.add(user)
    session.commit()
