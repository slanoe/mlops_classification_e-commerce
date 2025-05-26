from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

class Item(BaseModel):
    text: str

BENTO_URL = "http://localhost:3000/predict"

@app.post("/predict")
def predict(item: Item):
    response = requests.post(BENTO_URL, json={"text": item.text})
    if response.status_code == 200:
        return response.json()
    return {"error": "Erreur lors de la prédiction"}

@app.post("/add_product")
def add_product(item: Item):
    # Appel à BentoML pour obtenir la catégorie
    response = requests.post(BENTO_URL, json={"text": item.text})
    if response.status_code == 200:
        category = response.json().get("category")
        # Ici, on pourrait ajouter le produit à une base de données, etc.
        return {"description": item.text, "predicted_category": category}
    return {"error": "Erreur lors de l'ajout du produit"}
