# Name: Jon Robert N. Boland (jboland7)

# Module Info: Module 4 - Pizza Ordering System

This module provides a simple Python package for modeling a pizza ordering system. It includes classes for creating pizzas with customizable ingredients and for managing customer orders, including cost calculation and payment tracking.

## Project Structure

```
module_4/
├── order.py         # Defines the Order class for managing pizza orders
├── pizza.py         # Defines the Pizza class for building pizzas and calculating cost
├── requirements.txt # Python dependencies
├── tests/           # Unit and integration tests for the pizza and order modules
```

## Features

- **Custom Pizza Creation:** Build pizzas with various crusts, sauces, cheeses, and toppings.
- **Order Management:** Add multiple pizzas to an order, track total cost, and manage payments.
- **Cost Calculation:** Automatically calculates the cost of each pizza and the total order.
- **Payment Tracking:** Supports partial and full payments, and checks if the order is fully paid.
- **Test Coverage:** Includes unit and integration tests for both pizza and order logic.

## Installation

1. **Clone the repository:**
   ```powershell
   git clone git@github.com:rob-boland/jhu_software_concepts.git
   cd <repository directory>/module_4
   ```

2. **(Recommended) Create and activate a virtual environment:**
   ```powershell
   python -m venv env
   # On Windows:
   .\env\Scripts\activate
   # On macOS/Linux:
   source env/bin/activate
   ```

3. **Install dependencies:**
   ```powershell
   pip install -r <repository directory>/module_4/requirements.txt
   ```

## Usage

### Create a Pizza
```python
from pizza import Pizza
pizza = Pizza("thin", ["pesto"], ["mushrooms"], "mozzarella")
print(pizza)  # Shows ingredients and cost
```

### Create and Manage an Order
```python
from order import Order
order = Order()
order.input_pizza("thin", ["pesto"], ["mushrooms"], "mozzarella")
order.input_pizza("thick", ["marinara"], ["pepperoni"], "mozzarella")
print(order)  # Shows all pizzas in the order and total cost
order.pay_for_order(20)
print(order.order_paid())  # Checks if the order is fully paid
```

### Run Tests
```powershell
cd <repository directory>
pytest
```

## Customization
- Add new crusts, sauces, toppings, or cheeses by editing the `cost_structure` in `pizza.py`.
- Extend the `Order` class to support discounts, delivery, or other features as needed.
- Add more tests in the `tests/` directory to cover additional scenarios.

## Notes
- The modules are designed to be run both as scripts and as part of a package.
- The import logic in `order.py` allows for flexible usage in different environments.

## Approach
- **pizza.py:** Defines the `Pizza` class, which models a pizza and calculates its cost based on selected ingredients.
- **order.py:** Defines the `Order` class, which manages a list of pizzas, tracks the total cost, and handles payments.
- **tests/**: Contains unit and integration tests to ensure correct behavior of pizza creation, order management, and cost calculation.

## Known Bugs and Limitations
- **Ingredient Validation:** Unknown ingredients will print a warning but do not raise an error.