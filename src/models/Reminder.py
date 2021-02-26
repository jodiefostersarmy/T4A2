from main import db
from sqlalchemy.orm import backref

class Reminder(db.Model):
    __tablename__= "reminders"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    word_id = db.Column(db.Integer, db.ForeignKey('words.id'), primary_key=True)
    notification_type = db.Column(db.Enum(name='type'), nullable=False)
    notification_time = db.Column(db.Enum(name='time'), nullable=False)
    last_update = db.Column(db.DateTime(), nullable=True)

    def __repr__(self):
        return f"<Reminder: {self.notification_type}>"