from datetime import datetime
import json
from pathlib import Path
import re
from typing import cast, List, Literal, TypedDict
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

Availability = Literal["In Stock", "Out Of Stock"]
Product = TypedDict(
    "Product",
    {
        "name": str,
        "price": float,
        "priceCurrency": Literal["CAD"],
        "availability": Availability,
        "url": str,
    },
)


def schema_to_availability(url: str) -> Availability:
    # Convert from schema URL to string.
    availability = urlparse(url).path[1:]
    availability = re.sub(r"([a-z])([A-Z])", r"\1 \2", availability)
    # Cast the string to a Literal.
    return cast(Availability, availability)


def parser(data) -> Product:
    offer = data["offers"][0]

    return {
        "name": data["name"].strip(),
        "price": offer["price"],
        "priceCurrency": offer["priceCurrency"],
        "availability": schema_to_availability(offer["availability"]),
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
        # Ignore any ld+json blocks that aren't a list/array.
        scripts = [data for data in scripts if isinstance(data, list)]

    except json.JSONDecodeError:
        print("⚠️ Skipping invalid JSON block")

    products = []
    for data in scripts:
        # Only parse items with @type=Product
        items = [parser(item) for item in data if item["@type"] == "Product"]
        products.extend(items)

    return products


if __name__ == "__main__":
    today = datetime.now().strftime("%Y-%m-%d")
    filepath = Path("data", f"{today}.json")
    data = fetch_products(URL)

    with open(filepath, "w") as fp:
        json.dump(data, fp, indent=2)
