from scrapy.crawler import CrawlerProcess
from price_tracker.spiders.amazon_spider import AmazonSpider
from database.database import create_table

create_table()

# Run scrapy bot
process = CrawlerProcess()
process.crawl(AmazonSpider)
process.start()
