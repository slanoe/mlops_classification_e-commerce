Classification de produits e-commerce Rakuten
==============================

Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources -> the external data you want to make a prediction on
    │   ├── preprocessed      <- The final, canonical data sets for modeling.
    |   |  ├── image_train <- Where you put the images of the train set
    |   |  ├── image_test <- Where you put the images of the predict set
    |   |  ├── X_train_update.csv    <- The csv file with te columns designation, description, productid, imageid like in X_train_update.csv
    |   |  ├── X_test_update.csv    <- The csv file with te columns designation, description, productid, imageid like in X_train_update.csv
    │   └── raw            <- The original, immutable data dump.
    |   |  ├── image_train <- Where you put the images of the train set
    |   |  ├── image_test <- Where you put the images of the predict set
    │
    ├── logs               <- Logs from training and predicting
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   ├── main.py        <- Scripts to train models 
    │   ├── predict.py     <- Scripts to use trained models to make prediction on the files put in ../data/preprocessed
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   ├── check_structure.py    
    │   │   ├── import_raw_data.py 
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models                
    │   │   └── train_model.py
    │   └── config         <- Describe the parameters used in train_model.py and predict_model.py

## Development

This project requires Python 3.10.

--------

> `sudo apt update && sudo apt install python3.10 python3.10-venv python3.10-dev && sudo apt install python3-virtualenv`      <- It will install Python 3.10 and virtualenv

> `virtualenv -p python3.10 .venv`      <- It will create a virtual environment named .venv

> `source .venv/bin/activate`  <- It will activate the virtual environment

> `pip install "setuptools<66"`      <- It will downgrade setuptools

> `pip install -r requirements.txt`      <- It will install the required packages

> `python src/predict.py`                <- It will use the trained models to make a prediction (of the prdtypecode) on the desired data, by default, it will predict on the train. You can pass the path to data and images as arguments if you want to change it
>
    Exemple : python src/predict.py --dataset_path "data/preprocessed/X_test_update.csv" --images_path "data/preprocessed/image_test"
                                        
                                         The predictions are saved in data/preprocessed as 'predictions.json'

> `python tests/simulate_add_products.py`  <- It will simulate the addition of products in the PostgreSQL database

> You can download the trained models loaded here : https://drive.google.com/drive/folders/1fjWd-NKTE-RZxYOOElrkTdOw2fGftf5M?usp=drive_link and insert them in the models folder


## Architecture diagram

> `docker run -it --rm -p 8081:8080 -d -v ./docs/:/usr/local/structurizr structurizr/lite`      <- It will run the structurizr on http://localhost:8081/


## Start the Services

To start all services (BentoML, FastAPI, Streamlit, PostgreSQL, Prometheus, Grafana):

> `docker compose up -d`      <- It will start all services in detached mode

Available endpoints:
- BentoML API: http://localhost:3000
- FastAPI: http://localhost:8000
- Streamlit UI: http://localhost:8501
- Grafana: http://localhost:3001

To stop all services:

> `docker compose down`


## Monitoring

The application includes monitoring capabilities:

> Prometheus is available at: http://localhost:9090/

> Grafana dashboard is available at: http://localhost:3001/d/fe484e94-dd3a-4b2c-9462-53c0f5cbe50e/drift?orgId=1&from=now-10m&to=now&timezone=browser&refresh=5s

The following metric is exposed from the PostgreSQL database:
- `product_category_drift`: Monitors the distribution of product categories to detect potential data drift



<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>