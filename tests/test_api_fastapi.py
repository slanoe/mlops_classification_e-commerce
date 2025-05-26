import requests

def test_add_product_predict_category():
    url = "http://localhost:8000/add_product"
    payload = {
        "text": "Balancoire pour jardin extérieur",
        "category": "2582"
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "category" in data
    assert str(data["category"]) == "2582"
