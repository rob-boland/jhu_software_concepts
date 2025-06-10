

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
    def __init__(self, crust:str, sauce:list[str], cheese:str, toppings:list[str]):
        """Build Pizza with one crust, one cheese, multiple sauces, and multiple toppings"""
        self.crust = ("crust", crust)
        self.cheese = ("cheese", cheese)
        self.sauce = [("sauce", s) for s in sauce]
        
        self.toppings = [("toppings", t) for t in toppings]

        self.ingredients = [self.crust, self.cheese, *self.sauce, *self.toppings]

    def __str__(self):
        crust = self.crust[1].title()
        cheese = self.cheese[1].title()
        sauces = [s[1].title() for s in self.sauce]
        toppings = [t[1].title() for t in self.toppings]
        return f"Crust: {crust}, Cheese: {cheese}, Sauce(s): {sauces}, Topping(s): {toppings}\nTotal cost: ${self.cost()}"


    def cost(self) -> int:
        self.total_cost = 0

        try:
            for type, ingredient in self.ingredients:
                formatted_ingredient = ingredient.replace(" ", "_").lower()
                ingredient_cost = self.cost_structure[type][formatted_ingredient]
                self.total_cost += ingredient_cost
        except KeyError as e:
            print("Unknown ingredient", e)

        return self.total_cost

pizza_0 = Pizza("thin", ["Liv Sauce", "marinara"], "mozzarella", ["pepperoni", "mushrooms"])
print(pizza_0)

