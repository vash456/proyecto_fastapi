from fastapi import status
from sqlmodel import select

from models import Customer, CustomerPlan, StatusEnum

cliente = {"name": "Jhon Doe", "email": "jhon@example.com", "age": 33}
plan = {"name": "Basic", "price": 12, "descripcion": "Plan básico límitado."}


def test_create_customer(client):
    response = client.post(
        "/customers", json={"name": "jhon Doe", "email": "jhon@example.com", "age": 33}
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_get_customer(client):
    response = client.post(
        "/customers", json={"name": "jhon Doe", "email": "jhon@example.com", "age": 33}
    )
    assert response.status_code == status.HTTP_201_CREATED
    customer_id: int = response.json()["id"]
    response_read = client.get(f"/customers/{customer_id}")
    assert response_read.status_code == status.HTTP_200_OK
    assert response_read.json()["name"] == "jhon Doe"


def test_list_customers(client):
    response = client.post(
        "/customers",
        json=cliente,
    )
    response = client.get("/customers")
    assert response != None
    assert response != []
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)  # Verifica que el contenido sea una lista
    assert len(response.json()) > 0  # Verifica que la lista tenga al menos un elemento


def test_update_customer(client, session):
    response = client.post(
        "/customers",
        json=cliente,
    )
    assert response.status_code == status.HTTP_201_CREATED
    customer_id = response.json()["id"]
    response_up = client.patch(f"/customers/{customer_id}", json={"name": "Jhon Snow"})
    assert response_up.status_code == status.HTTP_201_CREATED
    created_customer = session.exec(
        select(Customer).where(Customer.name == "Jhon Snow")
    ).first()
    assert (
        response_up.json()["name"] == created_customer.name
    )  # este valida en la base de datos
    assert response_up.json()["name"] == "Jhon Snow"  # este valida en el endpoint


def test_delete_customer(client, session):
    response = client.post(
        "/customers",
        json=cliente,
    )
    assert response.status_code == status.HTTP_201_CREATED
    customer_id = response.json()["id"]
    response_delete = client.delete(f"/customers/{customer_id}")
    assert response_delete.status_code == status.HTTP_200_OK
    deleted_customer = session.get(
        Customer, customer_id
    )  # consultamos el customer con el ID en la base de datos
    assert deleted_customer is None  # verificamos que la consulta sea None


def test_suscribe_customer_to_plan(client, session):
    response_customer = client.post(
        "/customers",
        json=cliente,
    )
    customer_id = response_customer.json()["id"]
    response_plan = client.post(
        "/plans",
        json=plan,
    )
    plan_id = response_plan.json()["id"]
    assert response_customer.status_code == status.HTTP_201_CREATED
    assert response_plan.status_code == status.HTTP_201_CREATED

    response_suscribe = client.post(
        f"/customers/{customer_id}/plans/{plan_id}",
        params={"plan_status": StatusEnum.ACTIVE.value},
    )
    assert response_suscribe.status_code == status.HTTP_201_CREATED

    created_subscription = session.exec(
        select(CustomerPlan).where(CustomerPlan.customer_id == customer_id)
    ).first()
    assert created_subscription is not None
    assert created_subscription.customer_id == customer_id
    assert created_subscription.plan_id == plan_id


def test_list_customer_subscriptions(client, session):
    response_customer = client.post(
        "/customers",
        json=cliente,
    )
    customer_id = response_customer.json()["id"]

    response_plan = client.post(
        "/plans",
        json=plan,
    )
    plan_id = response_plan.json()["id"]

    assert response_customer.status_code == status.HTTP_201_CREATED
    assert response_plan.status_code == status.HTTP_201_CREATED

    response_suscribe = client.post(
        f"/customers/{customer_id}/plans/{plan_id}",
        params={"plan_status": StatusEnum.ACTIVE.value},
    )
    assert response_suscribe.status_code == status.HTTP_201_CREATED

    response_list_customer_subscriptions = client.get(
        f"/customers/{customer_id}/plans",
        params={"plan_status": StatusEnum.ACTIVE.value},
    )
    assert response_list_customer_subscriptions != None
    assert response_list_customer_subscriptions != []
    assert response_list_customer_subscriptions.status_code == status.HTTP_200_OK
    assert isinstance(
        response_list_customer_subscriptions.json(), list
    )  # Verifica que el contenido sea una lista
    assert (
        len(response_list_customer_subscriptions.json()) > 0
    )  # Verifica que la lista tenga al menos un elemento
