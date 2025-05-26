import bentoml
from bentoml.io import JSON
from src.predict import Predict
from tensorflow import keras
import json

with open("models/tokenizer_config.json", "r", encoding="utf-8") as json_file:
    tokenizer_config = json_file.read()
tokenizer = keras.preprocessing.text.tokenizer_from_json(tokenizer_config)

lstm = keras.models.load_model("models/best_lstm_model.h5")
vgg16 = keras.models.load_model("models/best_vgg16_model.h5")

with open("models/best_weights.json", "r") as json_file:
    best_weights = json.load(json_file)

with open("models/mapper.json", "r") as json_file:
    mapper = json.load(json_file)

dummy_csv = "data/preprocessed/X_train_update.csv"
dummy_img_dir = "data/preprocessed/image_train"

predictor = Predict(
    tokenizer=tokenizer,
    lstm=lstm,
    vgg16=vgg16,
    best_weights=best_weights,
    mapper=mapper,
    filepath=dummy_csv,
    imagepath=dummy_img_dir,
)

svc = bentoml.Service("cat_model_service")

@svc.api(input=JSON(), output=JSON())
def predict(data):
    text = data["text"]
    import pandas as pd
    df = pd.DataFrame([{"description": text, "image_path": None}])
    from features.build_features import TextPreprocessor
    text_preprocessor = TextPreprocessor()
    text_preprocessor.preprocess_text_in_df(df, columns=["description"])
    sequences = predictor.tokenizer.texts_to_sequences(df["description"])
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    padded_sequences = pad_sequences(
        sequences, maxlen=10, padding="post", truncating="post"
    )
    lstm_proba = predictor.lstm.predict([padded_sequences])
    import numpy as np
    vgg16_proba = np.zeros_like(lstm_proba)
    concatenate_proba = (
        predictor.best_weights[0] * lstm_proba + predictor.best_weights[1] * vgg16_proba
    )
    final_prediction = np.argmax(concatenate_proba, axis=1)[0]
    category = predictor.mapper[str(final_prediction)]
    return {"category": category}
