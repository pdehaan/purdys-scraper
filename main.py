import json
from typing import List, Literal, TypedDict
from urllib.parse import urlparse

import httpx
from parsel import Selector


URL = "https://www.purdys.com/chocolate/vegan-chocolates"


# class Product(TypedDict):
#     name: str
#     price: float
#     priceCurrency: Literal["CAD"]
#     availability: Literal["InStock", "OutOfStock"]
#     url: str

Product = TypedDict(
    "Product",
    {
        "name": str,
        "price": float,
        "priceCurrency": Literal["CAD"],
        "availability": Literal["InStock", "OutOfStock"],
        "url": str,
    },
)


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
    try:
        scripts = [
            json.loads(str)
            for str in selector.css('script[type="application/ld+json"]::text').getall()
        ]
        scripts = [data for data in scripts if isinstance(data, list)]

    except json.JSONDecodeError:
        print("⚠️ Skipping invalid JSON block")

    products = []
    for data in scripts:
        items = [parser(item) for item in data if item["@type"] == "Product"]
        products.extend(items)

    return products


if __name__ == "__main__":
    data = fetch_products(URL)
    print(json.dumps(data, indent=2))
