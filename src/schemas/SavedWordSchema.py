from main import ma
from models.SavedWord import SavedWord          # Importing SavedWord Class from Models
# from marshmallow.validate import Predicate
from schemas.UserSchema import UserSchema       # Importing the UserSchema for reference in class below
from schemas.WordSchema import WordSchema       # Importing the UserSchema for reference in class below

class SavedWordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SavedWord                       # Generating this schema by using the SavedWord model
        include_fk = True

    notification = ma.Boolean(required=True)
    date_added = ma.String()     # turn to required when basic scaffold done
    user = ma.Nested(UserSchema)                # nesting my user schema in the savedwordschema
    word = ma.Nested(WordSchema)                # nesting my word schema in the savedwordschema


savedword_schema = SavedWordSchema()
savedwords_schema = SavedWordSchema(many=True)