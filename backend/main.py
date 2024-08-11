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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, you can restrict this to specific domains
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

html_path = '../frontend/lime_explanation_single_tweet.html'
model = load_model('../model/nn_model.h5')
print('Model loaded!')

max_len = 500

tok = tokenization.getTokenizer( '../tokenizer/tokenizer.pkl')
X = pd.read_csv('../dataset/datasetX.csv', encoding = "ISO-8859-1", engine="python")
X.columns = ["label", "time", "date", "query", "username", "text"]
X = X.iloc[:int(10000)]
X = X['text']


class SentimentRequest(BaseModel):
    text: str

def predict_sentiment(data):
    sequences = tok.texts_to_sequences(data)
    sequences_matrix = sequence.pad_sequences(sequences, maxlen=max_len)
    predictions = model.predict(sequences_matrix)
    if predictions.shape[1] == 1:
        predictions = np.hstack([1 - predictions, predictions])
    return predictions

# Define the root endpoint
@app.get("/")
def read_root():
    return {"Hello": "World"}

# Define the prediction endpoint
@app.post("/predict/")
def get_prediction(request: SentimentRequest):
    try:
        text_to_explain = [request.text]
        print(text_to_explain)
        df = pd.DataFrame({'text': text_to_explain})
        df = processing.applyPreprocessing(df)
        texts_array = df['text'].tolist()
        
        text_to_explain = [' '.join(texts_array[0])] 

        #pred = predict_sentiment(text_to_explain[0])

        explainer = lime.lime_text.LimeTextExplainer(class_names=['negative', 'positive'])
        exp = explainer.explain_instance(text_to_explain[0], predict_sentiment, num_features=20)
        exp.save_to_file(html_path)
         
        explanation = exp.as_list()

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

# Endpoint to get random tweet
@app.get("/get_random_tweet/")
def explain_samples():
    try:
        #np.random.seed(42)
        sample_indices = np.random.choice(len(X), size=1, replace=False)
        
        result = {
            "tweet": X[sample_indices[0]],
        }

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))