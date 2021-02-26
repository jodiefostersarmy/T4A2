from main import ma                                                     # Import the serialization object from main
from models.User import User                                            # Importign the User model
from marshmallow.validate import Length, Email                          # Import the length class that will allow us to validate the length of the string 

class UserSchema(ma.SQLAlchemyAutoSchema):                              # Generates Schema automatically
    class Meta:
        model = User                                                    # Generate Schema using the User Model
        load_only = ["password"]                                        # This will load the password but it wont send it to the front end

    email = ma.String(required=True, validate=[Length(min=4), Email()])
    password = ma.String(required=True, validate=Length(min=6))
    mobile_number = ma.Integer(required=True, validate=Length(min=6, max=20))
    join_date = ma.DateTime(required=True)


user_schema = UserSchema()                                              # Schema for a single user
users_schema = UserSchema(many=True)                                    # Schema for multiple users    