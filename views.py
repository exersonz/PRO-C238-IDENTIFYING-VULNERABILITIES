# import necessary modules and functions from Flask and the application models
from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from app.models.products import Products
from app.models.address import Address
from app.models.users import Users
from app.models.orders import Orders
from app import db
from flask_cors import cross_origin

# create a Blueprint named 'views' with a url prefix "/"
views = Blueprint('views', __name__, url_prefix="/")

# route for the login page
@views.route('/')
@cross_origin()
def login():
    try:
        return render_template("/login/login.html") # render login page
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

# route for the dashboard page
@views.route('/dashboard')
@cross_origin()
def dashboard():
    try:
        query = "select * from products;" # SQL query to select all products
        products = db.engine.execute(query).all() # execute the query and fetch all products
        return render_template("/dashboard/dashboard.html", products=products, user_id=session.get('user_id')) # render the dashboard with products and user_id from session
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

# route for the profile page
@views.route('/profile')
@cross_origin()
def profile():
    try:
        user_id = request.args.get("id") # get the user ID from the request arguments
        user_query = f"select * from users where id='{user_id}';" # SQL query to select the user by ID
        user = db.engine.execute(user_query).first() # execute the query and fetch the user
        order_query = f"select p.image, p.name, o.amount from products p right join orders o on o.user_id={user['id']} and p.id=o.product_id;" # SQL query to fetch orders for the user
        orders = db.engine.execute(order_query).all() # execute the query and fetch all orders
        ticket_query = f"select * from tickets where user_id='{user['id']}';" # SQL query to fetch tickets for user
        tickets = db.engine.execute(ticket_query).all() # execute the query and fetch all tickets
        address_query = f"select * from address where user_id='{user['id']}'" # SQL query to fetch addresses for the user
        addresses = db.engine.execute(address_query).all() # execute the query and fetch all addresses
        return render_template("/profile/profile.html", user=user, orders=orders, addresses=addresses, tickets=tickets, user_id=session.get("user_id")) # render the profile page with user details, orders, addresses, tickets, and user_id from session
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

# route for order page
@views.route('/order')
@cross_origin()
def order():
    try:
        product_id = request.args.get("id") # get product ID from the request argument
        if not product_id:
            return jsonify({
                "message": "No product for purchase!",
                "status": "error"
            }), 400
        query = f"select * from products where id={product_id};" # SQL query to select product by ID
        product = db.engine.execute(query).first() # execute query and fetch the product
        address_query = f"select * from address where user_id='{session.get('user_id')}'" # SQL query to fetch addresses for the user
        addresses = db.engine.execute(address_query).all() or [] # execute query and fetch all addresses
        return render_template("/order/order.html", product=product, addresses=addresses, user_id=session.get('user_id')) # render the order page with the product, addresses, and user_id from session
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

# route for the help page
@views.route("/help")
@cross_origin()
def help_page():
    try:
        return render_template("/help/help.html", user_id=session.get('user_id')) # render the help page with user_id from session
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

# route for the editor page
@views.route("/editor")
@cross_origin()
def editor():
    try:
        return render_template("/editor/editor.html") # render the editor page
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400