from bs4 import BeautifulSoup
import requests
import csv

def scrape_product_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    product = {
        "URL": url,
        "Name": soup.select_one(".product-detail__info h1").text.strip(),
        "SKU": "N/A",  # Set default value for SKU
        "AUD": "N/A",
        "Metal": "N/A",
        "Gold Content (Troy oz)": "N/A",
        "Monetary Denomination (AUD)": "N/A",
        "Minimum Gross Weight (g)": "N/A"
    }

    # Extracting SKU if found
    sku_element = soup.find("td", string="SKU")
    if sku_element:
        next_sibling = sku_element.find_next_sibling("td")
        if next_sibling:
            product["SKU"] = next_sibling.text.strip()

    # Extracting additional details
    rows = soup.select('.table__tbody .table__row')
    for row in rows:
        label_element = row.find('span', {'role': 'cell'})
        value_elements = row.find_all('span', {'role': 'cell'})
        if label_element and len(value_elements) >= 2:
            label = label_element.text.strip()
            value = value_elements[1].text.strip()
            if label == "Metal":
                product["Metal"] = value
            elif label == "Gold Content (Troy oz)":
                product["Gold Content (Troy oz)"] = value
            elif label == "Monetary Denomination (AUD)":
                product["Monetary Denomination (AUD)"] = value
            elif label == "Minimum Gross Weight (g)":
                product["Minimum Gross Weight (g)"] = value

    return product




def main():
    base_url = "https://www.perthmint.com/shop/collector-coins/coins/"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, "html.parser")

    products = []
    max_products = 10

    # Extract links from the page
    links = soup.select("a[href^='/shop/collector-coins/coins/']")

    # Scrape details for each product URL
    for link in links[:max_products]:
        url = "https://www.perthmint.com" + link.get("href")
        product_details = scrape_product_details(url)
        products.append(product_details)

    # Save scraped data to a CSV file
    with open('coins.csv', 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ["URL", "Name", "SKU", "AUD", "Metal", "Gold Content (Troy oz)", "Monetary Denomination (AUD)", "Minimum Gross Weight (g)"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)

if __name__ == "__main__":
    main()
