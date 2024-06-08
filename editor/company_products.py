# importing necessary modules and db instance from app
from app import db

# importing Supplier model
from app.models.editor.supplier import Supplier

# defining the CompanyProducts model class (inherits from db.Model)
class CompanyProducts(db.Model):
    # specifying the table name in the database
    __tablename__ = "company_products"

    # defining columns of the company_products table
    id = db.Column(db.Integer, primary_key=True) # primary key column
    name = db.Column(db.String(64)) # name of company product
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False) # foreign key to suppliers table
    unit_price = db.Column(db.Float) # unit price of company product
    package = db.Column(db.String(64)) # company product package
    is_discontinued = db.Column(db.Integer) # whether company product is discontinued

    # static method to create a new company product record
    @staticmethod
    def create(id, name, supplier_id, unit_price, package, is_discontinued):
        # creating a dictionary with product details 
        products_dict = dict(
            id = id,
            name = name,
            supplier_id = supplier_id,
            unit_price = unit_price,
            package = package,
            is_discontinued = is_discontinued
        )
        # creating a CompanyProducts object from details dictionary
        products_obj = CompanyProducts(**products_dict)
        # adding the new product to the session and committing to the database
        db.session.add(products_obj)
        db.session.commit()