import requests
from bs4 import BeautifulSoup
import csv

# Function to scrape product details from a given URL
def scrape_product_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract product image
    image_element = soup.select_one(".wp-post-image")
    image_url = image_element["src"] if image_element else "N/A"

    # Extract product name
    title_element = soup.select_one(".product_title")
    name = title_element.text.strip() if title_element else "N/A"

    # Extract product price
    price_element = soup.select_one(".price")
    price = price_element.text.strip() if price_element else "N/A"

    return {
        "url": url,
        "image": image_url,
        "name": name,
        "price": price
    }

# Main function to crawl multiple pages and scrape product details
def main():
    base_url = "https://www.scrapingcourse.com/ecommerce/"
    urls_to_scrape = [base_url]

    products = []
    products_scraped = 0
    max_products = 20

    while urls_to_scrape and products_scraped < max_products:
        url = urls_to_scrape.pop()
        product_details = scrape_product_details(url)
        products.append(product_details)
        products_scraped += 1
        

        # Extract links from the page
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        links = soup.select("a[href^='https://www.scrapingcourse.com/ecommerce/']")

        # Add discovered links to the list of URLs to scrape
        for link in links:
            new_url = link.get("href")
            if new_url not in urls_to_scrape:
                urls_to_scrape.append(new_url)
        print("------------------")

    # Save scraped data to a CSV file
    with open('products.csv', 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["url", "image", "name", "price"])
        writer.writeheader()
        writer.writerows(products)

if __name__ == "__main__":
    main()
