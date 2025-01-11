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

def format_card_names(cards_list):
    # Replace spaces with + in all categories
    for category in cards_list:
        for i in range(len(category)):
            category[i] = category[i].replace(" ", "+")
    
    # Add /evolved to evolution cards
    for i in range(len(cards_list[1])):
        cards_list[1][i] = cards_list[1][i] + "/evolved"
    
    return cards_list

def scrape_cards(cards_list):
    # Base URL
    base_url = "https://statsroyale.com/card/{}"
    
    # Headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    all_cards_data = []
    
    # Iterate through all categories
    for category_index, category in enumerate(cards_list):
        for card_name in category:
            try:
                # Construct the full URL
                url = base_url.format(card_name)
                
                # Get the page
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                
                # Parse the HTML
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract card information
                card_data = {
                    "name": card_name.replace("+", " ").replace("/evolved", ""),
                    "category": ["Regular", "Evolution", "Tower"][category_index],
                    "rarity": soup.find("div", class_="card__rarity").text.strip() if soup.find("div", class_="card__rarity") else "Unknown",
                    "elixir": soup.find("div", class_="card__elixir").text.strip() if soup.find("div", class_="card__elixir") else "Unknown",
                    "stats": {}
                }
                
                # Get card statistics
                stats_container = soup.find("div", class_="card__stats")
                if stats_container:
                    stats = stats_container.find_all("div", class_="card__stat")
                    for stat in stats:
                        stat_name = stat.find("div", class_="card__stat-name").text.strip()
                        stat_value = stat.find("div", class_="card__stat-value").text.strip()
                        card_data["stats"][stat_name] = stat_value
                
                all_cards_data.append(card_data)
                
                # Add a small delay to avoid overwhelming the server
                time.sleep(1)
                
                print(f"[+] Successfully scraped {card_name}")
                
            except Exception as e:
                print(f"[-] Error scraping {card_name}: {str(e)}")
    
    # Convert to DataFrame and save to CSV (optional)
    df = pd.DataFrame(all_cards_data)
    df.to_csv('card_data.csv', index=False)
    
    return all_cards_data



if __name__ == "__main__":
    # Example usage
    cards_list = parse_cards_file('cards/cards.txt')
    cards_list = format_card_names(cards_list)
    card_data = scrape_cards(cards_list)

    # Print the first card's data as an example
    if card_data:
        print("\nExample card data:")
        print(card_data[0])

    print("[+] Done")


