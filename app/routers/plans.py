from fastapi import APIRouter, status, Depends
from sqlmodel import select

from models import Plan
from db import SessionDep
from app.core.roles import require_admin
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


@router.post(
    "/plans",
    status_code=status.HTTP_201_CREATED,
    tags=["plans"],
)
async def create_plan(plan_data: Plan, session: SessionDep, current_user: User = Depends(require_admin)):
    plan_db = Plan.model_validate(plan_data.model_dump())
    session.add(plan_db)
    session.commit()
    session.refresh(plan_db)
    return plan_db


@router.get(
    "/plans", response_model=list[Plan], status_code=status.HTTP_200_OK, tags=["plans"]
)
async def list_plans(session: SessionDep, current_user: User = Depends(get_current_user)):
    return session.exec(select(Plan)).all()
