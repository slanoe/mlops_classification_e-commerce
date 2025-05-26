from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

class Item(BaseModel):
    text: str

class Product(BaseModel):
    text: str
    category: str

BENTO_URL = "http://localhost:3000/predict"

@app.post("/predict")
def predict(item: Item):
    response = requests.post(BENTO_URL, json={"text": item.text})
    if response.status_code == 200:
        return response.json()
    return {"error": "Erreur lors de la prédiction"}

@app.post("/add_product")
def add_product(product: Product):
    # Ici, on pourrait ajouter le produit à une base de données, etc.
    return {"description": product.text, "category": product.category}
