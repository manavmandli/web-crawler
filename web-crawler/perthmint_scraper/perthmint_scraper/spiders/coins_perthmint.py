import scrapy

class CoinsSpider(scrapy.Spider):
	name = 'coins_perthmint'
	start_urls = ['https://www.perthmint.com/shop/collector-coins/coins/']

	def parse(self, response):
		# Extract links to individual product pages
		product_links = response.css('a[href^="/shop/collector-coins/coins/"]::attr(href)').getall()
		yield from response.follow_all(product_links, self.parse_product)

		# Follow pagination links if present
		next_page = response.css('.pagination__next a::attr(href)').get()
		if next_page:
			yield response.follow(next_page, self.parse)

	def parse_product(self, response):
		metal = "N/A"
		metal_content = "N/A"
		monetary_denomination = "N/A"
		gross_weight = "N/A"

		# Loop through each row to extract details
		for row in response.css('.table .table__tbody .table__row'):
			label = row.css('span[role="cell"]::text').get()
			value = row.css('span[role="cell"] + span::text').get()
			
			if label == "Metal":
				metal = value.strip()
			elif label == "Gold Content (Troy oz)":
				metal_content = value.strip()
			elif label == "Monetary Denomination (AUD)":
				monetary_denomination = value.strip()
			elif label == "Minimum Gross Weight (g)":
				gross_weight = value.strip()

		sku_element = response.css('td:contains("SKU") + td::text').get()
		sku = sku_element.strip() if sku_element else "N/A"
		
		aud_element = response.css(".rich-text h4:nth-of-type(2)::text").get()
		aud = aud_element.strip() if aud_element else "N/A"

		product_details = {
			'URL': response.url,
			'Name': response.css('.product-detail__info h1::text').get().strip(),
			'SKU': sku,
			'AUD': aud,
			'Metal': metal,
			'Gold Content (Troy oz)': metal_content,
			'Monetary Denomination (AUD)': monetary_denomination,
			'Minimum Gross Weight (g)': gross_weight
		}
		yield product_details
		
	def extract_value(self, response, label):
		value = response.css(f'span[role="cell"]:contains("{label}") + span::text').get()
		return value.strip() if value else 'N/A'
