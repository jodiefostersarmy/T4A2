from main import db
from sqlalchemy.orm import backref
from models.SavedWord import SavedWord
from flask_login import UserMixin

def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user

class User(db.Model, UserMixin):
    __tablename__= "users"

    id = db.Column(db.Integer, primary_key=True)
    saved_word = db.relationship(
        "SavedWord", backref="user", 
        lazy="dynamic", 
        cascade="all, delete", 
        passive_deletes=True
    )

    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    mobile_number = db.Column(db.BigInteger(), nullable=True)
    join_date = db.Column(db.BigInteger())
    is_admin = db.Column(db.Boolean(), nullable=True, default=False)

    def __repr__(self):
        return f"<User: {self.email}>"