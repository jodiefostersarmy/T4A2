from main import db

class SavedWord(db.Model):
    __tablename__= "saved_words"

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(), nullable=False, unique=True)
    definition = db.Column(db.String(), nullable=False)
    pronunciation = db.Column(db.String(), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey("words.id"), nullable=False)

    def __repr__(self):
        return f"<Word {self.word}>"