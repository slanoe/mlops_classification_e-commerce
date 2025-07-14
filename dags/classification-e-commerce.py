from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data.make_dataset import main as prepare_main
from main import main as train_main

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 7, 1),
    'retries': 1,
}

with DAG(
    dag_id='classification_ecommerce_rakuten',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    description='Classification de produits e-commerce Rakuten',
) as dag:

    prepare = PythonOperator(
        task_id='prepare_data',
        python_callable=prepare_main,
        op_args=['data/raw', 'data/preprocessed'],
    )

    train = PythonOperator(
        task_id='train_model',
        python_callable=train_main,
    )

    prepare >> train
