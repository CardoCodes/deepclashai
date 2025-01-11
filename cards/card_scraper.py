import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
def parse_cards_file(filename):
    categories = [[], [], []]  # [cards, evolutions, towers]
    current_category = None
    
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
                
            # Determine category
            if line == "Cards:":
                current_category = 0
                continue
            elif line == "Evolutions:":
                current_category = 1
                continue
            elif line == "Towers:":
                current_category = 2
                continue
            
            # Add item to appropriate category if we're in a category
            if current_category is not None:
                categories[current_category].append(line)
    
    return categories

def scrape_cards():
    # Base URL
    url = "https://statsroyale.com/top/cards"
    
    # Headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Get the page
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')


if __name__ == "__main__":
    # Example usage
result = parse_cards_file('cards/cards.txt')

# Print results (optional)
print("Cards:", result[0])
print("\nEvolutions:", result[1])
print("\nTowers:", result[2])
    

    print("[+] Done")


