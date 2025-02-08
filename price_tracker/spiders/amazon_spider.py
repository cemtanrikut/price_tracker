import scrapy
from fake_useragent import UserAgent

from database.database import check_price_drop, get_tracked_products, insert_or_update_product

class AmazonSpider(scrapy.Spider):
    name = "amazon"

    # start_urls = [
    #     "https://www.amazon.nl/dp/B07W4DGFSM",
    # ]
    
    def start_requests(self):
        # Takes following products URL's from the database and send to scrapy
        products = get_tracked_products()

        if not products:
            self.logger.warning("Takip edilen ürün bulunamadı!")
            return
        
        for product in products:
            if len(product) == 2:  # Hata çıkmasını önlemek için kontrol
                product_id, url = product
                yield scrapy.Request(url=url, callback=self.parse, meta={'product_id': product_id})
            else:
                self.logger.error(f"Data error: {product}")
            

    def parse(self, response):
        product_id = response.url.split("/dp/")[1].split("/")[0]

        ua = UserAgent()
        headers = {'User-Agent': ua.random}

        product_title = response.css("#productTitle::text").get()
        price = response.css(".a-price .a-offscreen::text").get()
        availability = response.css("#availability span::text").get()

        # Check if the product title, price and availability are not empty
        product_title = product_title.strip() if product_title else "Unknown"
        price = float(price.replace("€", "").replace(",", ".").strip()) if price else 0
        availability = availability.strip() if availability else "Stock Info Unknown"

        if check_price_drop(product_id, price):
            message = f"📉 **Price Dropped!** {product_title}\n💰 **New Price:** {price} €\n🔗 [Buy]({response.url})"
            # TODO: Send notification


        insert_or_update_product(product_id, product_title, price, availability)

        yield {
            'title': product_title,
            'price': price,
            'availability': availability,
        }
