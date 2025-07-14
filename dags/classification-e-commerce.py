from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
import os
import pandas as pd
import psycopg2

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 7, 1),
    'retries': 1,
}

def extract_from_postgres(**context):
    """Extraire les données de PostgreSQL et les sauvegarder au format CSV"""
    db_params = {
        "host": "db",
        "database": "mydatabase",
        "user": "myuser",
        "password": "mypassword",
    }
    
    # Connexion à PostgreSQL et extraction des données
    conn = psycopg2.connect(**db_params)
    query = "SELECT description, selected_category FROM products"
    df = pd.read_sql(query, conn)
    conn.close()
    
    # Sauvegarder les nouvelles données
    output_path = 'additional_data.csv'
    df.to_csv(output_path, index=False)
    return output_path

with DAG(
    dag_id='classification_ecommerce_rakuten',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    description='Classification de produits e-commerce Rakuten avec réentraînement',
) as dag:

    extract_data = PythonOperator(
        task_id='extract_postgres_data',
        python_callable=extract_from_postgres,
    )

    extract_data
