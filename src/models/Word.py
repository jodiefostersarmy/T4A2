from main import db                                                                   # This is the db instance created by SQLAlchemy
from sqlalchemy.orm import backref                                                    # Used to make references to other tables

class Word(db.Model):                                                                 # Creating a Users class inheriting from db.Model
    __tablename__= "words"                                                            # Explicitly naming the table "users"

    id = db.Column(db.Integer, primary_key=True)                                      # There is an id column and it is the primary key
    word = db.Column(db.String(), nullable=False, unique=True)                       # Email column, string andit must be unique
    definition = db.Column(db.String(), nullable=False)                              # The password is a string and must be present
    pronunciation = db.Column(db.String(), nullable=False)   

    def __repr__(self):                                                               # When printing the model we will see its email attribute
        return f"<Word {self.word}>"