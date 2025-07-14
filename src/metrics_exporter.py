from prometheus_client import start_http_server, Gauge
import psycopg2
import time

DB_CONFIG = {
    "host": "db",
    "port": 5432,
    "database": "mydatabase",
    "user": "myuser",
    "password": "mypassword",
}

# Métrique Prometheus : % de mismatch entre predicted et selected
category_drift = Gauge("product_category_drift", "Taux de dérive entre catégorie prédite et sélectionnée")

def compute_drift():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM products")
        total = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*) FROM products 
            WHERE predicted_category != selected_category
        """)
        mismatches = cursor.fetchone()[0]

        drift = (mismatches / total) if total > 0 else 0
        category_drift.set(drift)

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"[ERREUR] {e}")
        category_drift.set(0)

if __name__ == "__main__":
    start_http_server(9100)
    print("Exporter Prometheus lancé sur le port 9100")

    while True:
        compute_drift()
        time.sleep(1)
