import time
import csv
import requests
import os

CSV_FILE = "tests/simulate_add_products.csv"
FASTAPI_URL = "http://localhost:8000"
API_KEY = os.getenv("API_KEY", "mysecretkey")
HEADERS = {"X-API-Key": API_KEY}

with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=",")
    for row in reader:
        description = row["description"]
        predicted_category = row["predicted_category"]
        selected_category = row["selected_category"]

        payload = {
            "text": description,
            "predicted_category": predicted_category,
            "selected_category": selected_category
        }

        try:
            response = requests.post(
                f"{FASTAPI_URL}/add_product", 
                json=payload,
                headers=HEADERS
            )
            print(f"[AJOUTÉ] {response.json()}")
        except Exception as e:
            print(f"[ERREUR] {e}")

        time.sleep(0.1)
