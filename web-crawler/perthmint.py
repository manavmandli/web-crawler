import requests
import pandas as pd

BASE_URL = "https://www.perthmint.com/api/search/product/node/1073746523"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
}

def fetch_page_data(page_number, page_size=100):
    url = f"{BASE_URL}?page={page_number}&pageSize={page_size}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve page {page_number}")
        return None

def extract_coin_details(data):
    coin_details = []
    for item in data['result']['products']:
        price = item.get('prices', {})
        base_price = price.get('basePrice', {})
        price_str = "N/A N/A"
        if base_price and isinstance(base_price, dict):
            price = base_price.get('price', 'N/A')
            code = base_price.get('code', 'N/A')
            price_str = f"{price} {code}"
        coin = {
            'URL': item.get('link', ''),
            'Coin Name': item.get('title', ''),
            'SKU': item.get('skuItemNumber', ''),
            'AUD': price_str,
        }
        coin_details.append(coin)
    return coin_details

def scrape_all_pages():
    # max_pages = 2
    page_number= 1
    coins_data= []
    
    # while page_num <= max_pages:
    while True:
        data = fetch_page_data(page_number)
        if data and 'result' in data and 'products' in data['result'] and len(data['result']['products']) > 0:
            coins = extract_coin_details(data)
            coins_data.extend(coins)
            print(f"Page {page_number} processed, {len(coins)} coins found.")
            page_number += 1
        else:
            break
    
    df = pd.DataFrame(coins_data)
    df.to_csv('coin_details.csv', index=True)
    print(f"Scraping completed. Total {len(coins_data)} coins found and saved to coins_details.csv.")

if __name__ == "__main__":
    scrape_all_pages()
