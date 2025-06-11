# Intra-package imports
from pizza import Pizza

class Order:
    def __init__(self):
        """
        Initialize an Order with a cost of $0 and an empty cart.

        Attributes:
            cost (int): Total cost of the order.
            balance (int): Debt the customer owes (negative if unpaid, positive if overpaid).
            cart (list): List of Pizza objects in the order.
        """
        # Cost is total cost of order. Balance is debt customer owes
        self.cost = 0
        self.balance = 0
        self.cart = list()

    def __str__(self):
        pizzas_str = "\n".join(self.cart)
        return f"{len(self.cart)} with a total cost of {self.cost}\n{pizzas_str}"

    def input_pizza(self, crust:str, sauce:list[str], toppings:list[str], cheese:str="mozzarella"):
        """Add a pizza to the order with the specified ingredients.

        Args:
            crust (str): The type of crust for the pizza.
            sauce (list[str]): List of sauces for the pizza.
            toppings (list[str]): List of toppings for the pizza.
            cheese (str, optional): The type of cheese. Defaults to 'mozzarella'.
        """
        pizza = Pizza(crust, sauce, toppings, cheese)
        self.cart.append(pizza)

        # Compute pizza's cost. Add cost to total order cost and subtract from order balance
        pizza.cost()
        self.cost += pizza.total_cost
        self.balance -= pizza.total_cost

    def pay_for_order(self, payment:int) -> int:
        """Add a payment to the order and update the balance.

        Args:
            payment (int): The amount paid by the customer.

        Returns:
            int: The updated balance after payment.
        """
        self.balance += payment

        return self.balance
    def order_paid(self) -> bool:
        """Check if the order has been fully paid.

        Returns:
            bool: True if the balance is zero, False otherwise.
        """
        if self.balance == 0:
            return True
        else:
            print(f"Please pay {self.balance} to close out your order!")
            return False