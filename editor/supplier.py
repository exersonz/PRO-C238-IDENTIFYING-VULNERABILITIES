# import necessary modules and db instance from app
from app import db

# defining a Supplier model class (inherits from db.Model)
class Supplier(db.Model):
    # specifying table name in database
    __tablename__ = "suppliers"
    
    # defining columns of suppliers table
    id = db.Column(db.Integer, primary_key=True) # primary key column
    company_name = db.Column(db.String(64)) # company name of supplier
    contact_name = db.Column(db.String(64)) # supplier contact name
    city = db.Column(db.String(64)) # supplier city
    country = db.Column(db.String(64)) # supplier country
    phone = db.Column(db.String(64)) # supplier phone number
    fax = db.Column(db.String(64)) # supplier fax

    # static method to create a new supplier record
    @staticmethod
    def create(id, company_name, contact_name, city, country, phone, fax):
        # creating a dictionary with supplier details
        supplier_dict = dict(
            id = id,
            company_name = company_name,
            contact_name = contact_name,
            city = city,
            country = country,
            phone = phone
        )
        # creating a Supplier object from supplier details dictionary
        supplier_obj = Supplier(**supplier_dict)
        # adding new supplier to session and committing to the database
        db.session.add(supplier_obj)
        db.session.commit()