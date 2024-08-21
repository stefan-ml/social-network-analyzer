from typing import Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
import numpy as np
import pandas as pd
import json
from flask import Flask, jsonify, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing import sequence
import sys
sys.path.append('../')
from tokenizer import tokenization
from processing import processing
import lime
import lime.lime_text
import warnings

warnings.filterwarnings("ignore")

app = FastAPI()

# Dodavanje CORS middleware-a kako bi omogućili zahteve sa svih domena
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Dozvoljava sve izvore
    allow_credentials=True,
    allow_methods=["*"],  # Dozvoljava sve HTTP metode
    allow_headers=["*"],  # Dozvoljava sve HTTP zaglavlja
)

html_path = '../frontend/lime_explanation_single_tweet.html'

# Učitavanje NN modela
model = load_model('../model/nn_model.h5')
print('Model loaded!')

# Maksimalna dužina sekvence
max_len = 500

# Učitavanje tokenizer-a i skupa podataka
tok = tokenization.getTokenizer('../tokenizer/tokenizer.pkl')
X = pd.read_csv('../dataset/datasetX.csv', encoding="ISO-8859-1", engine="python")
X.columns = ["label", "time", "date", "query", "username", "text"]
X = X.iloc[:int(10000)] 
X = X['text']

# Model za zahtev za predikciju sentimenta
class SentimentRequest(BaseModel):
    text: str

def predict_sentiment(data):
    # Pretvaranje teksta u sekvence brojeva
    sequences = tok.texts_to_sequences(data)
    # Dopunjava sequence kako bi se uskladile sa maksimalnom dužinom
    sequences_matrix = sequence.pad_sequences(sequences, maxlen=max_len)
    # Predviđanje sentimenta koristeći NN model
    predictions = model.predict(sequences_matrix)
    if predictions.shape[1] == 1:
        # Ako je model binaran, dodaj kolonu za negativne predikcije
        predictions = np.hstack([1 - predictions, predictions])
    return predictions

# Definisanje root endpoint-a
@app.get("/")
def read_root():
    return {"Hello": "World"}

# Definisanje endpoint-a za predikciju
@app.post("/predict/")
def get_prediction(request: SentimentRequest):
    try:
        # Uzimanje i obrada teksta za objašnjenje
        text_to_explain = [request.text]
        print(text_to_explain)
        df = pd.DataFrame({'text': text_to_explain})
        df = processing.applyPreprocessing(df)  # Obrada teksta
        texts_array = df['text'].tolist()
        
        text_to_explain = [' '.join(texts_array[0])] 

        # XAI LIME explainer
        explainer = lime.lime_text.LimeTextExplainer(class_names=['negative', 'positive'])
        # Objašnjavanje predikcije NN modela
        exp = explainer.explain_instance(text_to_explain[0], predict_sentiment, num_features=10)
        exp.save_to_file(html_path)
         
        explanation = exp.as_list()

        # Izračunavanje ukupnog rezultata sentimenta
        total_score = sum(score for word, score in explanation)
        general_sentiment_label = "positive" if total_score >= 0 else "negative"

        explanation_data = {
            "general_sentiment": {
                "score": total_score,
                "label": general_sentiment_label
            },
            "words": []
        }

        for word, score in explanation:
            explanation_data["words"].append({
                "word": word,
                "score": score,
                "label": "positive" if score > 0 else "negative"
            })

        explanation_json = json.dumps(explanation_data)
 
        result = {
            "text": texts_array[0],
            "explanation_json": explanation_json,
            "lime_explanation": html_path
        }

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint za dobijanje nasumičnog tvita
@app.get("/get_random_tweet/")
def explain_samples():
    try:
        # Izbor nasumičnog tvita iz skupa podataka
        sample_indices = np.random.choice(len(X), size=1, replace=False)
        
        result = {
            "tweet": X[sample_indices[0]],
        }

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
