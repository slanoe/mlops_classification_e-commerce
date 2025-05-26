import requests

def test_add_product_predict_category():
    url = "http://localhost:8000/add_product"
    payload = {"text": "Balancoire pour jardin extérieur"}
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_category" in data
    assert str(data["predicted_category"]) == "2582"
