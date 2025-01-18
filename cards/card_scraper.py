import requests
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

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
                # Construct the full URL
                url = base_url.format(card_name)
                driver.get(url)
                
                wait = WebDriverWait(driver, 10)
                stats_rows = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "stats-row")))


               
            except Exception as e:
                print(f"[-] Error scraping {card_name}: {str(e)}")
                return None
        



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


