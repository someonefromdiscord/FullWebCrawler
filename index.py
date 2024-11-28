import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs, urlencode
import time

def normalize_url(url):
    """Normalize the URL by removing unwanted query parameters."""
    parsed_url = urlparse(url)
    # Keep only the scheme, netloc, and path
    normalized = parsed_url._replace(query='')
    return normalized.geturl()

def scrape_website(url, max_pages=111000000):
    scraped_data = []
    visited_urls = set()
    pages_to_visit = [url]
    
    while pages_to_visit and len(scraped_data) < max_pages:
        current_url = pages_to_visit.pop(0)
        
        if current_url in visited_urls:
            continue
        
        print(f"Scraping: {current_url}")
        visited_urls.add(current_url)
        
        try:
            response = requests.get(current_url)
            response.raise_for_status()  # Raise an error for bad responses
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract data (modify this part based on your needs)
            title = soup.title.string if soup.title else 'No Title'
            scraped_data.append({'url': current_url, 'title': title})
            
            # Find all links on the page
            for link in soup.find_all('a', href=True):
                full_link = urljoin(current_url, link['href'])  # Make it absolute using urljoin
                normalized_link = normalize_url(full_link)  # Normalize the URL
                if normalized_link not in visited_urls and len(pages_to_visit) < max_pages:
                    pages_to_visit.append(normalized_link)

        except Exception as e:
            print(f"Error scraping {current_url}: {e}")

        time.sleep(1)  # Respectful crawling delay

    return scraped_data

if __name__ == "__main__":
    start_url = 'https://google.com/search?q=random+sites&ref=youtube'  # Change this to the website you want to scrape
    data = scrape_website(start_url)
    
    for entry in data:
        print(entry)
