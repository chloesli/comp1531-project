from src.order import Order
from src.side import Fries
from src.drink import Drink
from src.main import Main
from src.ingredients import Ingredient
from src.side import Side, Nuggets, Fries
from src.sundae import Sundae
from src.ordering_system import g_ingredients, g_sides, g_drinks, OrderingSystem
from copy import deepcopy
import pytest


@pytest.fixture
def os():
    os = OrderingSystem()
    
    return os

# ===== FUNCTION THAT RETURNS THE AMOUNT OF INVENTORY LEFT FOR A SIDE =====
def side_quantity(side):
    find = [x for x in g_sides if type(x) == type(side)]
    return find[0].amount

# ===== FUNCTION THAT RETURNS THE AMOUNT OF INVENTORY LEFT FOR A DRINK =====
def drink_quantity(name, dtype):
    find = [x for x in g_drinks if x.name == name and x.drink_type == dtype]
    return find[0].amount

# ===== FUNCTION THAT RETURNS THE AMOUNT OF INVENTORY LEFT FOR AN INGREDIENT =====
def ing_quantity(name, itype):
    find = [x for x in g_ingredients if x.name == name and itype == itype]
    return find[0].amount

# ===== CREATING LIST OF BURGER INGREDIENTS =====
b_ingres = []
x1 = Ingredient("sesame", "bun", 3, 1.5)
x2 = Ingredient("beef", "patty", 2, 3.0)
x3 = Ingredient("tomato", "vegetable", 2, 0.5)
x4 = Ingredient("cheddar", "cheese", 2, 1)
x5 = Ingredient("tomato", "sauce", 2, 0.5)
for x in [x1, x2, x3, x4, x5]:
    b_ingres.append(x)

def test_completed(os):
  
    # ===== CREATING 3 ORDERS =====

    order1 = Order()
    m = Main("burger", b_ingres)
    order1.add_main(m)
    os.add_order(order1)

    order2 = Order()
    order2.add_main(m)
    os.add_order(order2)

    order3 = Order()
    order3.add_main(m)
    os.add_order(order3)

    assert len(os._orders) == 3

    # ===== COMPLETING ORDERS =====
    os.complete_order(order1._order_id)
    assert len(os._orders) == 2
    assert len(os._completed_orders) == 1
    os.complete_order(order3._order_id)
    assert len(os._orders) == 1
    assert len(os._completed_orders) == 2
    os.complete_order(order2._order_id)
    assert len(os._orders) == 0
    assert len(os._completed_orders) == 3

def test_cancel(os):
    # ===== CREATING 3 ORDERS =====

    order1 = Order()
    m = Main("burger", b_ingres)
    order1.add_main(m)
    os.add_order(order1)

    order2 = Order()
    order2.add_main(m)
    os.add_order(order2)

    order3 = Order()
    order3.add_main(m)
    os.add_order(order3)

    # ==== CANCELLING 3 ORDERS ====
    os.cancel_order(order1._order_id)
    assert len(os._orders) == 2
    assert len(os._completed_orders) == 0
    os.cancel_order(order3._order_id)
    assert len(os._orders) == 1
    assert len(os._completed_orders) == 0
    os.cancel_order(order2._order_id)
    assert len(os._orders) == 0
    assert len(os._completed_orders) == 0

def test_order_status(os):
    # ===== CREATING 3 ORDERS =====

    order1 = Order()
    m = Main("burger", b_ingres)
    order1.add_main(m)
    os.add_order(order1)
    
    order2 = Order()
    order2.add_main(m)
    os.add_order(order2)

    order3 = Order()
    order3.add_main(m)
    os.add_order(order3)    
    
    # ===== COMPLETING ORDERS =====
    assert order3._completed == False
    os.complete_order(order1._order_id)
    assert len(os._orders) == 2
    assert len(os._completed_orders) == 1
    assert order1._completed == True

    assert order3._completed == False
    os.complete_order(order3._order_id)
    assert len(os._orders) == 1
    assert len(os._completed_orders) == 2
    assert order3._completed == True

    assert order2._completed == False
    os.complete_order(order2._order_id)
    assert len(os._orders) == 0
    assert len(os._completed_orders) == 3
    assert order2._completed == True

def test_cancel_main(os):
# ===== MAKE LIST OF INGREDIENTS =====
    b_ingres = []
    x1 = Ingredient("sesame", "bun", "sesame bun", 3, 1.5)
  
    x2 = Ingredient("beef", "patty", "beef patty", 2, 3.0)

    x3 = Ingredient("tomato", "vegetable", "tomato", 2, 0.5)

    x4 = Ingredient("cheddar", "cheese", "cheddar cheese", 2, 1)
 
    x5 = Ingredient("tomato", "sauce", "tomato sauce", 2, 0.5)

    for x in [x1, x2, x3, x4, x5]:
        b_ingres.append(x)

    # ===== STORE CURRENT INVENTORY LEVELS =====
    bunQ = ing_quantity("sesame", "bun")
    pattyQ = ing_quantity("beef", "patty")
    vegQ = ing_quantity("tomato", "vegetable")
    cheQ = ing_quantity("cheddar", "cheese")
    sauQ = ing_quantity("tomato", "sauce")
    # ===== ORDER A MAIN =====
    order1 = Order()
    m1 = Main("burger", b_ingres)
    order1.add_main(m1)
    os.add_order(order1)

    assert len(os._orders) == 1
    assert order1.calculate_price() == 14.5
    assert len(order1.mains) == 1
    assert len(order1.mains[0]._ingredients) == 5

    # ===== MAKE SURE INVENTORY UPDATED CORRECTLY =====
    assert ing_quantity("sesame", "bun") == bunQ - 3
    assert ing_quantity("beef", "patty") == pattyQ - 2
    assert ing_quantity("tomato", "vegetable") == vegQ - 2
    assert ing_quantity("cheddar", "cheese") == cheQ - 2
    assert ing_quantity("tomato", "sauce") == sauQ - 2

    os.cancel_order(order1._order_id)
    # ===== IF AN ORDER IS CANCELLED MAKE SURE THE INGREDIENTS ARE PUT BACK IN THE INVENTORY SYSTEM =====
    assert ing_quantity("sesame", "bun") == bunQ 
    assert ing_quantity("beef", "patty") == pattyQ 
    assert ing_quantity("tomato", "vegetable") == vegQ 
    assert ing_quantity("cheddar", "cheese") == cheQ 
    assert ing_quantity("tomato", "sauce") == sauQ 

def test_cancel_nuggets(os):
    # ===== ORDERING 3 NUGGETS =====
    order1 = Order()
    originalq = nuggetq = side_quantity(Nuggets(3))
    nuggetq = side_quantity(Nuggets(3))
    order1.add_side(Nuggets(3))

    assert order1.calculate_price() == 3
    assert os.add_order(order1) == True
    assert side_quantity(Nuggets(3)) == nuggetq - 3

    # ===== ORDERING 6 NUGGETS =====
    order2 = Order()
    nuggetq = side_quantity(Nuggets(6))
    order2.add_side(Nuggets(6))

    assert order2.calculate_price() == 4.50
    assert os.add_order(order2) == True
    assert side_quantity(Nuggets(6)) == nuggetq - 6
    assert len(os._orders) == 2
    
    # ===== TESTING CANCEL ORDER UPDATES INVENTORY CORRECTLY =====
    os.cancel_order(order1._order_id)
    assert side_quantity(Nuggets(6)) == nuggetq - 3
    os.cancel_order(order2._order_id)
    assert side_quantity(Nuggets(6)) == originalq


def test_cancel_fries(os):
    # ===== ORDERING SMALL FRIES =====
    order1 = Order()
    friesQ = side_quantity(Fries(""))
    order1.add_side(Fries("small"))

    assert order1.calculate_price() == 2
    assert os.add_order(order1) == True
    assert side_quantity(Fries("")) == friesQ - 250

    os.cancel_order(order1.order_id)
    assert side_quantity(Fries("")) == friesQ 

def test_cancel_drinks(os):
    # ===== ORDERING SMALL OJ =====
    order1 = Order()
    ojQ = drink_quantity("orange juice", "")  
    order1.add_drink(Drink("orange juice", "small", 250)) 

    assert order1.calculate_price() == 2
    assert os.add_order(order1) == True
    assert drink_quantity("orange juice", "") == ojQ - 250

    os.cancel_order(order1.order_id)
    assert drink_quantity("orange juice", "") == ojQ 
