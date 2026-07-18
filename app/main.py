import json
from customer import Customer
from shop import Shop

def shop_trip():
    with open("config.json", "r") as f:
        data = json.load(f)
