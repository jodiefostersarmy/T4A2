from main import ma
from models.FolderWord import FolderWord
from schemas.WordSchema import WordSchema
from schemas.FolderSchema import FolderSchema
from marshmallow.validate import Length

class FolderedWordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FolderWord

    title = ma.String(required=True, validate=Length(min=1, max=50))
    description = ma.String(required=False, validate=Length(max=120))
    date_created = ma.DateTime(required=True)
    image = ma.Integer(required=False)
    word = ma.Nested(WordSchema)
    folder = ma.Nested(FolderSchema)


folderword_schema = FolderedWordSchema()
folderwords_schema = FolderedWordSchema(many=True)