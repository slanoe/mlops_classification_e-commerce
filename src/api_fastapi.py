from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel
import requests
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = FastAPI()

class Item(BaseModel):
    text: str

class Product(BaseModel):
    text: str
    predicted_category: str
    selected_category: str

BENTO_URL = "http://bentoml:3000/predict"

# Connexion PostgreSQL (ajuste selon ton docker-compose)
DB_CONFIG = {
    "host": "db",
    "database": "mydatabase",
    "user": "myuser",
    "password": "mypassword",
    "port": 5432,
}

API_KEY = os.getenv("API_KEY")

def get_connection():
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.post("/predict")
def predict(item: Item, authorized: None = Depends(verify_api_key)):
    response = requests.post(BENTO_URL, json={"text": item.text})
    if response.status_code == 200:
        return response.json()
    return {"error": "Erreur lors de la prédiction"}

@app.post("/add_product")
def add_product(product: Product, authorized: None = Depends(verify_api_key)):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Créer la table si elle n’existe pas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                description TEXT NOT NULL,
                predicted_category TEXT NOT NULL,
                selected_category TEXT NOT NULL
            )
        """)
        conn.commit()

        # Insérer le produit
        cursor.execute("""
            INSERT INTO products (description, predicted_category, selected_category)
            VALUES (%s, %s, %s)
            RETURNING id
        """, (product.text, product.predicted_category, product.selected_category))
        new_id = cursor.fetchone()["id"]
        conn.commit()

        cursor.close()
        conn.close()

        return {"id": new_id, "description": product.text, "predicted_category": product.predicted_category, "selected_category": product.selected_category}
    except Exception as e:
        return {"error": str(e)}
