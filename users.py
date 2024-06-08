# importing necessary modules and db instance from the app
from app import db
import uuid

# importing models for Address, Orders, and Tickets
from app.models.address import Address
from app.models.orders import Orders
from app.models.tickets import Tickets

# defining a Users model class (inherited from db.Model)
class Users(db.Model):
    # specifying the table name in the database
    __tablename__ = "users"

    # defining the columns of the users table
    id = db.Column(db.Integer, primary_key=True) # primary key column
    guid = db.Column(db.String, nullable=False, unique=True) # unique GUID for each user
    name = db.Column(db.String(64)) # user name column
    email = db.Column(db.String(64)) # user email column
    password = db.Column(db.String(64)) # user password column
    contact = db.Column(db.String(64)) # user contact column
    addresses = db.relationship(Address, lazy=True, backref="user") # relationship to Address model
    orders = db.relationship(Orders, lazy=True, backref="user") # relationship to Orders model
    tickets = db.relationship(Tickets, lazy=True, backref="user") # relationship to Tickets model

    # static method to create a new user record
    @staticmethod
    def create(name, email, password, contact):
        # creating a dictionary with user details and a unique GUID
        user_dict = dict(
            guid = str(uuid.uuid4()),
            name = name,
            email = email,
            password = password,
            contact = contact
        )
        # creating a Users object from the dictionary
        user_obj = Users(**user_dict)

        # adding the new user to session and committing to the database
        db.session.add(user_obj)
        db.session.commit()

    # instance method to update existing user record
    def update(self, **details_dict):
        # updating the user object with new values from the details dictionary
        for k, v in details_dict.items():
            setattr(self, k, v)
        # committing the updated user to database
        db.session.commit()

    # def to_dict(self):
    #     return {
    #         "email": self.email,
    #         "password": self.password,
    #         "name": self.name
    #     }