from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
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
    
    # Sauvegarder les nouvelles données dans un dossier partagé
    output_path = '/opt/airflow/data/raw/additional_data.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    return output_path

def split_additional_data(**context):
    """Séparer les données additionnelles en X et y"""
    df = pd.read_csv('/opt/airflow/data/raw/additional_data.csv')
    
    X = df[['description']]
    y = df[['selected_category']]
    y = y.rename(columns={'selected_category': 'prdtypecode'})
    
    X.to_csv('/opt/airflow/data/preprocessed/X_train_additional_data.csv', index=True)
    y.to_csv('/opt/airflow/data/preprocessed/Y_train_additional_data.csv', index=True)
    
    return {
        'x_path': '/opt/airflow/data/preprocessed/X_train_additional_data.csv',
        'y_path': '/opt/airflow/data/preprocessed/Y_train_additional_data.csv'
    }

with DAG(
    dag_id='classification_ecommerce_rakuten',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    description='Classification de produits e-commerce Rakuten',
) as dag:

    extract_data = PythonOperator(
        task_id='extract_postgres_data',
        python_callable=extract_from_postgres,
    )

    split_data = PythonOperator(
        task_id='split_additional_data',
        python_callable=split_additional_data,
    )

    extract_data >> split_data
