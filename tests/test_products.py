from fastapi.testclient import TestClient
from main import app 

client = TestClient(app)


def test_create_product():
    """POST /products"""
    response = client.post(
        "/products/",
        json={
            "name": "Laptop HP",
            "description": "Everyday homeuse (browsing, email, streaming)...",
            "price": 5000,
            "stock": 20,
            "category": "electronics",
            "is_active": True,
        },
    )

    assert response.status_code == 201
    data = response.json()

    assert data["name"] == "Laptop HP"
    assert data["description"] == "Everyday homeuse (browsing, email, streaming)..."
    assert data["price"] == '5000.00'
    assert data["stock"] == 20
    assert data["category"] == "electronics"
    assert data["is_active"] is True

    assert "id" in data
    assert "created_at" in data

def test_read_nonexistent_product():
    """GET /products/{id} -> returns 404 """
    response = client.get("/products/9999999/")

    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}