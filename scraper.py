import requests
from parsel import Selector
from fake_useragent import UserAgent

def get_product_info(url, site):
    ua = UserAgent()
    headers = {"User-Agent": ua.random}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"❌ Product info doesn't fetch, HTTP {response.status_code}")
            return None, None, None

        selector = Selector(text=response.text)

        if site == "amazon":
            title = selector.css("#productTitle::text").get()
            price = selector.css(".a-price .a-offscreen::text").get()
            availability = selector.css("#availability span::text").get()
        elif site == "ebay":
            title = selector.css("h1[itemprop='name']::text").get()
            price = selector.css(".display-price::text").get()
            availability = "Available"
        elif site == "aliexpress":
            title = selector.css("h1.product-title-text::text").get()
            price = selector.css("div.product-price-current span::text").get()
            availability = selector.css("div.product-quantity-tip::text").get()
        elif site == "bol":
            title = selector.css("span[data-test='title']::text").get()
            price = selector.css("span.promo-price::text").get()
            availability = "In Stock"
        else:
            return None, None, None

        title = title.strip() if title else "Product title uploading..."
        price = float(price.replace("€", "").replace(",", ".").strip()) if price else -1.0
        availability = availability.strip() if availability else "Availability uploding..."

        return title, price, availability

    except Exception as e:
        print(f"❌ Product fetching error: {e}")
        return None, None, None
