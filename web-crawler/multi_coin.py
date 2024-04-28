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
    aud_element = soup.select_one(".rich-text h4:nth-of-type(2)")
    aud = aud_element.text.strip() if aud_element else "N/A"

    return {
        "URL": url,
        "Name": name,
        "SKU": sku,
        "AUD": aud,
        "Metal": metal,
        "Gold Content (Troy oz)": metal_content,
        "Monetary Denomination (AUD)": monetary_denomination,
        "Minimum Gross Weight (g)": gross_weight,
    }


def main():
    base_url = "https://www.perthmint.com/shop/collector-coins/coins/"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, "html.parser")

    products = []

    # Extract links from the page
    links = soup.select("a[href^='/shop/collector-coins/coins/']")

    # Scrape details for each product URL
    for link in links:
        url = "https://www.perthmint.com" + link.get("href")
        product_details = scrape_product_details(url)
        if product_details:
            products.append(product_details)

    # Save scraped data to a CSV file
    with open('coins.csv', 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ["URL", "Name", "SKU", "AUD", "Metal", "Gold Content (Troy oz)", "Monetary Denomination (AUD)", "Minimum Gross Weight (g)"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)

if __name__ == "__main__":
    main()
