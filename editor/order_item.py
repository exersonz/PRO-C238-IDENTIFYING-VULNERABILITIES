# import necessary models and the db instance from app
from app import db

# importing CompanyOrders and CompanyProducts models
from app.models.editor.company_orders import CompanyOrders
from app.models.editor.company_products import CompanyProducts

# definign an OrderItems model class (inhreits from db.Model)
class OrderItems(db.Model):
    # specifying table name in db
    __tablename__ = "order_items"

    # defining column of order_items table
    id = db.Column(db.Integer, primary_key=True) # primary key column
    order_id = db.Column(db.Integer, db.ForeignKey('company_orders.id'), nullable=False) # foreign key to company_orders table
    product_id = db.Column(db.Integer, db.ForeignKey('company_products.id'), nullable=False) # foreign key to company_products table
    unit_price = db.Column(db.Float) # unit price of order item
    quantity = db.Column(db.Integer) # quantity of order item
    
    # static method to create a new order item record
    @staticmethod
    def create(id, order_id, product_id, unit_price, quantity):
        # creating a dictionary with order item details
        order_dict = dict(
            id = id,
            order_id = order_id,
            product_id = product_id,
            unit_price = unit_price,
            quantity = quantity
        )
        # creating OrderItems object from order details dictionary
        order_obj = OrderItems(**order_dict)
        # adding new order item to session and committing to database
        db.session.add(order_obj)
        db.session.commit()