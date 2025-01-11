import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_cards():
    # Base URL
    url = "https://statsroyale.com/cards"
    
    # Headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Get the page
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all card elements
    cards = soup.find_all('div', class_='cards__card')
    
    card_data = []
    for card in cards:
        try:
            name = card.find('div', class_='cards__card__name').text.strip()
            rarity = card.find('div', class_='cards__card__rarity').text.strip()
            elixir = card.find('div', class_='cards__card__elixir').text.strip()
            type_ = card.find('div', class_='cards__card__type').text.strip() if card.find('div', class_='cards__card__type') else 'N/A'
            
            card_info = {
                'name': name,
                'rarity': rarity,
                'elixir': elixir,
                'type': type_
            }
            card_data.append(card_info)
            
        except AttributeError as e:
            print(f"Error processing card: {e}")
    
    # Convert to DataFrame
    df = pd.DataFrame(card_data)
    
    # Save to CSV
    df.to_csv('clash_royale_cards.csv', index=False)
    return df

if __name__ == "__main__":
    cards_df = scrape_cards()
    print(f"Scraped {len(cards_df)} cards successfully!")


