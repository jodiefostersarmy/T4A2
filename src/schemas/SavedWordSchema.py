from main import ma
from models.SavedWord import SavedWord
# from marshmallow.validate import Predicate
from schemas.UserSchema import UserSchema
from schemas.WordSchema import WordSchema

class SavedWordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SavedWord
        include_fk = True

    notification = ma.Boolean(required=True)
    date_added = ma.String()
    user = ma.Nested(UserSchema)
    word = ma.Nested(WordSchema)


savedword_schema = SavedWordSchema()
savedwords_schema = SavedWordSchema(many=True)