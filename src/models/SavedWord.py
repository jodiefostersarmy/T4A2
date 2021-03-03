from main import db

class SavedWord(db.Model):
    __tablename__= "saved_words"

    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey("words.id"), nullable=False)
    
    date_added = db.Column(db.String())
    notification = db.Column(db.Boolean())


    def __repr__(self):
        return f"<Word {self.word}>"