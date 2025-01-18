import requests
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import json
from card import Card

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
    
    # Initialize all cards data
    all_cards_data = []

    driver = webdriver.Chrome()
    
    # Iterate through all categories
    for category_index, category in enumerate(cards_list):
        for card_name in category:
            try:
                # Create a new card instance
                card = Card(card_name)
                
                # Construct the full URL and get the page
                url = base_url.format(card_name)
                driver.get(url)
                wait = WebDriverWait(driver, 10)

                # Pull all divs that have the class "stats-row"
                stats_rows = driver.find_elements(By.CLASS_NAME, "stats-row")

                # Parse the stats for the card
                for row in stats_rows:
                    if row.find_element(By.XPATH, "..").get_attribute("class") == "content-box-main":
                        stat_text = row.text.lower()
                        # Split the text by newline
                        parts = stat_text.split('\n')
                        if len(parts) == 2:
                            stat_name = parts[0].strip()
                            stat_value = parts[1].strip()
                            # Try to convert to int if it's a number, otherwise keep as string
                            try:
                                stat_value = int(''.join(filter(str.isdigit, stat_value)))
                            except ValueError:
                                pass
                            card.add_stat(stat_name, stat_value)
                    else:
                        break
                
                all_cards_data.append(card.to_dict())
               
            except Exception as e:
                print(f"[-] Error scraping {card_name}: {str(e)}")
                continue
    
    driver.quit()
    return all_cards_data

if __name__ == "__main__":
    # Example usage
    cards_list = parse_cards_file('tools/cards.txt')
    cards_list = format_card_names(cards_list)
    cards_data = scrape_cards(cards_list)

    # Save to JSON file
    if cards_data:
        with open('cards_data.json', 'w') as f:
            json.dump(cards_data, f, indent=4)
        print("\nCards data saved to cards_data.json")

    print("[+] Done")

