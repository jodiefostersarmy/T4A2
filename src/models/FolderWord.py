from main import db
from sqlalchemy.orm import backref   

class FolderWord(db.Model):
    __tablename__= "foldered_words"

    id = db.Column(db.Integer, primary_key=True)
    
    word_id = db.Column(db.Integer, db.ForeignKey("words.id"), nullable=False)
    folder_id = db.Column(db.Integer, db.ForeignKey("folders.id"), nullable=False)

    date_added = db.Column(db.DateTime())
    
    def __repr__(self):
        return f"<Word {self.word}>"