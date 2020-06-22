from src.ingredients import Ingredient
from src.side import Fries, Nuggets
from src.drink import Drink
from src.sundae import Sundae

class Inventory():
    def __init__(self):
        self._ingredients = {}
        self._sides = {}
        self._drinks = {}
        self._sundaes = {}
    
    #search through dictionary of items
    def remove_ingredient(self, ingredient):
        self._ingredients[ingredient.i_type][ingredient.name] -= ingredient.amount
    
    def remove_side(self, side):
        self._sides[side.name] -= side.get_amount()
    
    def remove_drink(self, drink):
        self._drinks[drink.name][drink.drink_type] -= drink.amount
    
    def remove_sundae(self, sundae):
        self._sundaes[sundae.flavour][sundae.size] -= sundae.amount