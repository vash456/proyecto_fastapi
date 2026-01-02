from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import func, select

from db import SessionDep
from models import Transaction, TransactionCreate, Customer


router = APIRouter()


@router.post(
    "/transactions", status_code=status.HTTP_201_CREATED, tags=["transactions"]
)
async def create_transaction(transaction_data: TransactionCreate, session: SessionDep):
    transaction_data_dict = transaction_data.model_dump()
    customer = session.get(Customer, transaction_data_dict.get("customer_id"))
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exist."
        )
    transaction_db = Transaction.model_validate(transaction_data_dict)
    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)
    return transaction_db


@router.get("/transactions", tags=["transactions"])
async def list_transactions(
    session: SessionDep,
    skip: int = Query(0, description="Registros a omitir"),
    limit: int = Query(10, description="Numero de registros"),
):
    query = select(Transaction).offset(skip).limit(limit)
    transactions = session.exec(query).all()
    total_items: int = session.exec(select(func.count(Transaction.id))).one()
    total_pages = (total_items + limit - 1) // limit
    items_in_page = len(transactions)
    page = (skip // limit) + 1
    return {
        "pagination": {
            "skip": skip,
            "limit": limit,
            "total_pages": total_pages,
            "total_items": total_items,
            "items_in_page": items_in_page,
            "page": page,
        },
        "data": transactions,
    }
