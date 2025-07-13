import requests

def test_predict_balancoire():
    url = "http://localhost:3000/predict"
    payload = {"text": "Balancoire pour jardin exterieur"}
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "category" in data
    assert str(data["category"]) == "1302"
