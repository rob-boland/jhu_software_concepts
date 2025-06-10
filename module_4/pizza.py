

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
        "topping": {
            "pineapple": 1,
            "pepperoni": 2,
            "mushrooms": 3
        },
        "chesse": {
            "mozzarella": 1
        }
    }
    def __init__(self, crust:str, sauce:str, cheese:str, toppings:str):
        self.ingredients = {
            "crust": crust,
            "sauce": sauce,
            "cheese": cheese,
            "toppings": toppings
        }

    def __str__(self):
        pass

    def cost(self):
        self.total_cost = 0

        try:
            for type, ingredient in self.ingredients.items():
                formatted_ingredient = ingredient.replace(" ", "_").lower()
                ingredient_cost = self.cost_structure[type][ingredient]
                self.total_cost += ingredient_cost

