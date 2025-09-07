from datetime import datetime
import json
from pathlib import Path
import re
from typing import cast, Any, Dict, List, Literal, TypedDict
from urllib.parse import urlparse

import httpx
from parsel import Selector


URL = "https://www.purdys.com/chocolate/vegan-chocolates#/sort:name:asc"

# TODO: Move to pydantic model?
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
    """
    Converts from `"https://schema.org/InStock"` to `"In Stock"`.
    """
    # Convert from schema URL to string.
    availability = urlparse(url).path[1:]
    availability = re.sub(r"([a-z])([A-Z])", r"\1 \2", availability)
    # Cast the string to a Literal.
    return cast(Availability, availability)


def parser(data: Dict[Any, Any]) -> Product:
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
        ldjson_scripts: List[Dict[Any, Any]] = [
            json.loads(str)
            for str in selector.css('script[type="application/ld+json"]::text').getall()
        ]
        # Ignore any ld+json blocks that aren't a list/array.
        scripts = [data for data in ldjson_scripts if isinstance(data, list)]

    except json.JSONDecodeError:
        print("⚠️ Skipping invalid JSON block")
        scripts = []

    products: List[Product] = []
    for data in scripts:
        # Only parse items with @type=Product
        items = [parser(item) for item in data if item["@type"] == "Product"]
        products.extend(items)

    # Sort products by URL so diffs are a bit more consistent.
    return sorted(products, key=lambda x: x["url"])


if __name__ == "__main__":
    today = datetime.now().strftime("%Y-%m-%d")
    filepath = Path("data", f"{today}.json")
    data = fetch_products(URL)

    # TODO: Only write file if different from previous file?
    with open(filepath, "w") as fp:
        json.dump(data, fp, indent=2)
