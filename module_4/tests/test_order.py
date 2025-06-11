import pytest

# Intra-package imports
from module_4.order import Order
from module_4.pizza import Pizza

@pytest.fixture
def example_pizza_data():
    """List of pizzas for use in building test orders."""
    [
        {
            "crust": "thin",
            "sauce": ["pesto"],
            "toppings": ["mushrooms"],
            "cheese": "mozzarella"
        },
        {
            "crust": "chick",
            "sauce": ["marinara"],
            "toppings": ["mushrooms"],
            "cheese": "mozzarella"
        },
        {
            "crust": "gluten_free",
            "sauce": ["marinara"],
            "toppings": ["pineapple"],
            "cheese": "mozzarella"
        },
        {
            "crust": "thin",
            "sauce": ["liv_sauce", "pesto"],
            "toppings": ["mushrooms", "pepperoni"],
            "cheese": "mozzarella"
        }
    ]

def test_order_init():
    blank_order = Order()
    assert blank_order.cart == list()
    assert blank_order.cost == 0
    assert not blank_order.order_paid()