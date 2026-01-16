from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.core.security import (
    verify_password,
    create_access_token,
)
from db import engine
from app.models.user import User
from app.schemas.auth import Token

router = APIRouter(prefix="/auth", tags=["Auth"])


def authenticate_user(session: Session, username: str, password: str) -> User | None:
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()

    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None

    return user


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    with Session(engine) as session:
        user = authenticate_user(session, form_data.username, form_data.password)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )

        access_token = create_access_token(
            data={"sub": user.username, "role": user.role}
        )

        return {"access_token": access_token, "token_type": "bearer"}
