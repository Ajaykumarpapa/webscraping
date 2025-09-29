Web Scraping file:
# --- INSTALL DEPENDENCIES ---
!apt-get update
!apt-get install -y wget curl unzip
!wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
!dpkg -i google-chrome-stable_current_amd64.deb || true
!apt-get install -f -y
!apt-get install -y chromium-chromedriver
!pip install chromedriver-autoinstaller selenium beautifulsoup4 pandas


import chromedriver_autoinstaller
chromedriver_autoinstaller.install()


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


driver = webdriver.Chrome(options=chrome_options)


# --- SCRAPING PARAMETERS ---
base_url = "https://www.mouthshut.com/product-reviews/bigbasket-reviews-925660627"
pages = 100


def scrape_reviews(url):
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


# Download the file in Colab
from google.colab import files
files.download('bigbasket_reviews.csv')