# app/sentiment.py

import pickle

model = pickle.load(open("sentiment_model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

def predict_sentiment(text):
    vec = vectorizer.transform([text])
    probs = model.predict_proba(vec)[0]

    return {
        "positive": float(probs[1]),
        "negative": float(probs[0]),
        "label": "POSITIVE" if probs[1] > probs[0] else "NEGATIVE"
    }