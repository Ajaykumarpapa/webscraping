# Bigbasket Reviews - Web Scraping & NLP Analysis

A complete pipeline for scraping, analyzing, and extracting insights from Bigbasket product reviews on Mouthshut.com. Built for Google Colab.

## Project Overview

This project performs three main tasks:

1. **Web Scraping** - Collects product reviews from Mouthshut.com using Selenium and BeautifulSoup
2. **Sentiment Analysis** - Classifies reviews as positive/negative using Naive Bayes
3. **Topic Modeling** - Identifies key themes in reviews using BERTopic

## Data Flow

```
Mouthshut.com (Bigbasket Reviews)
        |
   [Web Scraping]
        |
  bigbasket_reviews.csv
        |
  [Sentiment Analysis]
        |
  sentiment_analysis_results.csv
        |
  [Topic Modeling]
        |
  bigbasket_topics.csv + Visualizations
```

## Files

| File | Description |
|------|-------------|
| `webscraping.txt` | Selenium-based scraper that extracts review titles, content, and ratings across 100 pages |
| `Sentimentalanalysis.txt` | Naive Bayes sentiment classifier with two implementations (basic and advanced) |
| `Topicmodeling.txt` | BERTopic-based topic extraction with UMAP dimensionality reduction and visualizations |

## Dependencies

### Web Scraping
- Selenium
- BeautifulSoup4
- Pandas
- chromedriver-autoinstaller

### Sentiment Analysis
- scikit-learn (CountVectorizer, MultinomialNB, Pipeline)
- Pandas
- Matplotlib

### Topic Modeling
- BERTopic
- sentence-transformers
- UMAP
- scikit-learn
- Matplotlib

## Usage

All scripts are designed to run in **Google Colab**. Open each `.txt` file and copy the code into a Colab notebook, or rename them to `.py` files.

### 1. Scrape Reviews

Run `webscraping.txt` to collect reviews. This will:
- Launch a headless Chrome browser
- Scrape 100 pages of reviews with random delays (6-10s) to avoid detection
- Save results to `bigbasket_reviews.csv`

### 2. Analyze Sentiment

Run `Sentimentalanalysis.txt` to classify reviews. Two approaches are included:
- **Basic**: Binary classification (positive/negative) based on rating threshold of 3
- **Advanced**: Includes text preprocessing, pipeline-based classification, confusion matrix, and sample predictions

Output: `sentiment_analysis_results.csv`

### 3. Extract Topics

Run `Topicmodeling.txt` to discover themes. This will:
- Clean review text
- Fit a BERTopic model with custom UMAP parameters
- Generate topic bar charts and document clustering visualizations
- Save the model and topic assignments to `bigbasket_topics.csv`

## Output Files

| File | Contents |
|------|----------|
| `bigbasket_reviews.csv` | Scraped review title, content, and rating |
| `sentiment_analysis_results.csv` | Reviews with predicted sentiment labels |
| `bigbasket_topics.csv` | Reviews with assigned topic IDs |
| `bigbasket_bertopic_model/` | Saved BERTopic model for reuse |
