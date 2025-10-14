Sentimental Analysis:
# --- SENTIMENT ANALYSIS WITH NAIVE BAYES ---
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


# Load scraped reviews
df = pd.read_csv('bigbasket_reviews.csv')


# Label: Use rating as proxy (>=3 positive, else negative)
def get_sentiment(rating):
   try:
       return "positive" if float(rating) >= 3 else "negative"
   except:
       return "neutral"


df['sentiment'] = df['rating'].apply(get_sentiment)


# Prepare data
X = df['content'].astype(str)
y = df['sentiment']


# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Vectorize
vectorizer = CountVectorizer(stop_words='english', max_features=5000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)


# Train Naive Bayes
clf = MultinomialNB()
clf.fit(X_train_vec, y_train)


# Predict and save results
df['predicted_sentiment'] = clf.predict(vectorizer.transform(df['content'].astype(str)))
df.to_csv('sentiment_analysis_results.csv', index=False)
print("Sentiment analysis complete. Results saved to sentiment_analysis_results.csv")


# Download the file in Colab
from google.colab import files
files.download('sentiment_analysis_results.csv')


# ---Another part of  SENTIMENT ANALYSIS WITH NAIVE BAYES ---
!pip install pandas scikit-learn matplotlib


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.pipeline import make_pipeline


# Load your scraped data
from google.colab import files
uploaded = files.upload()


# Read CSV file
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
df['rating'] = df['rating'].str.extract('(\d+\.?\d*)').astype(float)


# Create sentiment labels
def get_sentiment(rating):
   if rating >= 4: return 'positive'
   elif rating <= 2: return 'negative'
   else: return 'neutral'


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
print(classification_report(y_test, y_pred))


# Confusion matrix visualization
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8,6))
plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
plt.title('Confusion Matrix')
plt.colorbar()
tick_marks = np.arange(2)
plt.xticks(tick_marks, ['negative', 'positive'])
plt.yticks(tick_marks, ['negative', 'positive'])
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()


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
