import pytest

# Intra-package imports
from module_4.pizza import Pizza

# Test Pizza.__init__ with valid data types
@pytest.mark.parametrize("crust,sauce,cheese,toppings", [
    ("thin", ["pesto"], "mozzarella", ["mushrooms"]),
    ("thick", ["marinara"], "mozzarella", ["mushrooms", "pineapple"]),
    ("gluten_free", ["marinara", "pesto"], "mozzarella", ["pepperoni"]),
])
def test_pizza_init_types(crust, sauce, cheese, toppings):
    pizza = Pizza(crust, sauce, toppings, cheese)
    assert pizza.crust == crust
    assert pizza.sauce == sauce
    assert pizza.cheese == cheese
    assert pizza.toppings == toppings

# Test Pizza.__str__ output format
def test_pizza_str_format():
    pizza = Pizza("thin", ["pesto"], ["mushrooms"], "mozzarella")
    expected = "Crust: thin, Sauce: ['pesto'], Cheese: mozzarella, Toppings: ['mushrooms'], Cost: 11"
    assert str(pizza) == expected

# Test Pizza.cost() returns correct cost
@pytest.mark.parametrize("crust,sauce,cheese,toppings,expected_cost", [
    ("thin", ["pesto"], "mozzarella", ["mushrooms"], 11),
    ("thick", ["marinara"], "mozzarella", ["mushrooms", "pineapple"], 12),
    ("gluten_free", ["marinara", "pesto"], "mozzarella", ["pepperoni"], 15),
    ("thin", ["liv_sauce", "marinara"], "mozzarella", ["pepperoni", "mushrooms"], 17),
])
def test_pizza_cost(crust, sauce, cheese, toppings, expected_cost):
    pizza = Pizza(crust, sauce, toppings, cheese)
    assert pizza.cost() == expected_cost
