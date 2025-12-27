#!/usr/bin/env python3
"""Sentiment Analysis Script for BigBasket Reviews"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.pipeline import make_pipeline

# Load your scraped data
df = pd.read_csv('bigbasket_reviews.csv')

# Data preprocessing
def preprocess_text(text):
    # Handle NaN values
    text = str(text).lower()

    # Remove unwanted patterns
    text = text.replace('flag this review', '')
    text = text.replace('irrelevantfakejunk', '')

    return text

# Apply preprocessing
df['clean_content'] = df['content'].apply(preprocess_text)

# Convert ratings to numerical values
# Handle both string and numeric ratings
if df['rating'].dtype == 'object':
    df['rating'] = df['rating'].str.extract('(\d+\.?\d*)').astype(float)
else:
    df['rating'] = df['rating'].astype(float)

# Create sentiment labels
def get_sentiment(rating):
    if rating >= 4:
        return 'positive'
    elif rating <= 2:
        return 'negative'
    else:
        return 'neutral'

df['sentiment'] = df['rating'].apply(get_sentiment)

# Remove neutral reviews for binary classification
df = df[df['sentiment'] != 'neutral']

# Split data
X = df['clean_content']
y = df['sentiment']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create pipeline with CountVectorizer and Naive Bayes
model = make_pipeline(
    CountVectorizer(stop_words='english', max_features=5000),
    MultinomialNB()
)

# Train model
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Confusion matrix visualization
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
plt.title('Confusion Matrix')
plt.colorbar()
tick_marks = np.arange(2)
plt.xticks(tick_marks, ['negative', 'positive'])
plt.yticks(tick_marks, ['negative', 'positive'])
plt.xlabel('Predicted')
plt.ylabel('True')
plt.savefig('confusion_matrix.png')
print("Confusion matrix saved to confusion_matrix.png")

# Predict on new text
test_reviews = [
    "Great service and fresh products!",
    "Worst experience, items were damaged",
    "Delivery was late but quality was good"
]

predictions = model.predict(test_reviews)
print("\nSample predictions:")
for text, pred in zip(test_reviews, predictions):
    print(f"{text} => {pred}")

# Save results
df['predicted_sentiment'] = model.predict(df['clean_content'])
df.to_csv('sentiment_analysis_results.csv', index=False)
print("\nSentiment analysis complete. Results saved to sentiment_analysis_results.csv")
