import json
from .car import Car
from .customer import Customer
from .shop import Shop
import math


def shop_trip() -> None:
    with open("app/config.json", "r") as f:
        config = json.load(f)

    fuel_price = config["FUEL_PRICE"]

    customers = []
    for cus in config["customers"]:
        car = Car(cus["car"]["brand"], cus["car"]["fuel_consumption"])
        customer = Customer(
            name=cus["name"],
            location=cus["location"],
            money=cus["money"],
            car=car,
            home_location=cus["location"],
            product_cart=cus["product_cart"]
        )
        customers.append(customer)

    shops = []
    for item in config["shops"]:
        shop = Shop(
            name=item["name"],
            location=item["location"],
            products=item["products"]
        )
        shops.append(shop)

    for customer in customers:
        cheapest_cost = float("inf")
        cheapest_shop = None
        print(f"{customer.name} has {customer.money} dollars")

        for shop in shops:
            distancia_ida = math.hypot(shop.location[0] - customer.location[0],
                                       shop.location[1] - customer.location[1])
            custo_ida = customer.car.calculate_fuel_cost(
                distancia_ida,
                fuel_price
            )
            custo_produtos = shop.calculate_products_cost(
                customer.product_cart
            )
            distancia_volta = math.hypot(
                shop.location[0] - customer.home_location[0],
                shop.location[1] - customer.home_location[1]
            )
            custo_volta = customer.car.calculate_fuel_cost(
                distancia_volta,
                fuel_price
            )
            custo_total = custo_ida + custo_produtos + custo_volta
            print(f"{customer.name}'s trip to the "
                  f"{shop.name} costs {custo_total:.2f}")
            if custo_total < cheapest_cost:
                cheapest_cost = custo_total
                cheapest_shop = shop

        if customer.money > cheapest_cost:
            print(f"{customer.name} "
                  f"rides to {cheapest_shop.name}")
            print()
            customer.location = cheapest_shop.location
            customer.go_to_shop(
                cheapest_shop,
                fuel_price)
            cheapest_shop.sell_products(
                customer.product_cart
            )
            custo_produtos = cheapest_shop.calculate_products_cost(
                customer.product_cart
            )
            cheapest_shop.print_receipt(
                customer.name,
                customer.product_cart,
                custo_produtos
            )
            customer.location = customer.home_location
            customer.go_home(
                cheapest_shop,
                fuel_price
            )
            print(f"{customer.name} rides home")
            customer.money -= cheapest_cost
            print(f"{customer.name} now has "
                  f"{customer.money:.2f} dollars")
            print()
        else:
            print(f"{customer.name} doesn't have enough money "
                  f"to make a purchase in any shop")
