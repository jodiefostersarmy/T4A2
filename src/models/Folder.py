from main import db
from sqlalchemy.orm import backref
from models.FolderWord import FolderWord

class Folder(db.Model):
    __tablename__ = "folders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    foldered_word = db.relationship("FolderWord", backref=backref("folder_words", uselist=False))
    
    title = db.Column(db.String(), nullable=False, unique=True)
    description = db.Column(db.String(), nullable=False)
    date_created = db.Column(db.String(), nullable=False)
    image = db.Column(db.Integer, nullable=True, unique=True)


    
    def __repr__(self):
        return f"<Profile {self.username}>"