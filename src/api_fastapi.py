from fastapi import FastAPI
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
    category: str

BENTO_URL = "http://bentoml:3000/predict"

# Connexion PostgreSQL (ajuste selon ton docker-compose)
DB_CONFIG = {
    "host": "db",
    "database": "mydatabase",
    "user": "myuser",
    "password": "mypassword",
    "port": 5432,
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)

@app.post("/predict")
def predict(item: Item):
    response = requests.post(BENTO_URL, json={"text": item.text})
    if response.status_code == 200:
        return response.json()
    return {"error": "Erreur lors de la prédiction"}

@app.post("/add_product")
def add_product(product: Product):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Créer la table si elle n’existe pas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                description TEXT NOT NULL,
                category TEXT NOT NULL
            )
        """)
        conn.commit()

        # Insérer le produit
        cursor.execute("""
            INSERT INTO products (description, category)
            VALUES (%s, %s)
            RETURNING id
        """, (product.text, product.category))
        new_id = cursor.fetchone()["id"]
        conn.commit()

        cursor.close()
        conn.close()

        return {"id": new_id, "description": product.text, "category": product.category}
    except Exception as e:
        return {"error": str(e)}
