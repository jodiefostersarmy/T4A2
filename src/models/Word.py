from main import db
from sqlalchemy.orm import backref
from models.SavedWord import SavedWord
from models.Reminder import Reminder
from models.Folder import Folder

class Word(db.Model):
    __tablename__= "words"

    id = db.Column(db.Integer, primary_key=True)

    saved_word = db.relationship("SavedWord", backref="word")
    reminder = db.relationship("Reminder", backref=backref("word_reminder", uselist=False))
    foldered_word = db.relationship("FolderWord", backref=backref("word_foldered", uselist=False))

    word = db.Column(db.String(), nullable=False, unique=True)
    definition = db.Column(db.String(), nullable=False)
    pronunciation = db.Column(db.String(), nullable=False)



    def __repr__(self):
        return f"<Word: {self.word}>"