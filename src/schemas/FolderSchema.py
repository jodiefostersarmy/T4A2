from main import ma
from models.Folder import Folder
from schemas.UserSchema import UserSchema

class FolderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Folder

    title = ma.String(required=True, validate=Length(min=1, max=50))
    description = ma.String(required=False, validate=Length(max=120))
    date_created = ma.DateTime(required=True)
    image = ma.Integer(required=False)
    user = ma.Nested(UserSchema)


reminder_schema = ReminderSchema()
reminder_schema = ReminderSchema(many=True)