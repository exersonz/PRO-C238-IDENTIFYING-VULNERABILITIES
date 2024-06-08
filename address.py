# importing necessary modules and the db instance from the app
from app import db
import uuid

# defining the Address model class (inherits from db.Model)
class Address(db.Model):
    # specifying the table name in the database
    __tablename__ = "address"

    # defining the columns of the address table
    id = db.Column(db.Integer, primary_key=True) # primary key column 
    guid = db.Column(db.String, nullable=False, unique=True) # unique GUID for each address
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # foreign key to users table
    house_number = db.Column(db.String) # house number column
    city = db.Column(db.String) # city column
    state = db.Column(db.String) # state column
    country = db.Column(db.String) # country column
    pin_code = db.Column(db.String) # pin code column

    # static method to create a new address record
    @staticmethod
    def create(user_id, house_number, city, state, country, pin_code):
        # creating a dictionary with the address details and a unique GUID
        address_dict = dict(
            guid = str(uuid.uuid4()),
            user_id = user_id,
            house_number = house_number,
            city = city,
            state = state,
            country = country,
            pin_code = pin_code
        )
        # creating an Address object from dictionary
        address_obj = Address(**address_dict)
        # adding the new address to the session and committing to the database
        db.session.add(address_obj)
        db.session.commit()

    # instance method to update an existing address record
    def update(self, **details_dict):
        # updating the address object with new values from the details dictionary
        for k, v in details_dict.items():
            setattr(self, k, v)
        # committing the updated address to the database
        db.session.commit()