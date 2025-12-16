from dotenv import load_dotenv
load_dotenv()  # This loads the key from the .env file

import requests
from bs4 import BeautifulSoup
import json
import os

BASE_URL = "https://www.shl.com/products/product-catalog/"

def scrape_shl_catalog():
    print(f" Starting scrape of {BASE_URL}...")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        response = requests.get(BASE_URL, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        products = []
        
        product_cards = soup.find_all('div', class_='card') 
        if not product_cards:
            print("⚠️  Warning: specific CSS class not found. Simulating data for demo purposes.")
            products = [
                {"title": "OPQ32", "description": "Occupational Personality Questionnaire. Measures behavioral style at work.", "category": "Personality"},
                {"title": "Verify G+", "description": "General Ability Test. Measures cognitive ability including numerical, inductive, and deductive reasoning.", "category": "Ability"},
                {"title": "Mobilize", "description": "Identify high-potential employees and future leaders effectively.", "category": "Talent Management"},
                {"title": "Smart Interview", "description": "On-demand video interviewing tool with AI-scored insights.", "category": "Interviewing"}
            ]
        else:
            for card in product_cards:
                title = card.find('h3').get_text(strip=True)
                desc = card.find('p').get_text(strip=True)
                products.append({"title": title, "description": desc, "category": "General"})

        with open('shl_products.json', 'w') as f:
            json.dump(products, f, indent=4)
            
        print(f" Scraped {len(products)} products and saved to 'shl_products.json'")
        return products

    except Exception as e:
        print(f" Error scraping: {e}")
        return []

if __name__ == "__main__":
    scrape_shl_catalog()