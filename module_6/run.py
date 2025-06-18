"""
order.py

This module defines the Order class for managing pizza orders in a pizza ordering system.
It provides functionality to add pizzas to an order, calculate the total cost, track payments,
and represent the order as a string. The Order class integrates with the Pizza class to build
customized pizzas and manage multiple pizzas within a single order.

Classes:
    Order: Represents a customer's pizza order, including cart management, cost calculation,
           and payment tracking.
"""

import boland_website

if __name__ == "__main__":
    # Create Flask app, run with localhost:5000 address.
    app = boland_website.create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
