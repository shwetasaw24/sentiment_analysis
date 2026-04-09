import pickle

model = pickle.load(open("sentiment_model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

def predict_sentiment(text):
    vec = vectorizer.transform([text])
    probs = model.predict_proba(vec)[0]

    negative = float(probs[0])
    positive = float(probs[1])

    return {
        "negative": negative,
        "positive": positive,
        "label": "POSITIVE" if positive > negative else "NEGATIVE"
    }