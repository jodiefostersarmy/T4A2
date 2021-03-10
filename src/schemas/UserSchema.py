from main import ma
from models.User import User
from marshmallow.validate import Length, Email

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_only = ["password"]

    name = ma.String(required=True)
    email = ma.String(required=True, validate=[Length(min=4), Email()])
    password = ma.String(required=True, validate=Length(min=6))
    mobile_number = ma.Integer(required=False)
    join_date = ma.Integer(required=False)
    is_admin = ma.Boolean(required=False)

user_schema = UserSchema()
users_schema = UserSchema(many=True)