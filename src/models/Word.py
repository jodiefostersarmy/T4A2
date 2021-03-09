from main import db
from sqlalchemy.orm import backref
from models.SavedWord import SavedWord

class Word(db.Model):
    __tablename__= "words"

    id = db.Column(db.Integer, primary_key=True)

    saved_word = db.relationship("SavedWord", backref="word", lazy="dynamic")

    word = db.Column(db.String(), nullable=False, unique=True)
    definition = db.Column(db.String(), nullable=False)
    pronunciation = db.Column(db.String(), nullable=False)



    def __repr__(self):
        return f"{self.word}"