# purdys-scraper

Playing w/ httpx and parsel to scrape a random product page.

## USAGE

```sh
make
```

### OUTPUT

```json
[
  {
    "name": "Vegan Mylk Chocolate Sweet Georgia Browns, pack of 2, 70 g",
    "price": 8,
    "priceCurrency": "CAD",
    "availability": "InStock",
    "url": "https://www.purdys.com/vegan-mylk-chocolate-sweet-georgia-browns-pack-of-2-70-g"
  },
  {
    "name": "Vegan Hawaiian Black Salt Caramels, 16 pc",
    "price": 40,
    "priceCurrency": "CAD",
    "availability": "InStock",
    "url": "https://www.purdys.com/vegan-hawaiian-black-salt-caramels-16-pc"
  },
  {
    "name": "Vegan Mylk Chocolate Classic Bar, pack of 9",
    "price": 46.5,
    "priceCurrency": "CAD",
    "availability": "InStock",
    "url": "https://www.purdys.com/vegan-mylk-chocolate-classic-bar-pack-of-9"
  },
  {
    "name": "Vegan Dark Chocolate Bar, 40 g",
    "price": 5.5,
    "priceCurrency": "CAD",
    "availability": "InStock",
    "url": "https://www.purdys.com/vegan-dark-chocolate-bar-40-g"
  },
  {
    "name": "Vegan Mylk Chocolate Bar, 40 g",
    "price": 5.5,
    "priceCurrency": "CAD",
    "availability": "InStock",
    "url": "https://www.purdys.com/vegan-mylk-chocolate-bar-40-g"
  },
  {
    "name": "Vegan Mylk Chocolate Sweet Georgia Browns, 8 pc",
    "price": 35.5,
    "priceCurrency": "CAD",
    "availability": "InStock",
    "url": "https://www.purdys.com/vegan-mylk-chocolate-sweet-georgia-browns-8-pc"
  },
  {
    "name": "Vegan Hawaiian Black Salt Caramels, 6 pc",
    "price": 20,
    "priceCurrency": "CAD",
    "availability": "OutOfStock",
    "url": "https://www.purdys.com/vegan-hawaiian-black-salt-caramels-6-pc"
  },
  {
    "name": "Vegan Dark Chocolate Collection, 16 pc",
    "price": 40,
    "priceCurrency": "CAD",
    "availability": "InStock",
    "url": "https://www.purdys.com/vegan-dark-chocolate-collection-16-pc"
  }
]
```
