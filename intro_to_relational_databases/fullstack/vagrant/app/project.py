from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from setup_database import Base, Restaurants, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from setup_database import Base, Restaurants, MenuItem


app = Flask(__name__)
engine = create_engine('postgresql://vagrant:glue@localhost/restaurant_db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants', methods=['GET'])
def show_restaurants():
    restaurants = session.query(Restaurants).all()
    return render_template('restaurants.html', restaurants=restaurants)

@app.route('/restaurants/new', methods=['GET', 'POST'])
def new_restaurant():
    if request.method == 'POST':
        name = request.form['new_name']
        session.add(Restaurants(name=name))
        session.commit()
        return redirect(url_for('show_restaurants'))
    else:
        return render_template('restaurants_new.html')
    
@app.route('/restaurants/<int:id>/', methods=['GET'])
def restaurant_page(id):
    restaurant = session.query(Restaurants).filter_by(id=id).one()
    menu_item = session.query(MenuItem).filter_by(restaurant_id = restaurant.id).all()
    return render_template('restaurant_page.html', rest=restaurant, menu=menu_item)

@app.route('/restaurants/<int:id>/menu_items/<int:menu_id>/edit', methods=['GET', 'POST'])
def edit_item(id, menu_id):
    if request.method == 'POST':
        item = session.query(MenuItem).filter_by(item_id=menu_id).one()
        item.name = request.form["item_name"]
        item.course = request.form["item_course"]
        item.price = float(request.form["item_price"])
        item.description = request.form["item_description"]
        session.add(item)
        session.commit()
        return redirect(url_for('restaurant_page', id=id))
    else:
        restaurant = session.query(Restaurants).filter_by(id=id).one()
        menu_item = session.query(MenuItem).filter_by(item_id=menu_id).one()
        return render_template("item_edit.html", rest=restaurant, item=menu_item)

@app.route('/restaurants/<int:id>/menu_items/<int:menu_id>/delete', methods=['GET', 'POST'])
def delete_item(id, menu_id):
    if request.method == 'POST':
        item = session.query(MenuItem).filter_by(item_id=menu_id).one()
        session.delete(item)
        session.commit()
        return redirect(url_for('restaurant_page', id=id))
    else:
        restaurant = session.query(Restaurants).filter_by(id=id).one()
        menu_item = session.query(MenuItem).filter_by(item_id = menu_id).one()
        return render_template("item_delete.html", rest=restaurant, item=menu_item)

@app.route('/restaurants/<int:id>/menu_items/new', methods=['GET', 'POST'])
def new_item(id):
     if request.method == 'POST':
        
        name = request.form["item_name"]
        course = request.form["item_course"]
        price = float(request.form["item_price"])
        description = request.form["item_description"]
        restaurant = session.query(Restaurants).filter_by(id=id).one()
        item = MenuItem(name=name, course=course, price=price, description=description, restaurant_id=id, restaurants=restaurant)
        session.add(item)
        session.commit()
        return redirect(url_for('restaurant_page', id=id))
     else:
        restaurant = session.query(Restaurants).filter_by(id=id).one() 
        return render_template("item_new.html", rest=restaurant)
@app.route('/restaurants/<int:id>/menu/JSON', methods=['GET'])
def restaurantMenuJSON(id):
    restaurant = session.query(Restaurants).filter_by(id=id).one()
    menu_items = session.query(MenuItem).filter_by(restaurant_id=id).all()
    return jsonify(MenuItems = [i.serialize for i in menu_items])

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
