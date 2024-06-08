# importing necessary modules and functions from Flask and application modules
from flask import Blueprint, jsonify, request, session, redirect, url_for, send_file
from app.models.users import Users
from app.models.address import Address
from app.models.orders import Orders
from app.models.tickets import Tickets
from werkzeug.utils import secure_filename
from app import db
import os

# making a Blueprint named 'api' with a url prefix of "/api"
api = Blueprint('api', __name__, url_prefix="/api")

# setting the upload folder for attachments
UPLOAD_FOLDER = os.path.abspath("app/static/attachments")

# route for user login
@api.route('/login', methods=['POST'])
def login():
    try:
        email = request.json.get('email') # get email from request
        password = request.json.get('password') # get password from request

        # SQL query to select user with the provided email and password
        query = f"(select * from users where email='{email}' and password='{password}');"
        
        if not all((email, password)): # check if both email and password are provided
            return jsonify({
                    'status': 'error',
                    'message': 'Both email and password are required!'
            }), 400
        user = db.engine.execute(query).first() # execute query and get the first result

        if user: # user exists, set session and return success response
            session["email"] = email
            session["user_id"] = user[0]
            return jsonify({
                "status": "success",
                "id": user[0]
            }), 200
        else: # if user doesn't exist, return error response
            return jsonify({
                "status": "error",
                "message": "Not sure"
            }), 400
    except Exception as e: # handle exceptions and return error response
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

# route for user logout
@api.route("/logout", methods=["POST"])
def logout():
    try:
        session["email"] = None # clear email from session
        session["user_id"] = None # clear user_id from session
        return jsonify({
            "status": "success",
        }), 200

    except Exception as e: # handle exceptions and return error message
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

# route for adding a new address
@api.route("/add-address", methods=["POST"])
def add_address():
    try:
        # get address details from request
        house_number = request.json.get("house_number")
        city = request.json.get("city")
        state = request.json.get("state")
        country = request.json.get("country")
        pin_code = request.json.get("pin_code")

        user_email = session.get("email") # get user email from session
        user_query = f"select * from users where email='{user_email}';" # SQL query to get user by email
        user = db.engine.execute(user_query).first() # execute query and get the first result
        
        # create new address
        Address.create(user["id"], house_number, city, state, country, pin_code)

        return jsonify({
            "status": "success",
        }), 201
        
    except Exception as e: # handle exceptions and return error message
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

# route for creating new order
@api.route("/create-order", methods=["POST"])
def create_order():
    try:
        user_email = session.get("email") # get user email fro msession
        user_query = f"select * from users where email='{user_email}';" # SQL query to select user by email
        user = db.engine.execute(user_query).first() # execute query and get first result

        # get order details from request
        product_id = request.json.get("product_id")
        address_id = request.json.get("address_id")
        amount = request.json.get("amount")
        
        # create new order
        Orders.create(user["id"], product_id, 1, address_id, amount)
        return jsonify({
                "status": "success",
        }), 201
    except Exception as e: # handle exceptions and return error message
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

# route for submitting a help request
@api.route("/submit-help", methods=["POST"])
def submit_help():
    # get help request details from form
    title = request.form.get("title")
    description = request.form.get("description")
    attachment = request.files.get("attachment")
    
    if attachment: # if there is an attachment, save it
        filename = secure_filename(attachment.filename)
        attachment.save(os.path.join(UPLOAD_FOLDER, filename))
    
    user_email = session.get("email") # get user email from session
    user_query = f"select * from users where email='{user_email}';" # SQL query to get user by email
    user = db.engine.execute(user_query).first() # execute query and get first result

    # create new help ticket
    Tickets.create(user["id"], title, description, filename)
    
    return jsonify({
        "status": "success",
    }), 201

# route for downloading a file
@api.route("/download/<path:filename>")
def download(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename), as_attachment=True) # send file as attachment

# route for searching an order
@api.route("/search-order")
def search_order():
    order_id = request.args.get("order_id") # get order id from request arguments
    user_email = session.get("email") # get user email from session
    user_query = f"select * from users where email='{user_email}';" # SQL query to get user by email
    user = db.engine.execute(user_query).first() # execute query and get the first result

    # SQL query to get order details
    order_query = f"(select p.image, p.name, o.amount from products p right join orders o on o.user_id={user['id']} and p.id=o.product_id and o.id={order_id});"
    order = db.engine.execute(order_query).all() # execute query and get all results+

    orders = []
    for order_obj in order: # process order details
        if all((order_obj[0], order_obj[1], order_obj[2])):
            orders.append([order_obj[0], order_obj[1], order_obj[2]])
    
    return jsonify({
        "status": "success",
        "orders": orders
    }), 200

# route for executing raw SQL queries
@api.route("/execute", methods=["POST"])
def execute():
    try:
        code = request.json.get("code") # get SQL query from request
        result = db.engine.execute(code).all() # execute query and get all results
        
        if len(result) == 0: # if no results, return no result status
            return jsonify({
                "status": "no_result"
            }), 200
        else: # process and return query results
            keys, values = result[0].keys()._keys, []
            for result_obj in result:
                temp_values = []
                for result_value in result_obj:
                    temp_values.append(result_value)
                values.append(temp_values)
            return jsonify({
                "status": "success",
                "keys": keys,
                "values": values
            }), 200
    except Exception as e: # handle exceptions and return error message
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

# route for getting customer details
@api.route("/get-customer")
def get_customer():
    try:
        customer_id = request.args.get("id") # get customer ID from request arguments
        customer_query = f"select * from customers where id='{customer_id}';" # SQL query to get customer by ID
        customer_data = db.engine.execute(customer_query).first() # execute query and get the first result

        if(customer_data): # if customer exists, return success status
            return jsonify({
                "status": "success",
            
            }), 200
        else: # if customer does not exist, return error status
            return jsonify({
                "status" : "error",
                "message" : "Customer not found"
            }), 404
    except Exception as e: # handle exceptions and return error message
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400