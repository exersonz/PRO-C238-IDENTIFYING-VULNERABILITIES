# importing necessary modules and the db instance from the app
from app import db
import uuid

# defining Tickets model class (inherits from db.model)
class Tickets(db.Model):
    # specifying the table name in the database
    __tablename__ = "tickets"

    # defining the columns of the tickets table
    id = db.Column(db.Integer, primary_key=True) # primary key column
    guid = db.Column(db.String, nullable=False, unique=True) # unique GUID for each ticket
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # foreign key for users table
    title = db.Column(db.String(64)) # title column
    description = db.Column(db.String(1024)) # description column
    attachment = db.Column(db.String(64)) # attachment column

    # static method to create a new ticket record
    @staticmethod
    def create(user_id, title, description, attachment):
        # creating a dictionary with ticket details and a unique GUID
        ticket_dict = dict(
            guid = str(uuid.uuid4()),
            user_id = user_id,
            title = title,
            description = description,
            attachment = attachment
        )
        # creating a Tickets object from the dictionary
        ticket_obj = Tickets(**ticket_dict)
        # adding the new ticket to the session and committing to the database
        db.session.add(ticket_obj)
        db.session.commit()

    # instance method to update the existing ticket record
    def update(self, **details_dict):
        # updating the ticket object with new values from the details dictionary
        for k,v in details_dict.items():
            setattr(self, k, v)
        # committing the updated ticket to the databse
        db.session.commit()