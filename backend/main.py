from flask import Flask, request, jsonify
from flask_cors import CORS
from collections import defaultdict

from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax

import pandas as pd
import re
import csv
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})  # Allow CORS for /api/* routes and localhost:3000 origin

# Dummy data
dummy_data = [
    {"id": 1, "name": "Item 1"},
    {"id": 2, "name": "Item 2"},
    {"id": 3, "name": "Item 3"}
]


@app.route('/api/data', methods=["POST"])
def add_one():
    data = request.json
    comment = data.get('comment')
    result = get_score(comment)

    negative_score = str(result["Negative"])
    positive_score = str(result["Positive"])
    neutral_score = str(result["Neutral"])
    # print(result)
    # if result is None:
    #     return jsonify({'error': 'Missing number'}), 400

    return jsonify({"Negative": negative_score, "Positive": positive_score, "Neutral": neutral_score})


roberta = "cardiffnlp/twitter-roberta-base-sentiment"
model = AutoModelForSequenceClassification.from_pretrained(roberta)
tokenizer = AutoTokenizer.from_pretrained(roberta)

def get_score(comment):
    comment_words = []

    for word in comment.split(' '):
        if word.startswith('@') and len(word) > 1:
            word = '@user'
        
        elif word.startswith('http'):
            word = "http"
        comment_words.append(word)

    tweet_proc = " ".join(comment_words)

    labels = ['Negative', 'Neutral', 'Positive']

    # sentiment analysis
    encoded_tweet = tokenizer(tweet_proc, return_tensors='pt')
    # output = model(encoded_tweet['input_ids'], encoded_tweet['attention_mask'])
    output = model(**encoded_tweet)

    scores = output[0][0].detach().numpy()
    scores = softmax(scores)

    scores_dict = defaultdict(float)
    for i in range(len(scores)):
        l = labels[i]
        s = scores[i]

        scores_dict[l] = s

    return scores_dict


df = pd.read_csv("suicide-messages.csv")

def get_answer():
    # Iterate through each row in the 'text' column and apply the cleaning function
    df["cleaned_text"] = df["text"].apply(clean_text)

    # Split the dataset into features (X) and target labels (y)
    X = df["text"]
    y = df["class"]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Create a CountVectorizer to convert text into numerical features (bag-of-words)
    vectorizer = CountVectorizer()
    X_train_vectorized = vectorizer.fit_transform(X_train)
    X_test_vectorized = vectorizer.transform(X_test)

    # Initialize and train the Support Vector Machine classifier
    svm_classifier = SVC(kernel="linear")
    svm_classifier.fit(X_train_vectorized, y_train)

    # Predict labels for the test set
    y_pred = svm_classifier.predict(X_test_vectorized)

    # Evaluate the model's performance
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)
    print(classification_report(y_test, y_pred))

    # Display the cleaned text
    # print(df[['text', 'cleaned_text']])

    # Display first few rows of dataset

def clean_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove numbers, punctuation, and special characters
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text


if __name__ == '__main__':
    app.run(port=5000)  # Running on port 5000

