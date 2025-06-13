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
        """
        Build a Pizza with one crust, one cheese, multiple sauces, and multiple toppings.

        :param crust: The type of crust (e.g., 'thin', 'thick', 'gluten_free')
        :type crust: str
        :param sauce: List of sauces to add to the pizza
        :type sauce: list[str]
        :param toppings: List of toppings to add to the pizza
        :type toppings: list[str]
        :param cheese: The type of cheese, defaults to 'mozzarella'
        :type cheese: str, optional
        """
        self.crust = crust
        self.cheese = cheese
        self.sauce = sauce
        self.toppings = toppings

        self.ingredients = [("crust", crust), ("cheese", cheese), *[("sauce", s) for s in sauce], *[("toppings", t) for t in toppings]]

    def __str__(self):
        """
        Return a string representation of the pizza, including all ingredients and total cost.

        :return: String describing the pizza and its cost
        :rtype: str
        """
        crust = self.crust
        cheese = self.cheese
        sauces = [s for s in self.sauce]
        toppings = [t for t in self.toppings]

        return f"Crust: {crust}, Sauce: {sauces}, Cheese: {cheese}, Toppings: {toppings}, Cost: {self.cost()}"

    def cost(self) -> int:
        """
        Calculate the total cost of the pizza based on the cost_structure.

        :return: The total cost of the pizza
        :rtype: int
        """
        self.total_cost = 0

        try:
            for type, ingredient in self.ingredients:
                formatted_ingredient = ingredient.replace(" ", "_").lower()
                ingredient_cost = self.cost_structure[type][formatted_ingredient]
                self.total_cost += ingredient_cost
        except KeyError as e:
            print("Unknown ingredient", e)

        return self.total_cost