from src.order import Order
from src.side import Nuggets, Fries
from src.drink import Drink
from src.main import Main
from src.sundae import Sundae
from src.ingredients import Ingredient
import pickle

def pickle_ingredients():
    outfile = open('g_ingredients', 'wb')
    pickle.dump(g_ingredients, outfile)
    outfile.close()

def pickle_sides():
    outfile = open('g_sides', 'wb')
    pickle.dump(g_sides, outfile)
    outfile.close()

def pickle_drinks():
    outfile = open('g_drinks', 'wb')
    pickle.dump(g_drinks, outfile)
    outfile.close()

def pickle_sundaes():
    outfile = open('g_sundaes', 'wb')
    pickle.dump(g_sundaes, outfile)
    outfile.close()

# g_ indicated global variables
filename = 'g_ingredients'
try:
    infile = open(filename, 'rb')
    g_ingredients = pickle.load(infile)
    infile.close()
except:
    ingredients_gen = [["sesame", "bun", "Sesame Bun", 52, 1.5], ["plain", "wrap", "Plain Wrap", 42, 2.0], ["vegetarian", "patty", "Vegetarian Patty", 35, 3.0], ["beef", "patty", "Beef Patty", 84, 3.0], ["lettuce", "vegetable", "Lettuce", 84, 0.5], ["tomato", "vegetable", "Tomato", 84, 1.0], ["tomato", "sauce", "Tomato Sauce", 84, 0.5], ["cheddar", "cheese", "Cheddar Cheese", 84, 1.0]]
    
    g_ingredients = []

    # create ingredients list with amount left, name and price
    # customer and ordering_system will access this list
    for i_gen in ingredients_gen:
        g_ingredients.append(Ingredient(i_gen[0], i_gen[1], i_gen[2], i_gen[3], i_gen[4]))
    
    pickle_ingredients()

filename = 'g_sides'
try:
    infile = open(filename, 'rb')
    g_sides = pickle.load(infile)
    infile.close()
except:
    g_sides = [Nuggets(342), Fries(amount=18000)]
    pickle_sides()

filename = 'g_drinks'
try:
    infile = open(filename, 'rb')
    g_drinks = pickle.load(infile)
    infile.close()
except:
    g_drinks = [Drink("pepsi", "can", 134), Drink("pepsi", "bottle", 34), Drink("sprite", "can", 134), Drink("sprite", "bottle", 231), Drink("orange juice", "", 65000)] 
    pickle_drinks()

filename = 'g_sundaes'
try:
    infile = open(filename, 'rb')
    g_sundaes = pickle.load(infile)
    infile.close()
except:
    g_sundaes = [Sundae("chocolate", "small", 200), Sundae("chocolate", "medium", 200), Sundae("chocolate", "large", 200)]
    pickle_sundaes()

g_inventory = g_ingredients + g_sides + g_drinks + g_sundaes

# Generate a unique ID for each item in the inventory
for x in range(len(g_inventory)):
    g_inventory[x].inv_id = x


def has_ingredients(main, ingredients):
    for ingredient in main.ingredients:
        matches = [x for x in ingredients if x.name == ingredient.name and x.i_type == ingredient.i_type]

        if len(matches) != 1:
            return False

        if matches[0].amount < ingredient.amount:
            return False
    
    return True


def take_ingredients(main, ingredients):
    for ingredient in main.ingredients:
        matches = [x for x in ingredients if x.name == ingredient.name and x.i_type == ingredient.i_type]

        matches[0].amount -= ingredient.amount

        pickle_ingredients()

    return True

def add_ingredients(main, ingredients):
    for ingredient in main.ingredients:
        matches = [x for x in ingredients if x.name == ingredient.name and x.i_type == ingredient.i_type]

        matches[0].amount += ingredient.amount

    pickle_ingredients()

    return True

def has_side(side, sides):
    matches = [x for x in sides if type(x) == type(side)]

    if len(matches) != 1:
        return False

    if matches[0].amount < side.amount:
        return False

    return True

def take_side(side, sides):
    matches = [x for x in sides if type(x) == type(side)]

    matches[0].amount -= side.amount

    pickle_sides()

    return True

def add_side(side, sides):
    matches = [x for x in sides if type(x) == type(side)]

    matches[0].amount += side.amount

    pickle_sides()

    return True

# Values {inv_id: new_number}
def update_inventory(values, inventory):
    for inv_id, new_amount in values.items():
        for inv in inventory:
            if inv.inv_id == inv_id:
                inv.amount = new_amount

                continue
        
def has_drink(drink, drinks):
    if drink.drink_type == "can" or drink.drink_type == "bottle":
        matches = [x for x in drinks if x.name == drink.name and x.drink_type == drink.drink_type]
    else:
        matches = [x for x in drinks if x.name == drink.name]

    if len(matches) != 1:
        return False

    if matches[0].amount < drink.amount:
        return False

    return True

def take_drink(drink, drinks):
    if drink.drink_type == "can" or drink.drink_type == "bottle":
        matches = [x for x in drinks if x.name == drink.name and x.drink_type == drink.drink_type]
    else:
        matches = [x for x in drinks if x.name == drink.name]

    matches[0].amount -= drink.amount

    pickle_drinks()

    return True

def add_drink(drink, drinks):
    if drink.drink_type == "can" or drink.drink_type == "bottle":
        matches = [x for x in drinks if x.name == drink.name and x.drink_type == drink.drink_type]
    else:
        matches = [x for x in drinks if x.name == drink.name]

    matches[0].amount += drink.amount

    pickle_drinks()

    return True

def has_sundae(sundae, sundaes):
    matches = [x for x in sundaes if x.flavour == sundae.flavour and x.size == sundae.size]

    if len(matches) != 1:
        return False
    
    if matches[0].amount < sundae.amount:
        return False
    
    return True

def take_sundae(sundae, sundaes):
    matches = [x for x in sundaes if x._flavour == sundae._flavour and x._size == sundae._size]

    matches[0]._amount -= sundae._amount

    pickle_sundaes()

    return True

def add_sundae(sundae, sundaes):
    matches = [x for x in sundaes if x._flavour == sundae.flavour and x.size == sundae._size]

    matches[0]._amount += sundae._amount

    pickle_sundaes()

    return True

class OrderingSystem():
    def __init__(self):
        self._orders = []
        self._completed_orders = []
        
    @property
    def orders(self):
        return self._orders
    @property
    def completed_orders(self):
        return self._completed_orders

    def get_order_by_id(self, order_id):
        for o in self._orders:
            if order_id == o.order_id:
                return o

        for o in self._completed_orders:
            if order_id == o.order_id:
                return o
        # else fail ???? TODO
        return None

    def add_order(self, order):
        e1 = [x for x in order.mains if not has_ingredients(x, g_ingredients)]
        e2 = [x for x in order.sides if not has_side(x, g_sides)]
        e3 = [x for x in order.drinks if not has_drink(x, g_drinks)]

        if (len(e1) > 0 or len(e2) > 0 or len(e3) > 0): 
            raise Exception("Not enough ingredients available.")
        
        [take_ingredients(x, g_ingredients) for x in order.mains]
        [take_side(x, g_sides) for x in order.sides]
        [take_drink(x, g_drinks) for x in order.drinks]
        [take_sundae(x, g_sundaes) for x in order.sundaes]
        self._orders.append(order)

        return True

    def complete_order(self, order_id):
        for o in self._orders:
            if o.order_id == order_id:
                o.completed = True
                self._completed_orders.append(o)
                self._orders.remove(o)
       
    def cancel_order(self, order_id):
        for o in self._orders:
            if o.order_id == order_id:
                o.completed = True
                self._orders.remove(o)
                [add_ingredients(x, g_ingredients) for x in o.mains]
                [add_side(x, g_sides) for x in o.sides]
                [add_drink(x, g_drinks) for x in o.drinks]

    def displayIngredients(self, i_type):
        for x in ingredients:
            if x.i_type == i_type:
                print(x.name)        

