# importing necessary models and the db instance from the app
from app import db

# defining a Customer model class (inherits from db.Model)
class Customer(db.Model):
    # specifying the table name in the database
    __tablename__ = "customers"

    # defining the columns of customers table
    id = db.Column(db.Integer, primary_key=True) # primary key column
    first_name = db.Column(db.String(64)) # customer's first name
    last_name = db.Column(db.String(64)) # customer's last name
    city = db.Column(db.String(64)) # city customer is from
    country = db.Column(db.String(64)) # country customer is from
    phone = db.Column(db.String(64)) # customer phone number

    # static method to create a new customer record
    @staticmethod
    def create(id, first_name, last_name, city, country, phone):
        # creating a dictionary with customer details
        customer_dict = dict(
            id = id,
            first_name = first_name,
            last_name = last_name,
            city = city,
            country = country,
            phone = phone
        )
        # creating a Customer object from customer details dictionary
        customer_obj = Customer(**customer_dict)
        # adding the new customer to the session and committing to the database
        db.session.add(customer_obj)
        db.session.commit()    