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

def table_exists(cursor, table_name):
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = %s
        );
    """, (table_name,))
    return cursor.fetchone()[0]

def compute_drift():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Vérifier si la table existe
        if not table_exists(cursor, 'products'):
            print("[INFO] La table 'products' n'existe pas encore")
            category_drift.set(0)
            cursor.close()
            conn.close()
            return

        # Si la table existe, exécuter les requêtes
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
