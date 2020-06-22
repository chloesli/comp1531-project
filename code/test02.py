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

# ===== FUNCTION THAT RETURNS THE AMOUNT OF INVENTORY LEFT FOR A DRINK =====
def drink_quantity(name, dtype):
    find = [x for x in g_drinks if x.name == name and x.drink_type == dtype]
    return find[0].amount

# ===== FUNCTION THAT RETURNS THE AMOUNT OF INVENTORY LEFT FOR A SIDE =====
def side_quantity(side):
    find = [x for x in g_sides if type(x) == type(side)]
    return find[0].amount

# ===== FUNCTION THAT RETURNS THE AMOUNT OF INVENTORY LEFT FOR AN INGREDIENT =====
def ing_quantity(name, itype):
    find = [x for x in g_ingredients if x.name == name and itype == itype]
    return find[0].amount

def test_make_full_order(os):
    # ===== MAKE A LIST OF INGREDIENTS AND MAKE A MAIN =====
    w_ingres = []
    x1 = Ingredient("plain", "wrap", "plain wrap", 1, 2)

    x2 = Ingredient("lettuce", "vegetable", "lettuce", 2, 0.5)

    x3 = Ingredient("tomato", "vegetable", "tomato", 2, 1)

    x4 = Ingredient("cheddar", "cheese", "cheddar cheese", 4, 1)

    for x in [x1, x2, x3, x4]:
        w_ingres.append(x)

    m1 = Main("wrap", w_ingres)

    # ===== STORE INVENTORY LEVELS =====
    wrapQ = ing_quantity("plain", "wrap")
    letQ = ing_quantity("lettuce", "vegetable")
    tomQ = ing_quantity("tomato", "vegetable")
    cheQ = ing_quantity("cheddar", "cheese")
    ojQ = drink_quantity("orange juice", "")  
    pepsi_q = drink_quantity("pepsi", "can")
    nuggetQ = side_quantity(Nuggets(6))
    friesQ = side_quantity(Fries(""))

    # ===== ADD MAIN, DRINK AND SIDES TO ORDER =====
    order1 = Order()
    order1.add_main(m1)
    order1.add_drink(Drink("orange juice", "small", 250)) 
    order1.add_drink(Drink("pepsi", "can", 2)) 
    order1.add_side(Fries("large"))
    order1.add_side(Nuggets(6))

    # ===== ADD ORDER TO ORDERING SYSTEM =====
    assert os.add_order(order1) == True
    # ===== ASSERT ORDER WAS LOGGED =====
    assert len(os._orders) == 1
    # ===== CHECK PRICE =====
    assert order1.calculate_price() == 21
    # ===== MAKE SURE CORRECT NUMBER OF ITEMS HAVE BEEN PUT INTO THE ORDER =====
    assert len(order1.mains) == 1
    assert len(order1.sides) == 2
    assert len(order1.drinks) == 2
    assert len(order1.mains[0]._ingredients) == 4

    # ===== MAKE SURE INVENTORY LEVELS WERE UPDATED CORRECTLY =====
    assert ing_quantity("plain", "wrap") == wrapQ - 1
    assert ing_quantity("lettuce", "vegetable") == letQ - 2
    assert ing_quantity("tomato", "vegetable") == tomQ - 2
    assert ing_quantity("cheddar", "cheese") == cheQ - 4
    assert side_quantity(Nuggets(6)) == nuggetQ - 6
    assert side_quantity(Fries("")) == friesQ - 640
    assert drink_quantity("orange juice", "") == ojQ - 250
    assert drink_quantity("pepsi", "can") == pepsi_q - 2

def test_order_main(os):
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

def test_order_two(os):
    b_ingres = []
    x1 = Ingredient("sesame", "bun", "sesame bun", 3, 1.5)
    
    x2 = Ingredient("beef", "patty", "beef patty", 2, 3.0)
    
    x3 = Ingredient("tomato", "vegetable", "tomato", 2, 0.5)
    
    x4 = Ingredient("cheddar", "cheese", "cheddar cheese", 2, 1)
    
    for x in [x1, x2, x3, x4]:
        b_ingres.append(x)
    # ===== ORDER 1ST MAIN =====
    order1 = Order()
    m1 = Main("burger", b_ingres)
    order1.add_main(m1)

    assert os.add_order(order1) == True
    assert len(os._orders) == 1
    assert order1.calculate_price() == 13.5

    # ===== MAKE SURE ONLY 1 MAIN WITH 4 INGREDIENTS ADDED =====
    assert len(order1.mains) == 1
    assert len(order1.sides) == 0
    assert len(order1.drinks) == 0
    assert len(order1.mains[0]._ingredients) == 4

    w_ingres = []
    x1 = Ingredient("plain", "wrap", "plain wrap", 1, 2)

    x2 = Ingredient("lettuce", "vegetable", "lettuce", 2, 0.5)

    x3 = Ingredient("tomato", "vegetable", "tomato", 2, 1)

    x4 = Ingredient("cheddar", "cheese", "cheddar cheese", 4, 1)

    for x in [x1, x2, x3, x4]:
        w_ingres.append(x)

    # ===== STORE CURRENT INVENTORY LEVELS =====
    wrapQ = ing_quantity("plain", "wrap")
    letQ = ing_quantity("lettuce", "vegetable")
    tomQ = ing_quantity("tomato", "vegetable")
    cheQ = ing_quantity("cheddar", "cheese")
    
    # ===== ORDER 2ND MAIN =====
    order2 = Order()
    m2 = Main("wrap", w_ingres)
    order2.add_main(m2)
    assert os.add_order(order2) == True
    assert len(os._orders) == 2
    assert order2.calculate_price() == 9

    # ===== MAKE SURE ONLY 1 MAIN WITH 4 INGREDIENTS ADDED =====
    assert len(order2.mains) == 1
    assert len(order2.sides) == 0
    assert len(order2.drinks) == 0
    assert len(order2.mains[0]._ingredients) == 4

    # ===== MAKE SURE INVENTORY UPDATED CORRECTLY =====
    assert ing_quantity("plain", "wrap") == wrapQ - 1
    assert ing_quantity("lettuce", "vegetable") == letQ - 2
    assert ing_quantity("tomato", "vegetable") == tomQ - 2
    assert ing_quantity("cheddar", "cheese") == cheQ - 4

    
def test_invalid_order_main(os):
    # ===== ORDERS A BURGER WITH TOO MANY BUNS =====
    b_ingres = []
    x1 = Ingredient("sesame", "bun", "sesame bun", 1000, 1.5)
    x2 = Ingredient("lettuce", "vegetable", 2, 0.5)
    b_ingres.append(x1)
    b_ingres.append(x2)

    order1 = Order()
    bunQ = ing_quantity("sesame", "bun")
    m1 = Main("Burger", b_ingres)
    order1.add_main(m1)

    # ===== MAKES SURE THE ERROR IS CATCHED AND THE CORRECT MESSAGE IS DISPLAYED =====
    try:
        os.add_order(order1)
        assert False

    except Exception as err:
        assert str(err) == "Not enough ingredients available."
        assert True
        
    # ===== MAKE SURE INVENTORY WASN'T UPDATED =====
    assert ing_quantity("sesame", "bun") == bunQ
    # ASSERT NO ORDER LOGGED
    assert len(os._orders) == 0

def test_many_invalid_order_main(os):
    ingres1 = []
    x1 = Ingredient("sesame", "bun", "sesame bun", 3, 1.5)
    
    x2 = Ingredient("beef", "patty", "beef patty", 40, 3.0)
    
    x3 = Ingredient("tomato", "vegetable", "tomato", 15, 0.5)
    
    x4 = Ingredient("cheddar", "cheese",  "cheddar cheese", 2, 1)
    
    for x in [x1, x2, x3, x4]:
        ingres1.append(x)

    # ===== ORDERING 1 BURGER =====
    order1 = Order()
    m1 = Main("Burger", ingres1)
    order1.add_main(m1)
    assert os.add_order(order1) == True
    assert len(os._orders) == 1

    ingres2 = []
    x1 = Ingredient("plain", "wrap", "plain wrap", 3, 1.5)
    
    x2 = Ingredient("beef", "patty", "beef patty", 2, 3.0)
    
    x3 = Ingredient("tomato", "vegetable", "tomato", 2, 0.5)
    
    x4 = Ingredient("cheddar", "cheese", "cheddar cheese", 2, 1)
    
    for x in [x1, x2, x3, x4]:
        ingres2.append(x)

    # ===== ORDERING A WRAP =====
    order2 = Order()
    m2 = Main("wrap", ingres2)
    order2.add_main(m2)
    assert os.add_order(order2) == True
    assert len(os._orders) == 2

    # ===== ORDERING ANOTHER BURGER - INVALID =====
    ingres3 = []
    x1 = Ingredient("plain", "wrap", "plain wrap", 30, 1.5)
    
    x2 = Ingredient("beef", "patty", "beef patty", 4000, 3.0)
    
    x3 = Ingredient("tomato", "vegetable", "tomato",20, 0.5)
    
    x4 = Ingredient("cheddar", "cheese", "cheddar cheese", 200, 1)
    
    for x in [x1, x2, x3, x4]:
        ingres3.append(x)

    m3 = Main("burger", ingres3)
    order3 = Order()
    order3.add_main(m3)
   
    # ===== MAKES SURE THE ERROR IS CATCHED AND THE CORRECT MESSAGE IS DISPLAYED=====
    try:
        os.add_order(order3)
        print(ing_quantity("beef", "patty"))
        assert False
    except Exception as err:
        assert str(err) == "Not enough ingredients available."
        assert True
    
    # ASSERT ONLY 2 ORDERS HAVE BEEN LOGGED
    assert len(os._orders) == 2

def test_order_nuggets(os):
    # ===== ORDERING 3 NUGGETS =====
    order1 = Order()
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

def test_order_invalid_nuggets(os):
    # ===== ORDERS NUGGETS UNTIL NEXT ORDER WILL BE INVALID =====
    x = 0
    nuggetq = side_quantity(Nuggets(6))
    end = nuggetq / 6
    iterate = nuggetq - 6
    if nuggetq % 6 == 0:
        iterate = nuggetq
          
    while x < iterate:
        orderx = Order()
        orderx.add_side(Nuggets(6))
        assert orderx.calculate_price() == 4.50
        assert os.add_order(orderx) == True
        x += 6

    assert len(os._orders) == int(end)

    # ===== MAKES A NEW ORDER =====
    invalid_order = Order()
    invalid_order.add_side(Nuggets(6))
    assert invalid_order.calculate_price() == 4.50

    # ===== MAKES SURE THE ERROR IS CATCHED AND THE CORRECT MESSAGE IS DISPLAYED=====
    try:
        os.add_order(invalid_order)
        assert False
    except Exception as err:
        assert str(err) == "Not enough ingredients available."
        assert True

    # ASSERT THAT LENGTH IS SAME AS BEFORE SHOWING THAT ORDER WASN'T ADDED
    assert len(os._orders) == int(end)

def test_order_fries(os):
    # ===== ORDERING SMALL FRIES =====
    order1 = Order()
    friesQ = side_quantity(Fries(""))
    order1.add_side(Fries("small"))

    assert order1.calculate_price() == 2
    assert os.add_order(order1) == True
    assert side_quantity(Fries("")) == friesQ - 250

    # ===== ORDERING MEDIUM FRIES =====
    order2 = Order()
    friesQ = side_quantity(Fries(""))
    order2.add_side(Fries("medium"))

    assert order2.calculate_price() == 3
    assert os.add_order(order2) == True
    assert side_quantity(Fries("")) == friesQ - 400

    # ===== ORDERING LARGE FRIES =====
    order3 = Order()
    friesQ = side_quantity(Fries(""))
    order3.add_side(Fries("large"))

    assert order3.calculate_price() == 3.5
    assert os.add_order(order3) == True
    assert side_quantity(Fries("")) == friesQ - 640

    # ASSERT THAT 3 ORDERS WERE MADE
    assert len(os._orders) == 3

def test_order_fries_invalid(os):
    # ===== ORDERS FRIES UNTIL NEXT ORDER WILL BE INVALID =====
    friesQ = side_quantity(Fries(""))
    end = friesQ / 640
    x = 0
    iterate = friesQ - 640
    if friesQ % 640 == 0:
        iterate = friesQ
   
          
    while x < iterate:
        orderx = Order()
        orderx.add_side(Fries("large"))
        assert orderx.calculate_price() == 3.50
        assert os.add_order(orderx) == True
        x += 640

    assert len(os._orders) == int(end)

    # ===== MAKES A NEW ORDER =====
    invalid_order = Order()
    invalid_order.add_side(Fries("large"))
    assert invalid_order.calculate_price() == 3.5

    # ===== MAKES SURE THE ERROR IS CATCHED AND THE CORRECT MESSAGE IS DISPLAYED=====
    try:
        os.add_order(invalid_order)
        assert False
    except Exception as err:
        assert str(err) == "Not enough ingredients available."
        assert True

    # ASSERT THAT LENGTH IS SAME AS BEFORE SHOWING THAT ORDER WASN'T ADDED
    assert len(os._orders) == int(end)

def test_order_drinks(os):
    # ===== ORDERING SMALL OJ =====
    order1 = Order()
    ojQ = drink_quantity("orange juice", "")  
    order1.add_drink(Drink("orange juice", "small", 250)) 

    assert order1.calculate_price() == 2
    assert os.add_order(order1) == True
    assert drink_quantity("orange juice", "") == ojQ - 250

    # ===== ORDERING MEDIUM OJ =====
    order2 = Order()
    ojQ = drink_quantity("orange juice", "")  
    order2.add_drink(Drink("orange juice", "medium", 500))

    assert order2.calculate_price() == 2.50
    assert os.add_order(order2) == True
    assert drink_quantity("orange juice", "") == ojQ - 500

    # ===== ORDERING LARGE OJ =====
    order3 = Order()
    ojQ = drink_quantity("orange juice", "") 
    order3.add_drink(Drink("orange juice", "large", 650))

    assert order3.calculate_price() == 2.95
    assert os.add_order(order3) == True
    assert drink_quantity("orange juice", "") == ojQ - 650

    # ===== 3 ORDERS WERE MADE =====
    assert len(os._orders) == 3

def test_order_drinks_invalid(os):
    # ===== ORDERS DRINKS UNTIL NEXT ORDER WILL BE INVALID =====
    orange_q = drink_quantity("orange juice", "")
    end = orange_q / 640

    x = 1
    while x < orange_q - 640:
        orderx = Order()
        orderx.add_drink(Drink("orange juice", "large", 640))
        assert orderx.calculate_price() == 2.95
        assert os.add_order(orderx) == True
        x += 640

    assert len(os._orders) == int(end)

     # ===== MAKES A NEW ORDER =====
    invalid_order = Order()
    invalid_order.add_drink(Drink("orange juice", "large", 640))
    assert invalid_order.calculate_price() == 2.95
    # ===== MAKES SURE THE ERROR IS CATCHED AND THE CORRECT MESSAGE IS DISPLAYED=====
    try:
        os.add_order(invalid_order)  
        assert False
    except Exception as err:
        assert str(err) == "Not enough ingredients available."
        assert True

    # ASSERT LENGTH OF ORDERS IS THE SAME - NO ORDER WAS ADDED
    assert len(os._orders) == int(end)

def test_order_drink_can_bottle(os):
    #===== ORDERING AN CAN OF PEPSI =====
    order1 = Order()
    pepsi_q = drink_quantity("pepsi", "can")   

    order1.add_drink(Drink("pepsi", "can", 1))
    order1.add_drink(Drink("pepsi", "can", 1))
    assert order1.calculate_price() == 2 * 2
    assert os.add_order(order1) == True 
    assert drink_quantity("pepsi", "can") == pepsi_q - 2

    #===== ORDERING AN BOTTLE OF SPRITE =====
    order2 = Order()
    order2.add_drink(Drink("sprite", "bottle", 1))
    sprite_q = drink_quantity("sprite", "bottle")

    assert order2.calculate_price() == 3
    assert os.add_order(order2) == True
    assert drink_quantity("sprite", "bottle") == sprite_q - 1
    assert len(os._orders) == 2

def test_order_drink_can_invalid(os):
    # ===== ORDERS DRINKS UNTIL NEXT ORDER WILL BE INVALID =====
    x = 1
    pepsi_q = drink_quantity("pepsi", "can")   
    end = pepsi_q 
    while x <= pepsi_q:
        orderx = Order()
        orderx.add_drink(Drink("pepsi", "can", 1))
        assert orderx.calculate_price() == 2 
        assert os.add_order(orderx) == True
        assert drink_quantity("pepsi", "can") == pepsi_q - x
        x += 1

    assert len(os._orders) == end
    # ===== MAKES A NEW ORDER =====
    invalid_order = Order()
    invalid_order.add_drink(Drink("pepsi", "can", 1))
    assert invalid_order.calculate_price() == 2 

    # ===== MAKES SURE THE ERROR IS CATCHED AND THE CORRECT MESSAGE IS DISPLAYED=====
    try:
        os.add_order(invalid_order)  
        assert False
    except Exception as err:
        assert str(err) == "Not enough ingredients available."
        assert True

    # ASSERT THAT LENGTH IS SAME AS BEFORE SHOWING THAT ORDER WASN'T ADDED
    assert len(os._orders) == end

def test_order_drink_bottle_invalid(os):
    # ===== ORDERS DRINKS UNTIL NEXT ORDER WILL BE INVALID =====
    x = 1
    sprite_q = drink_quantity("sprite", "bottle")   
    end = sprite_q
    while x <= sprite_q:
        orderx = Order()
        orderx.add_drink(Drink("sprite", "bottle", 1))
        assert orderx.calculate_price() == 3 
        assert os.add_order(orderx) == True
        assert drink_quantity("sprite", "bottle") == sprite_q - x
        x += 1

    assert len(os._orders) == end
    # ===== MAKES A NEW ORDER =====
    invalid_order = Order()
    invalid_order.add_drink(Drink("sprite", "bottle", 1))
    assert invalid_order.calculate_price() == 3

    # ===== MAKES SURE THE ERROR IS CATCHED AND THE CORRECT MESSAGE IS DISPLAYED=====
    try:
        os.add_order(invalid_order)  
        assert False
    except Exception as err:
        assert str(err) == "Not enough ingredients available."
        assert True

    # ASSERT LENGTH IS THE SAME 
    assert len(os._orders) == end

