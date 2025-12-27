#!/usr/bin/env python3
"""Test script for web scraping - only scrapes 2 pages"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

# --- SETUP CHROME OPTIONS ---
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

print("Initializing Chrome driver...")
driver = webdriver.Chrome(options=chrome_options)
print("Chrome driver initialized successfully!")

# --- SCRAPING PARAMETERS ---
base_url = "https://www.mouthshut.com/product-reviews/bigbasket-reviews-925660627"
pages = 2  # Only test with 2 pages

def scrape_reviews(url):
    driver.get(url)
    time.sleep(random.uniform(3, 5))  # Reduced wait time for testing
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    reviews_list = []

    review_containers = soup.find_all("div", class_="review-article")

    for container in review_containers:
        try:
            title_tag = container.find("a", class_="rptreviews_ct100_lnkTitle")
            title = title_tag.text.strip() if title_tag else "No Title"

            content_div = container.find("div", class_="more")
            content = content_div.text.strip() if content_div else "No Content"

            rating_div = container.find("div", class_="rating")
            rating = rating_div.text.strip() if rating_div else "No Rating"

            reviews_list.append({
                "title": title,
                "content": content,
                "rating": rating
            })
        except Exception as e:
            print(f"Error parsing review: {e}")
            continue
    return reviews_list

print("Starting test scraping (2 pages only)...")
all_reviews_data = []
try:
    for page in range(pages):
        page_url = f"{base_url}-page-{page+1}"
        print(f"Scraping page {page+1}...")
        reviews_data = scrape_reviews(page_url)
        print(f"Found {len(reviews_data)} reviews on page {page+1}")
        all_reviews_data.extend(reviews_data)
except Exception as e:
    print(f"Error during scraping: {e}")
finally:
    driver.quit()
    print("Browser closed.")

# --- SAVE TO CSV ---
df = pd.DataFrame(all_reviews_data)
df.to_csv('bigbasket_reviews.csv', index=False, encoding='utf-8')
print(f"Test scraping completed! {len(df)} reviews saved to bigbasket_reviews.csv")
print(f"\nFirst few reviews:")
print(df.head())
