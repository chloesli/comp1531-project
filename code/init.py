from src.ordering_system import g_ingredients, g_sides, g_drinks, OrderingSystem
from src.order import Order
from src.side import Nuggets, Fries
from src.drink import Drink
from src.main import Main

from copy import deepcopy

# TODO __str__ large fries

def bootstrap_system():
    system = OrderingSystem()
    
    order1 = Order()
    
    custom_ingredients = deepcopy(g_ingredients)

    custom_ingredients = [x for x in custom_ingredients if x.i_type != "wrap"]
    for i in custom_ingredients:
        i.amount = 1

    main1 = Main("burger", custom_ingredients)
    order1.add_main(main1)

    nuggets1 = Nuggets(6)
    order1.add_side(nuggets1)

    fries1 = Fries("large")
    order1.add_side(fries1)

    drink1 = Drink("pepsi", "can", 2)
    order1.add_drink(drink1)

    system.add_order(order1)

    order2 = Order()
    order2.add_main(main1)
    order2.add_side(nuggets1)
    order2.add_side(fries1)
    order2.add_drink(drink1)

    system.add_order(order2)

    return system
