from sqlmodel import select
from fastapi import APIRouter, HTTPException, Query, status

from db import SessionDep
from models import (
    Customer,
    CustomerCreate,
    CustomerUpdate,
    Plan,
    CustomerPlan,
    StatusEnum,
)

router = APIRouter()


@router.post(
    "/customers",
    response_model=Customer,
    status_code=status.HTTP_201_CREATED,
    tags=["customers"],
)
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()  # genera la sentencia sql para guardar el modelo en la db
    session.refresh(customer)  # refrescamos la variable en memoria para que tenga el id
    # asumiendo como db
    # customer.id = len(db_customers)
    # db_customers.append(customer)
    return customer


@router.get("/customers", response_model=list[Customer], tags=["customers"])
async def list_customer(session: SessionDep):
    return session.exec(select(Customer)).all()
    # return db_customers


@router.get("/customers/{customer_id}", response_model=Customer, tags=["customers"])
async def get_customer(session: SessionDep, customer_id: int):
    # return session.exec(select(Customer).where(Customer.id == customer_id)).first()
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exist."
        )
    return customer_db


@router.patch(
    "/customers/{customer_id}",
    response_model=Customer,
    status_code=status.HTTP_201_CREATED,
    tags=["customers"],
)
async def update_customer(
    customer_id: int, customer_data: CustomerUpdate, session: SessionDep
):
    # return session.exec(select(Customer).where(Customer.id == customer_id)).first()
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exist."
        )
    customer_data_dict = customer_data.model_dump(exclude_unset=True)
    customer_db.sqlmodel_update(customer_data_dict)
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    return customer_db


@router.delete("/customers/{customer_id}", response_model=Customer, tags=["customers"])
async def delete_customer(session: SessionDep, customer_id: int):
    # return session.exec(select(Customer).where(Customer.id == customer_id)).first()
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exist."
        )
    session.delete(customer_db)
    session.commit()
    return {"detail": "ok"}


@router.post("/customers/{customer_id}/plans/{plan_id}", tags=["customers"])
async def subscribe_customer_to_plan(
    customer_id: int,
    plan_id: int,
    session: SessionDep,
    plan_status: StatusEnum = Query(),
):
    customer_db = session.get(Customer, customer_id)
    plan_db = session.get(Plan, plan_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exists."
        )
    if not plan_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Plan doesn't exists."
        )
    customer_plan_db = CustomerPlan(
        plan_id=plan_db.id, customer_id=customer_db.id, status=plan_status
    )
    session.add(customer_plan_db)
    session.commit()
    session.refresh(customer_plan_db)
    return customer_plan_db


@router.get("/customers/{customer_id}/plans", tags=["customers"])
async def list_plans_customer(
    customer_id: int, session: SessionDep, plan_status: StatusEnum = Query()
):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    query = (
        select(CustomerPlan)
        .where(CustomerPlan.customer_id == customer_id)
        .where(CustomerPlan.status == plan_status)
    )
    plans = session.exec(query).all()
    return plans
