import json
from typing import List, TypedDict
from urllib.parse import urlparse

import httpx
from parsel import Selector


URL = "https://www.purdys.com/chocolate/vegan-chocolates"


class Product(TypedDict):
    name: str
    price: float
    priceCurrency: str
    availability: str
    url: str


def parser(data) -> Product:
    offer = data["offers"][0]
    return {
        "name": data["name"].strip(),
        "price": offer["price"],
        "priceCurrency": offer["priceCurrency"],
        # Convert from schema URL to string
        "availability": urlparse(offer["availability"]).path[1:],
        "url": offer["url"],
    }


def fetch_products(url: str) -> List[Product]:
    res = httpx.get(url, timeout=10.0)
    res.raise_for_status()

    selector = Selector(text=res.text)
    scripts = selector.css('script[type="application/ld+json"]::text').getall()

    products = []
    for script in scripts:
        try:
            data = json.loads(script)
            if isinstance(data, list):
                items = [parser(item) for item in data if item["@type"] == "Product"]
                products.extend(items)

        except json.JSONDecodeError:
            print("⚠️ Skipping invalid JSON block")

    return products


if __name__ == "__main__":
    data = fetch_products(URL)
    print(json.dumps(data, indent=2))
