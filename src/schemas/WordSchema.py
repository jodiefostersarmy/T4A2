from main import ma
from models.Word import Word
from marshmallow.validate import Length


class WordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Word

    word = ma.String(required=True, validate=Length(min=3))
    definition = ma.String(required=True, validate=Length(min=5))
    pronunciation = ma.String(required=True, validate=Length(min=1))

word_schema = WordSchema()
words_schema = WordSchema(many=True)