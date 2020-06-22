from copy import deepcopy
from flask import render_template, request, redirect, url_for, abort
from server import app, system
from datetime import datetime
from src.ordering_system import g_ingredients, g_sides, g_drinks, g_inventory, OrderingSystem
from src.ordering_system import update_inventory as u_inventory
from src.forms import InventoryForm, OrderForm

from src.main import Main
from src.order import Order
from src.side import Nuggets, Fries
from src.ingredients import Ingredient
from src.drink import Drink
from src.sundae import Sundae
'''
Dedicated page for "page not found"
'''
@app.route('/404')
@app.errorhandler(404)
def page_not_found(e=None):
    return render_template('404.html'), 404

@app.route('/', methods=["GET", "POST"])
def homepage():
    return render_template('home.html', ingredients=g_ingredients)


@app.route('/orders/new', methods=["GET", "POST"])
def new_order():
    # TODO this is gonna be sloppy as fuck, will fix later
    # first get the type of burger then display the available list of ingredients
    # for that type of main.. Then just display the rest LOL
    # validate burger and wrap option

    if request.method == "GET":
        if request.args.get('amount') is None:
            return render_template('new_order_amount.html')
        else:
            return render_template('new_order_type.html')

    else:
        if request.form.get('first_try') == 'true':
            return render_template('new_order_main.html', ingredients=g_ingredients, sides=g_sides, drinks=g_drinks)

        form = OrderForm(request.form)
        
        
        if form.is_valid:
            order = Order()

            if int(form.get_raw_data('amount')) > 0:
                for x in range(int(form.get_raw_data('amount'))):
                    # i_type = 'burger' or 'wrap'
                    i_type = form.get_raw_data('main_' + str(x))


                    ingredients = deepcopy(g_ingredients)
                    custom_ingredients = []

                    for ingredient in ingredients:
                        if i_type == 'burger' and ingredient.i_type != 'wrap':
                            ingredient.amount = int(form.get_raw_data('main_' + str(x) + '_' + str(ingredient.inv_id)))
                            custom_ingredients.append(ingredient)
                        elif i_type == 'wrap' and ingredient.i_type != 'bun':
                            ingredient.amount = int(form.get_raw_data('main_' + str(x) + '_' + str(ingredient.inv_id)))
                            custom_ingredients.append(ingredient)
                        else:
                            continue
                    
                    main = Main(i_type, custom_ingredients)

                    order.add_main(main)

            if int(form.get_raw_data('sundae_small')) > 0:
                for x in range(int(form.get_raw_data('sundae_small'))):
                    sundae_small = Sundae("chocolate", "small", 1)
                    order.add_sundae(sundae_small)

            if int(form.get_raw_data('sundae_medium')) > 0:
                for x in range(int(form.get_raw_data('sundae_medium'))):
                    sundae_small = Sundae("chocolate", "medium", 1)
                    order.add_sundae(sundae_small)
                    
            if int(form.get_raw_data('sundae_large')) > 0:
                for x in range(int(form.get_raw_data('sundae_large'))):
                    sundae_small = Sundae("chocolate", "large", 1)
                    order.add_sundae(sundae_small)

            if int(form.get_raw_data('nuggets_3')) > 0:
                for x in range(int(form.get_raw_data('nuggets_3'))):
                    nuggets_3 = Nuggets(3)

                    order.add_side(nuggets_3)

            if int(form.get_raw_data('nuggets_6')) > 0:
                for x in range(int(form.get_raw_data('nuggets_6'))):
                    nuggets_6 = Nuggets(6)

                    order.add_side(nuggets_6)

            if int(form.get_raw_data('fries_small')) > 0:
                for x in range(int(form.get_raw_data('fries_small'))):
                    fries_small = Fries('small')

                    order.add_side(fries_small)

            if int(form.get_raw_data('fries_medium')) > 0:
                for x in range(int(form.get_raw_data('fries_medium'))):
                    fries_medium = Fries('medium')

                    order.add_side(fries_medium)

            if int(form.get_raw_data('fries_large')) > 0:
                for x in range(int(form.get_raw_data('fries_large'))):
                    fries_large = Fries('large')

                    order.add_side(fries_large)

            if int(form.get_raw_data('sprite_can')) > 0:
                for x in range(int(form.get_raw_data('sprite_can'))):
                    sprite_can = Drink('sprite', 'can', 1)

                    order.add_drink(sprite_can)

            if int(form.get_raw_data('sprite_bottle')) > 0:
                for x in range(int(form.get_raw_data('sprite_bottle'))):
                    sprite_bottle = Drink('sprite', 'bottle', 1)

                    order.add_drink(sprite_bottle)

            if int(form.get_raw_data('pepsi_can')) > 0:
                for x in range(int(form.get_raw_data('pepsi_can'))):
                    pepsi_can = Drink('pepsi', 'can', 1)

                    order.add_drink(pepsi_can)

            if int(form.get_raw_data('pepsi_bottle')) > 0:
                for x in range(int(form.get_raw_data('pepsi_bottle'))):
                    pepsi_bottle = Drink('pepsi', 'bottle', 1)

                    order.add_drink(pepsi_bottle)

            if int(form.get_raw_data('orange_juice_small')) > 0:
                for x in range(int(form.get_raw_data('orange_juice_small'))):
                    orange_juice_small = Drink('orange juice', 'small', 250)

                    order.add_drink(orange_juice_small)

            if int(form.get_raw_data('orange_juice_medium')) > 0:
                for x in range(int(form.get_raw_data('orange_juice_medium'))):
                    orange_juice_medium = Drink('orange juice', 'medium', 450)

                    order.add_drink(orange_juice_medium)

            if int(form.get_raw_data('orange_juice_large')) > 0:
                for x in range(int(form.get_raw_data('orange_juice_large'))):
                    orange_juice_large = Drink('orange juice', 'large', 650)

                    order.add_drink(orange_juice_large)

            if 'confirm' in request.form:
                system.add_order(order)
                return redirect(url_for('order',order_id=order.order_id))

            else:
                if order.calculate_price() > 0:
                    return render_template('new_order_main.html', ingredients=g_ingredients, sides=g_sides, drinks=g_drinks, confirm=True, fee='{:0,.2f}'.format(order.calculate_price()))
                else:
                    return render_template('new_order_main.html', ingredients=g_ingredients, sides=g_sides, drinks=g_drinks, fee=0)

        else:
            errors = {}
            
            for field in form.fields:
                errors[field.name] = field.error

            return render_template('new_order_main.html', ingredients=g_ingredients, sides=g_sides, drinks=g_drinks, errors=errors)


        return render_template('new_order_main.html', ingredients=g_ingredients, sides=g_sides, drinks=g_drinks)


@app.route('/orders', methods=["GET", "POST"])
def orders():
    orders = system.orders
    completed_orders = system.completed_orders

    return render_template('orders.html', orders=orders, completed_orders=completed_orders)

@app.route('/orders/<int:order_id>', methods=["GET"])
def order(order_id):
    order = system.get_order_by_id(order_id)
    
    if order not in system.completed_orders and order not in system.orders:
        abort(404)
 
    return render_template('order.html', order=order)


@app.route('/orders/<int:order_id>/complete', methods=["GET"])
def complete_order(order_id):
    order = system.get_order_by_id(order_id)

    if not order:
        abort(404)

    system.complete_order(order_id)

    return redirect(url_for('orders'))

@app.route('/orders/<int:order_id>/cancel', methods=["GET"])
def cancel_order(order_id):
    order = system.get_order_by_id(order_id)
    
    if not order:
        abort(404)  

    system.cancel_order(order_id)

    return redirect(url_for('orders'))

@app.route('/inventory', methods=["GET"])
def inventory():
    return render_template('inventory.html', inventory=g_inventory)

@app.route('/inventory/update', methods=["GET", "POST"])
def update_inventory():
    if request.method == "POST":
        form = InventoryForm(request.form)

        if form.is_valid:
            values = {}

            for field in form.fields:
                values[int(field.name)] = int(field.data)

            u_inventory(values, g_inventory)

            return redirect(url_for('inventory'))

        else:
            errors = {}
            
            for field in form.fields:
                errors[field.name] = field.error

            return render_template('update_inventory.html', inventory=g_inventory, errors=errors)

    return render_template('update_inventory.html', inventory=g_inventory)

