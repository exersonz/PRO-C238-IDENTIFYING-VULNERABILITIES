# importing the necessary modules and db instance from the app
from app import db

# importing Customer model
from app.models.editor.customer import Customer

# defining the CompanyOrders model class (inherits from db.Model)
class CompanyOrders(db.Model):
    # specifying the table name in the database
    __tablename__ = "company_orders"

    # defining the columns of the company_orders table
    id = db.Column(db.Integer, primary_key=True) # primary key column
    date = db.Column(db.DateTime) # date of the order
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False) # foreign key to customers table
    total_amount = db.Column(db.Float) # total amount for the order
    order_number = db.Column(db.Integer) # order number

    # static method to create a new company order record
    @staticmethod
    def create(id, date, customer_id, total_amount, order_number):
        # creating a dictionary with order details
        order_dict = dict(
            id = id,
            date = date,
            customer_id = customer_id,
            total_amount = total_amount,
            order_number = order_number
        )
        # creating a CompanyOrders object from the dictionary
        order_obj = CompanyOrders(**order_dict)
        # adding the new order to the session and committing to the database
        db.session.add(order_obj)
        db.session.commit()