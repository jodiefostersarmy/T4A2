from main import ma                                                   # Import the serialization object from main
from models.Word import Word                                          # Importign the Profile model
from marshmallow.validate import Length                               # Import the length class that will allow us to validate the length of the string 


class WordSchema(ma.SQLAlchemyAutoSchema):                            # Generates Schema automatically
    class Meta:
        model = Word                                                    # Generate Schema using the Word Model

    word = ma.String(required=True, validate=Length(min=3))            # word is required and the minimum length is 3
    definition = ma.String(required=True, validate=Length(min=5))      # definition is required and the minimum length is 5
    pronunciation = ma.String(required=True, validate=Length(min=1))   # pronunciation is required and the minimum length is 1

word_schema = WordSchema()                                            # Schema for a single word
words_schema = WordSchema(many=True)                                  # Schema for multiple words