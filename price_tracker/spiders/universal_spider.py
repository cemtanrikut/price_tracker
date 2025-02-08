import scrapy
from fake_useragent import UserAgent
from database.database import insert_or_update_product, get_tracked_products
# from price_tracker.database.telegram_notify import send_telegram_message

class UniversalSpider(scrapy.Spider):
    name = "universal"

    def start_requests(self):
        products = get_tracked_products()
        
        if not products:
            self.logger.warning("Followed product doesn't found!")
            return

        for product_id, platform, url in products:
            yield scrapy.Request(url=url, callback=self.parse, meta={'product_id': product_id, 'platform': platform})

    def parse(self, response):
        ua = UserAgent()
        headers = {"User-Agent": ua.random}

        product_id = response.meta['product_id']
        platform = response.meta['platform']

        if platform == "amazon":
            product_title = response.css("#productTitle::text").get()
            price = response.css(".a-price .a-offscreen::text").get()
            availability = response.css("#availability span::text").get()
        elif platform == "ebay":
            product_title = response.css("h1[itemprop='name']::text").get()
            price = response.css(".display-price::text").get()
            availability = "Available"
        elif platform == "aliexpress":
            product_title = response.css("h1.product-title-text::text").get()
            price = response.css("div.product-price-current span::text").get()
            availability = response.css("div.product-quantity-tip::text").get()
        elif platform == "bol":
            product_title = response.css("span[data-test='title']::text").get()
            price = response.css("span.promo-price::text").get()
            availability = "In Stock"
        else:
            product_title, price, availability = "Unknown", "0", "Unknown"

        product_title = product_title.strip() if product_title else "Unknown"
        price = float(price.replace("€", "").replace(",", ".").strip()) if price else 0
        availability = availability.strip() if availability else "Unknown"

        insert_or_update_product(product_id, platform, product_title, price, availability)

        yield {
            "product_id": product_id,
            "platform": platform,
            "title": product_title,
            "price": price,
        }
