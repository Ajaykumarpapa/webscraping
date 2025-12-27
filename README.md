# BigBasket Reviews Analysis

This project contains Python scripts for web scraping BigBasket reviews from MouthShut, performing sentiment analysis, and topic modeling.

## Project Structure

- `webscraping.py` - Scrapes BigBasket reviews from MouthShut website
- `sentiment_analysis.py` - Performs sentiment analysis on the scraped reviews using Naive Bayes
- `topic_modeling.py` - Performs topic modeling on the reviews using BERTopic
- `requirements.txt` - List of required Python packages
- `create_test_data.py` - Creates sample test data for testing the scripts

## Prerequisites

### System Requirements

1. **Python 3.8+**
2. **Chrome/Chromium Browser** - Required for web scraping
   ```bash
   # On Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install chromium-browser chromium-chromedriver

   # Or install Google Chrome
   wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
   sudo dpkg -i google-chrome-stable_current_amd64.deb
   ```

### Python Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install selenium beautifulsoup4 pandas scikit-learn matplotlib webdriver-manager
pip install bertopic sentence-transformers umap-learn
```

## Usage

### 1. Web Scraping

Scrape reviews from MouthShut:

```bash
python webscraping.py
```

This will:
- Scrape 100 pages of BigBasket reviews (configurable)
- Save results to `bigbasket_reviews.csv`
- Contains columns: title, content, rating

**Note**: The scraping process may take a while. You can modify the `pages` variable in the script to scrape fewer pages for testing.

### 2. Sentiment Analysis

Analyze sentiment of the scraped reviews:

```bash
python sentiment_analysis.py
```

This will:
- Load data from `bigbasket_reviews.csv`
- Clean and preprocess the text
- Train a Naive Bayes classifier
- Generate classification report
- Save confusion matrix to `confusion_matrix.png`
- Save results to `sentiment_analysis_results.csv`

### 3. Topic Modeling

Discover topics in the reviews:

```bash
python topic_modeling.py
```

This will:
- Load data from `sentiment_analysis_results.csv` or `bigbasket_reviews.csv`
- Clean and preprocess the text
- Apply BERTopic for topic modeling
- Generate visualizations (saved as HTML files)
- Save results to `bigbasket_topics.csv`

## Testing

To test the scripts without web scraping:

```bash
# Create sample test data
python create_test_data.py

# Run sentiment analysis on test data
python sentiment_analysis.py

# Run topic modeling on test data
python topic_modeling.py
```

## Output Files

- `bigbasket_reviews.csv` - Raw scraped reviews
- `sentiment_analysis_results.csv` - Reviews with predicted sentiments
- `confusion_matrix.png` - Confusion matrix visualization
- `bigbasket_topics.csv` - Reviews with assigned topics
- `topic_barchart.html` - Interactive topic visualization
- `document_clustering.html` - Interactive document clustering visualization
- `bigbasket_bertopic_model/` - Saved BERTopic model

## Configuration

### Web Scraping Parameters

In `webscraping.py`:
- `pages` - Number of pages to scrape (default: 100)
- `base_url` - URL to scrape from

### Sentiment Analysis Parameters

In `sentiment_analysis.py`:
- Sentiment thresholds can be adjusted in the `get_sentiment()` function
- Vectorizer parameters can be modified in the `CountVectorizer()` initialization

### Topic Modeling Parameters

In `topic_modeling.py`:
- `min_topic_size` - Minimum number of documents per topic (default: 25)
- `n_neighbors` - UMAP parameter for clustering (default: 15)
- `n_components` - UMAP dimensionality (default: 5)

## Troubleshooting

### Chrome/ChromeDriver Issues

If you encounter Chrome/ChromeDriver errors:
1. Ensure Chrome or Chromium is installed
2. The script uses `webdriver-manager` to automatically download the correct ChromeDriver
3. Try running with `--headless` mode (already configured)

### Memory Issues

For large datasets:
- Reduce the number of pages to scrape
- Process data in batches
- Increase system memory allocation

### Missing Data Files

If `sentiment_analysis.py` or `topic_modeling.py` fail:
- Ensure `bigbasket_reviews.csv` exists (run `webscraping.py` or `create_test_data.py` first)
- Check file permissions

## Notes

- The web scraping script includes random delays to avoid overwhelming the server
- Sentiment analysis uses a simple threshold-based approach (rating >= 4 is positive, <= 2 is negative)
- Topic modeling requires sufficient data for meaningful results (minimum 25 documents per topic by default)
- All scripts include error handling for robustness

## License

This project is for educational purposes only. Ensure you comply with MouthShut's terms of service when scraping data.
