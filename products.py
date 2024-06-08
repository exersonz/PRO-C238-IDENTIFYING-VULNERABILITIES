# importing necessary modules and the db instance from the app
from app import db
import uuid

# defining the Products model class (inherits from db.Model)
class Products(db.Model):
    # specifying the table name in the database
    __tablename__ = "products"

    # defining columns of the products table
    id = db.Column(db.Integer, primary_key=True) # primary key column
    guid = db.Column(db.String, nullable=False, unique=True)# unique GUID for each product
    name = db.Column(db.String(64)) # product name column
    image = db.Column(db.String(128)) # product image column
    rating = db.Column(db.Integer) # product rating column
    marked_price = db.Column(db.Float) # product marked price column
    selling_price = db.Column(db.Float) # product selling price column

    # static method to create a new product record
    @staticmethod
    def create(name, image, rating, marked_price, selling_price):
        # creating a dictionary with the product details and a unique GUID
        product_dict = dict(
            guid = str(uuid.uuid4()),
            name = name,
            image = image,
            rating = rating,
            marked_price = marked_price,
            selling_price = selling_price
        )
        # creating a Products object from the dictionary
        product_obj = Products(**product_dict)
        # adding the new product to the session and committing to the database
        db.session.add(product_obj)
        db.session.commit()

    # instance method to update an existing product record
    def update(self, **details_dict):
        # updating the product object with new values from the details dictionary
        for k,v in details_dict.items():
            setattr(self, k, v)
        # committing the updated order to the database
        db.session.commit()