#!/usr/bin/env python3
"""Web Scraping Script for BigBasket Reviews from MouthShut"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import sys

# --- SETUP CHROME OPTIONS ---
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')

try:
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print("Chrome driver initialized successfully!")
except Exception as e:
    print(f"Error initializing Chrome driver: {e}")
    print("Please ensure Chrome/Chromium browser is installed.")
    sys.exit(1)

# --- SCRAPING PARAMETERS ---
base_url = "https://www.mouthshut.com/product-reviews/bigbasket-reviews-925660627"
pages = 100

def scrape_reviews(url):
    """Scrape reviews from a given URL"""
    try:
        driver.get(url)
        time.sleep(random.uniform(6, 10))  # Wait for page to load fully
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
    except Exception as e:
        print(f"Error accessing URL {url}: {e}")
        return []

print("Starting scraping...")
all_reviews_data = []
try:
    for page in range(pages):
        page_url = f"{base_url}-page-{page+1}"
        print(f"Scraping page {page+1}...")
        reviews_data = scrape_reviews(page_url)
        print(f"Found {len(reviews_data)} reviews on page {page+1}")
        all_reviews_data.extend(reviews_data)
finally:
    driver.quit()
    print("Browser closed.")

# --- SAVE TO CSV ---
df = pd.DataFrame(all_reviews_data)
df.to_csv('bigbasket_reviews.csv', index=False, encoding='utf-8')
print(f"Scraping completed! {len(df)} reviews saved to bigbasket_reviews.csv")
