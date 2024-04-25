import requests
from bs4 import BeautifulSoup
import csv

def scrape_product_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    metal = "N/A"
    metal_content = "N/A"
    monetary_denomination = "N/A"
    gross_weight = "N/A"

    # Find all rows containing the details
    rows = soup.select('.table__tbody .table__row')

    # Loop through each row to extract details
    for row in rows:
        cells = row.find_all('span', {'role': 'cell'})
        if len(cells) == 2:
            label = cells[0].text.strip()
            value = cells[1].text.strip()

            if label == "Metal":
                metal = value
            elif label == "Gold Content (Troy oz)":
                metal_content = value
            elif label == "Monetary Denomination (AUD)":
                monetary_denomination = value
            elif label == "Minimum Gross Weight (g)":
                gross_weight = value

    # Extract product name
    name_element = soup.select_one(".product-detail__info h1")
    name = name_element.text.strip() if name_element else "N/A"
 
    # Extract product SKU
    sku_element = soup.find("td", string="SKU")
    sku = sku_element.find_next_sibling("td").text.strip() if sku_element else "N/A"
    
    # Extract product AUD
    aud_element = "N/A"

    return {
        "URL": url,
        "Name": name,
        "SKU": sku,
        "AUD":aud_element,
        "Metal": metal,
        "Gold Content (Troy oz)": metal_content,
        "Monetary Denomination (AUD)": monetary_denomination,
        "Minimum Gross Weight (g)": gross_weight,
    }
    
    
def main():
    base_url = "https://www.perthmint.com/shop/collector-coins/coins/australian-kangaroo-2024-1oz-gold-proof-high-relief-coin/"
    urls_to_scrape = [base_url]

    products = []
    products_scraped = 0
    max_products = 10

    while urls_to_scrape and products_scraped < max_products:
        url = urls_to_scrape.pop()
        product_details = scrape_product_details(url)
        if product_details:
            products.append(product_details)
            products_scraped += 1

            # Extract links from the page
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            links = soup.select("a[href^='https://www.perthmint.com/shop/collector-coins/coins/australian-kangaroo-2024-1oz-gold-proof-high-relief-coin/']")

            # Add discovered links to the list of URLs to scrape
            for link in links:
                new_url = link.get("href")
                if new_url not in urls_to_scrape and len(products) < max_products:
                    urls_to_scrape.append(new_url)

    # Save scraped data to a CSV file
    with open('coins.csv', 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ["URL", "Name", "SKU","AUD", "Metal", "Gold Content (Troy oz)", "Monetary Denomination (AUD)", "Minimum Gross Weight (g)"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)

if __name__ == "__main__":
    main()
