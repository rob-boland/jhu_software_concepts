# Intra-package imports
from pizza import Pizza

class Order:
    def __init__(self):
        """
        Initialize an Order with a cost of $0 and an empty cart.
        """
        # Cost is total cost of order. Balance is debt customer owes
        self.cost = 0
        self.balance = 0
        self.cart = list()
        self.payment_made = False

    def __str__(self):
        """
        Return a string representation of the order, including all pizzas in the cart.

        :return: String listing all pizzas in the order
        :rtype: str
        """
        pizzas_str = "\n".join([str(pizza) for pizza in self.cart])
        return f"Customer Requested:\n{pizzas_str}"

    def input_pizza(self, crust:str, sauce:list[str], toppings:list[str], cheese:str="mozzarella"):
        """
        Add a pizza to the order with the specified ingredients.

        :param crust: The type of crust for the pizza
        :type crust: str
        :param sauce: List of sauces for the pizza
        :type sauce: list[str]
        :param toppings: List of toppings for the pizza
        :type toppings: list[str]
        :param cheese: The type of cheese, defaults to 'mozzarella'
        :type cheese: str, optional
        """
        pizza = Pizza(crust, sauce, toppings, cheese)
        self.cart.append(pizza)

        # Compute pizza's cost. Add cost to total order cost and subtract from order balance
        pizza.cost()
        self.cost += pizza.total_cost
        self.balance -= pizza.total_cost

    def pay_for_order(self, payment:int) -> int:
        """
        Add a payment to the order and update the balance.

        :param payment: The amount paid by the customer
        :type payment: int
        :return: The updated balance after payment
        :rtype: int
        """
        self.balance += payment
        self.payment_made = True

        return self.balance

    def order_paid(self) -> bool:
        """
        Check if the order has been fully paid.

        :return: True if the balance is zero and payment has been made, False otherwise
        :rtype: bool
        """
        if self.balance == 0 and self.payment_made:
            self.paid = True
        else:
            print(f"Please pay {self.balance} to close out your order!")
            self.paid = False
        return self.paid