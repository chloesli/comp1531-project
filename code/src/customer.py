from src.order import Order
from src.side import Fries
from src.drink import Drink
from src.main import Main
from src.ingredients import Ingredient
from src.side import Side, Nuggets, Fries
from src.sundae import Sundae
from src.ordering_system import g_ingredients, g_sides, g_drinks, OrderingSystem

from copy import deepcopy


def orderFries():
    size = int(input("Size? \n1. Small\n2. Medium \n3. Large\n"))

    if (size == 1):
        fries = Fries("small")

    elif (size == 2):
        fries = Fries("medium")

    elif (size == 3):
        fries = Fries("large")

    else: 
        fries = None
        
    return fries


def orderNuggets():
    amount = int(input("Pack \n1. 3-Pack\n2. 6-Pack\n"))

    if (amount == 1):
        nuggets = Nuggets(3)

    elif (amount == 2):
        nuggets = Nuggets(6)

    else: 
        nuggets = None
    
    return nuggets


def orderDrink():
    drinks = [str(x) for x in g_drinks]
    print("Which drink would you like?")

    for d in range(0, len(drinks)):
        print("{} - {}".format(d + 1, str(drinks[d])))
    
    choice = int(input())

    drink = deepcopy(g_drinks)[choice - 1]

    if (drink.drink_type == "bottle" or drink.drink_type == "can"):
        drink.amount = 1 

    else:
        size_i = int(input("What size? \n1. Small\n2. Medium\n3. Large\n"))

        if (size_i == 1):
            drink.drink_type = "small"
            drink.amount = 250

        elif (size_i == 2):
            drink.drink_type = "medium"
            drink.amount = 450

        elif (size_i == 3):
            drink.drink_type = "large"
            drink.amount = 650

        else:
            drink = None

    return drink

def createMain(main_type):
    print("\nWhat would you like in your %s?\n" % main_type)

    custom_ingredients = deepcopy(g_ingredients)

    if (main_type == "burger"):
        custom_ingredients = [x for x in custom_ingredients if x.i_type != "wrap"]
    else:
        custom_ingredients = [x for x in custom_ingredients if x.i_type != "bun"]

    for x in custom_ingredients:
        x.amount = int(input("How many %s? " % x))
    
    
    m = Main(main_type, custom_ingredients)

    return m


if __name__ == "__main__":
    os = OrderingSystem()
    
    # Testing
    # print([str(x) for x in g_ingredients])
    # print([str(x) for x in g_sides])
    # print([str(x) for x in g_drinks])
    
    order1 = Order()
    
    main = int(input("Type the number of the item you would like to order:\n1. Burger\n2. Wrap\nI would like to order: "))
    
    if main == 1: 
        m1 = createMain("burger")
    
        order1.add_main(m1)
    
    elif main == 2: 
        m1 = createMain("wrap")
    
        order1.add_main(m1)
    else:
        raise Exception("Please enter a valid number")

    # Order sides
    sides = input("Would you like to order additional sides? (y/n): ")
    
    if sides.lower() == "y":
        fries = input("Would you like fries (y/n)? ")

        if fries.lower() == "y":
            fries = orderFries()

            order1.add_side(fries)
            

        nuggets = input("Would you like nuggets (y/n)? ")
        
        if nuggets.lower() == "y":
            nuggets = orderNuggets()

            order1.add_side(nuggets)
            

    drink = input("Would you like a drink (y/n)? ")

    if drink.lower() == "y":
        drink = orderDrink()

        order1.add_drink(drink)
    

    print("Your order subtotal: ${:0,.2f}".format(order1.calculate_price()))
    
    try:
        os.add_order(order1) 

    except:
        print("Could not add your order to queue, not enough ingredients available.")

    else:
        print("Order added to queue.")

    # When the order has been fuffiled by the chefs
    os.complete_order(order1)

    # Testing
    # print([str(x) for x in g_ingredients])
    # print([str(x) for x in g_sides])
    # print([str(x) for x in g_drinks])
    
