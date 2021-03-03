from main import ma                                                     # Import the serialization object from main
from models.User import User                                            # Importign the User model
from marshmallow.validate import Length, Email                          # Import the length class that will allow us to validate the length of the string 

class UserSchema(ma.SQLAlchemyAutoSchema):                              # Generates Schema automatically
    class Meta:
        model = User                                                    # Generate Schema using the User Model
        load_only = ["password"]                                        # This will load the password but it wont send it to the front end

    name = ma.String(required=True)
    email = ma.String(required=True, validate=[Length(min=4), Email()])
    password = ma.String(required=True, validate=Length(min=6))
    mobile_number = ma.Integer(required=True)
    join_date = ma.Integer(required=False)                               # using INTEGER while testing, change to datetime at some point and also required=True
    is_admin = ma.Boolean(required=True)

user_schema = UserSchema()                                              # Schema for a single user
users_schema = UserSchema(many=True)                                    # Schema for multiple users    