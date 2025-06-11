class Pizza:
    cost_structure = {
        "crust": {
            "thin": 5,
            "thick": 6,
            "gluten_free": 8
        },
        "sauce": {
            "marinara": 2,
            "pesto": 3,
            "liv_sauce": 5
        },
        "toppings": {
            "pineapple": 1,
            "pepperoni": 2,
            "mushrooms": 3
        },
        "cheese": {
            "mozzarella": 0
        }
    }
    def __init__(self, crust:str, sauce:list[str], toppings:list[str], cheese:str="mozzarella"):
        """Build Pizza with one crust, one cheese, multiple sauces, and multiple toppings.

        Args:
            crust (str): The type of crust (e.g., 'thin', 'thick', 'gluten_free').
            sauce (list[str]): List of sauces to add to the pizza.
            cheese (str): The type of cheese (e.g., 'mozzarella').
            toppings (list[str]): List of toppings to add to the pizza.
        """
        self.crust = ("crust", crust)
        self.cheese = ("cheese", cheese)
        self.sauce = [("sauce", s) for s in sauce]
        self.toppings = [("toppings", t) for t in toppings]

        self.ingredients = [self.crust, self.cheese, *self.sauce, *self.toppings]

        self.total_cost = self.cost()

    def __str__(self):
        return f"Crust: {self.crust}, Sauce: {self.sauce}, Cheese: {self.cheese}, Toppings: {self.toppings}, Cost: {self.cost()}"

    def cost(self) -> int:
        """Calculate the total cost of the pizza based on the cost_structure.

        Returns:
            total_cost (int): The total cost of the pizza.
        """
        total_cost = 0

        try:
            for type, ingredient in self.ingredients:
                formatted_ingredient = ingredient.replace(" ", "_").lower()
                ingredient_cost = self.cost_structure[type][formatted_ingredient]
                total_cost += ingredient_cost
        except KeyError as e:
            print("Unknown ingredient", e)

        return total_cost