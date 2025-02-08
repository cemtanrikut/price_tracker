from scraper import get_product_info
from scrapy.crawler import CrawlerProcess
from database.database import add_tracked_product, create_table, insert_or_update_product
import re

from price_tracker.spiders.universal_spider import UniversalSpider
from scraper import get_product_info

def detect_platform(url):
    if "amazon" in url:
        return "amazon"
    elif "ebay" in url:
        return "ebay"
    elif "aliexpress" in url:
        return "aliexpress"
    elif "bol" in url:
        return "bol"
    else:
        return None

def add_product():
    url = input("Enter the URL of the product you want to track: ").strip()
    platform = detect_platform(url)

    if platform is None:
        print("❌ Unsupported platform!")
        return

    match = re.search(r"/dp/(\w+)", url) if platform == "amazon" else re.search(r"/(\d+)", url)
    if match:
        product_id = match.group(1)

        title, price, availability = get_product_info(url, platform)

        if title is None:
            title, price, availability = "Product title uploading...", -1.0, "Availability uploading..."
        
        add_tracked_product(product_id, platform, url)

        print(f"🚀 New product added: {product_id} ({platform}). Scrapy starting...")

        insert_or_update_product(product_id, platform, title, price, availability)

        print(f"✅ Product followed and added Products table: {product_id} ({platform})")
  
    else:
        print("❌ Wrong URL!")

if __name__ == "__main__":
    create_table()

    action = input("1 - Add Product\n2 - Run Scrapy\nChoose an action: ")

    if action == "1":
        add_product()
    elif action == "2":
        process = CrawlerProcess()
        process.crawl(UniversalSpider)
        process.start()
        # print("💡 Scrapy works on `scheduler.py`.")
    else:
        print("❌ Invalid action!")    
