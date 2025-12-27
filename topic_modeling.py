#!/usr/bin/env python3
"""Topic Modeling Script for BigBasket Reviews using BERTopic"""

import pandas as pd
from bertopic import BERTopic
from umap import UMAP
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt

# Load your data
# Try to load the sentiment analysis results, or fall back to raw reviews
import os
if os.path.exists('sentiment_analysis_results.csv'):
    df = pd.read_csv('sentiment_analysis_results.csv')
elif os.path.exists('bigbasket_sentiment_analysis.csv'):
    df = pd.read_csv('bigbasket_sentiment_analysis.csv')
elif os.path.exists('bigbasket_reviews.csv'):
    df = pd.read_csv('bigbasket_reviews.csv')
else:
    raise FileNotFoundError("No data file found. Please run sentiment_analysis.py first or provide bigbasket_reviews.csv")

# Preprocess text
def clean_text(text):
    text = str(text).lower()
    text = text.replace('flag this review', '')
    text = text.replace('irrelevantfakejunk', '')
    text = text.replace('thank you! we appreciate your effort.', '')
    return text.strip()

df['clean_content'] = df['content'].apply(clean_text)

# Prepare documents list
docs = df['clean_content'].tolist()

# Initialize BERTopic with custom parameters
umap_model = UMAP(n_neighbors=15, n_components=5, min_dist=0.0, random_state=42)
vectorizer_model = CountVectorizer(stop_words="english", ngram_range=(1, 2))

topic_model = BERTopic(
    language="english",
    umap_model=umap_model,
    vectorizer_model=vectorizer_model,
    min_topic_size=25,
    nr_topics="auto"
)

# Fit the model
print("Fitting BERTopic model...")
topics, probs = topic_model.fit_transform(docs)

# Get topic information
topic_info = topic_model.get_topic_info()
print("\nTopic Information:")
print(topic_info.head(10))

# Visualize topics
fig = topic_model.visualize_barchart(top_n_topics=10, n_words=10)
fig.write_html("topic_barchart.html")
print("\nTopic barchart saved to topic_barchart.html")

# Visualize document clustering
fig = topic_model.visualize_documents(docs, hide_annotations=True)
fig.write_html("document_clustering.html")
print("Document clustering visualization saved to document_clustering.html")

# Save model
topic_model.save("bigbasket_bertopic_model")
print("Model saved to bigbasket_bertopic_model")

# Save results to CSV
df['topic'] = topics
df.to_csv('bigbasket_topics.csv', index=False)
print("Results saved to bigbasket_topics.csv")

# Analyze topics
unique_topics = sorted(df['topic'].unique())
print("\nAll topics found in the data:", unique_topics)

print("\nNumber of reviews per topic:")
print(df['topic'].value_counts().sort_index())

for topic in unique_topics:
    print(f"\n--- Topic {topic} ---")
    topic_reviews = df[df['topic'] == topic]['content'].head(3)
    for i, review in enumerate(topic_reviews, 1):
        print(f"Example {i}: {review[:300]}")
