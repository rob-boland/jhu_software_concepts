import pytest

# Intra-package imports
from module_4.pizza import Pizza
from module_4.order import Order

@pytest.fixture
def pizza_data_list():
    return [
        ("thin", ["pesto"], "mozzarella", ["mushrooms"], 11),
        ("thick", ["marinara"], "mozzarella", ["mushrooms", "pineapple"], 12),
        ("gluten_free", ["marinara", "pesto"], "mozzarella", ["pepperoni"], 15),
        ("thin", ["liv_sauce", "marinara"], "mozzarella", ["pepperoni", "mushrooms"], 17),
    ]

def test_multiple_pizzas_in_order_increases_cost(pizza_data_list):
    order = Order()
    running_cost = 0
    for crust, sauce, cheese, toppings, expected_cost in pizza_data_list:
        pizza = Pizza(crust, sauce, toppings, cheese)
        order.cart.append(pizza)
        order.cost += pizza.cost()
        running_cost += expected_cost
        assert order.cost == running_cost