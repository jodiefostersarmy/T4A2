from main import ma
from models.Folder import Folder
from schemas.UserSchema import UserSchema
from marshmallow.validate import Length

class FolderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Folder

    title = ma.String(required=True, validate=Length(min=1, max=50))
    description = ma.String(required=False, validate=Length(max=120))
    date_created = ma.String(required=True)   # change this to datetime
    image = ma.String()
    # user = ma.Nested(UserSchema)


folder_schema = FolderSchema()
folders_schema = FolderSchema(many=True)