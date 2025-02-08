from scrapy.crawler import CrawlerProcess
from price_tracker.spiders.amazon_spider import AmazonSpider
from database.database import add_tracked_product, create_table

def add_product():
    url = input("Enter the URL of the product you want to track: ").strip()
    if "/dp/" in url:
        product_id = url.split("/dp/")[1].split("/")[0]
        add_tracked_product(product_id, url)
    else:
        print("❌ Wrong Amazon URL!")

if __name__ == "__main__":
    create_table()

    action = input("1 - Add Product\n2 - Run Scrapy\nChoose an action: ")

    if action == "1":
        add_product()
    elif action == "2":
        process = CrawlerProcess()
        process.crawl(AmazonSpider)
        process.start()
    else:
        print("❌ Invalid action!")    
