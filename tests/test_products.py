import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def sample_laptop():
    return {
        "name": "Laptop HP ProBook 450",
        "description": "Business laptop, 16GB RAM, 512GB SSD, Intel i7",
        "price": 4500.00,
        "stock": 15,
        "category": "electronics",
        "is_active": True,
    }


@pytest.fixture
def sample_tshirt():
    return {
        "name": "Cotton T-shirt Basic",
        "description": "100% cotton, unisex, various sizes",
        "price": 49.99,
        "stock": 100,
        "category": "clothing",
        "is_active": True,
    }


@pytest.fixture
def created_product(client, sample_laptop):
    response = client.post("/products/", json=sample_laptop)
    laptop = response.json()
    product_id = laptop["id"]
    yield laptop
    client.delete(f"/products/{product_id}/")


@pytest.fixture
def created_tshirt(client, sample_tshirt):
    response = client.post("/products/", json=sample_tshirt)
    tshirt = response.json()
    tshirt_id = tshirt["id"]
    yield tshirt
    client.delete(f"/products/{tshirt_id}/")


def test_update_product(client, created_product):
    product_id = created_product["id"]
    update_data = {"description": "lorem ipsum"}

    response = client.patch(f"/products/{product_id}/", json=update_data)

    assert response.status_code == 200

    data = response.json()
    assert data["description"] == "lorem ipsum"

    assert data["name"] == created_product["name"]
    assert data["price"] == created_product["price"]
    assert data["stock"] == created_product["stock"]
    assert data["category"] == created_product["category"]


def test_update_product_multiple_fields(client, created_tshirt):
    product_id = created_tshirt["id"]
    update_data = {"name": "Tommy Jeans tshirt", "stock": 31}

    response = client.patch(f"/products/{product_id}/", json=update_data)

    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Tommy Jeans tshirt"
    assert data["stock"] == 31

    assert data["description"] == created_tshirt["description"]
    assert data["price"] == created_tshirt["price"]
    assert data["category"] == created_tshirt["category"]


def test_delete_product(client, created_product):
    product_id = created_product["id"]
    response = client.delete(f"/products/{product_id}/")
    assert response.status_code == 204

    response = client.get(f"/products/{product_id}/")
    assert response.status_code == 404


def test_update_nonexistent_product(client):
    response = client.patch("/products/999999/", json={"stock": 0})
    assert response.status_code == 404
