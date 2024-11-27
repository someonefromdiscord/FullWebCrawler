import requests
from bs4 import BeautifulSoup
import time

def scrape_website(url, max_pages=1000000):
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
                full_link = link['href']
                if full_link.startswith('/'):
                    full_link = url + full_link  # Make it absolute
                if url in full_link and full_link not in visited_urls and len(pages_to_visit) < max_pages:
                    pages_to_visit.append(full_link)

        except Exception as e:
            print(f"Error scraping {current_url}: {e}")

        time.sleep(1)  # Respectful crawling delay

    return scraped_data

if __name__ == "__main__":
    start_url = 'https://google.com/search?q=random+sites&ref=youtube'  # Change this to the website you want to scrape
    data = scrape_website(start_url)
    
    for entry in data:
        print(entry)
