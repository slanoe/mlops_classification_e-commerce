import requests
import os

API_KEY = os.getenv("API_KEY", "mysecretkey")
HEADERS = {"X-API-Key": API_KEY}

def test_add_product_predict_category():
    url = "http://localhost:8000/add_product"
    payload = {
        "text": "Balancoire pour jardin exterieur",
        "predicted_category": "1302",
        "selected_category": "1302"
    }
    response = requests.post(url, json=payload, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_category" in data
    assert data["predicted_category"] == "1302"
