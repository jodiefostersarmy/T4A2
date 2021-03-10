from main import db                                                                   # This is the db instance created by SQLAlchemy
from sqlalchemy.orm import backref                                                    # Used to make references to other tables
from models.SavedWord import SavedWord

class User(db.Model):                                                                 # Creating a Users class inheriting from db.Model
    __tablename__= "users"                                                            # Explicitly naming the table "users"

    id = db.Column(db.Integer, primary_key=True)                                      # There is an id column and it is the primary key
    saved_word = db.relationship(
        "SavedWord", backref="user", 
        lazy="dynamic", 
        cascade="all, delete", 
        passive_deletes=True
    )

    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)                       # Email column, string and it must be unique, not null
    password = db.Column(db.String(), nullable=False)                                 # The password is a string and must be present
    mobile_number = db.Column(db.BigInteger(), nullable=True)           # Mobile is an integer, cannot be null and must be unique
    join_date = db.Column(db.BigInteger())                                            # The join_date is a datetime and cannot be null
    is_admin = db.Column(db.Boolean(), nullable=True, default=False)

    def __repr__(self):                                                               # When printing the model we will see user email attribute
        return f"<User: {self.email}>"