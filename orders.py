# importing necessary modules and the db instance from the app
from app import db
import uuid

# importing the models for Products and Address
from app.models.products import Products
from app.models.address import Address

# defining the Orders model class (inherits from db.Model)
class Orders(db.Model):
    # specifying the table name in database
    __tablename__ = "orders"

    # defining the columns of the orders table
    id = db.Column(db.Integer, primary_key=True) # primary key column
    guid = db.Column(db.String, nullable=False, unique=True) # unique GUID for each order
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # foreign key for users table
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False) # foreign key for products table
    product = db.relationship(Products, lazy=True, uselist=False) # relationship to the products model
    quantity = db.Column(db.Integer) # quantity of the product in order
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False) # foreign key to address table
    address = db.relationship(Address, lazy=True, uselist=False) # relationship to the address model
    amount = db.Column(db.Float) # amount for the order

    # static method to create a new order record
    @staticmethod
    def create(user_id, product_id, quantity, address_id, amount):
        # creating a dictionary with order details and a unique GUID
        order_dict = dict(
            guid = str(uuid.uuid4()),
            user_id = user_id,
            product_id = product_id,
            quantity = quantity,
            address_id = address_id,
            amount = amount
        )
        # creating an Orders object from the dictionary
        order_obj = Orders(**order_dict)
        # adding the new order to the session and committing to the databse
        db.session.add(order_obj)
        db.session.commit()

    # instance method to update an existing order record
    def update(self, **details_dict):
        # updating the order object with new values fro mthe details dictionary
        for k, v in details_dict.items():
            setattr(self, k, v)
        # committing the updated order to the database
        db.session.commit()