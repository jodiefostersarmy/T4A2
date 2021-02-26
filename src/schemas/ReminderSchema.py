from main import ma
from models.Reminder import Reminder
from marshmallow.validate import OneOf
from schemas.UserSchema import UserSchema
from schemas.WordSchema import WordSchema

class ReminderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Reminder

    notification_type = ma.String(required=True, validate=validate.OneOf(["web", "mobile", "email", "all"]))
    last_update = ma.DateTime(required=False)
    notification_time = ma.Integer(required=True, validate=validate.OneOf([5, 10, 20, 30]))
    user = ma.Nested(UserSchema)
    word = ma.Nested(WordSchema)


reminder_schema = ReminderSchema()
reminders_schema = ReminderSchema(many=True)