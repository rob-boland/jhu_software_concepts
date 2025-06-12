import pytest

# Intra-package imports
from module_4.order import Order
from module_4.pizza import Pizza

@pytest.fixture
def example_orders():
    """Returns two Order objects: the first with pizzas 0 and 1, the second with pizzas 2 and 3 from pizza_list."""
    pizza_list = [
        {
            "crust": "thin",
            "sauce": ["pesto"],
            "toppings": ["mushrooms"],
            "cheese": "mozzarella"
        },
        {
            "crust": "thick",
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
    order_0 = Order()
    order_0.input_pizza(
        crust=pizza_list[0]["crust"], sauce=pizza_list[0]["sauce"], toppings=pizza_list[0]["toppings"], cheese=pizza_list[0]["cheese"]
    )
    order_0.input_pizza(
        crust=pizza_list[1]["crust"], sauce=pizza_list[1]["sauce"], toppings=pizza_list[1]["toppings"], cheese=pizza_list[1]["cheese"]
    )


    order_1 = Order()
    order_1.input_pizza(
        crust=pizza_list[2]["crust"], sauce=pizza_list[2]["sauce"], toppings=pizza_list[2]["toppings"], cheese=pizza_list[2]["cheese"]
    )
    order_1.input_pizza(
        crust=pizza_list[3]["crust"], sauce=pizza_list[3]["sauce"], toppings=pizza_list[3]["toppings"], cheese=pizza_list[3]["cheese"]
    )

    return order_0, order_1


def test_order_init():
    blank_order = Order()
    assert blank_order.cart == list()
    assert blank_order.cost == 0
    assert not blank_order.order_paid()

def test_order__str__(example_orders):
    # Test against pizzas given in assignment instructions
    assert str(example_orders[0]) == \
    "Customer Requested:\nCrust: thin, Sauce: ['pesto'], Cheese: mozzarella, Toppings: ['mushrooms'], Cost: 11\nCrust: thick, Sauce: ['marinara'], Cheese: mozzarella, Toppings: ['mushrooms'], Cost: 11"
    assert str(example_orders[1]) == \
    "Customer Requested:\nCrust: gluten_free, Sauce: ['marinara'], Cheese: mozzarella, Toppings: ['pineapple'], Cost: 11\nCrust: thin, Sauce: ['liv_sauce', 'pesto'], Cheese: mozzarella, Toppings: ['mushrooms', 'pepperoni'], Cost: 18"

def test_input_pizza_updates_cost():
    order = Order()
    # Add a pizza with known cost: thin (5) + pesto (3) + mozzarella (0) + mushrooms (3) = 11
    order.input_pizza(crust="thin", sauce=["pesto"], toppings=["mushrooms"], cheese="mozzarella")
    assert order.cost == 11
    # Add another pizza: thick (6) + marinara (2) + mozzarella (0) + mushrooms (3) + pineapple (1) = 12
    order.input_pizza(crust="thick", sauce=["marinara"], toppings=["mushrooms", "pineapple"], cheese="mozzarella")
    assert order.cost == 23

def test_order_paid_behavior():
    order = Order()
    # Add a pizza with cost 11
    order.input_pizza(crust="thin", sauce=["pesto"], toppings=["mushrooms"], cheese="mozzarella")
    # Not paid yet
    assert not order.order_paid()
    # Pay less than total
    order.pay_for_order(5)
    assert not order.order_paid()
    # Pay the rest
    order.pay_for_order(6)
    assert order.order_paid()