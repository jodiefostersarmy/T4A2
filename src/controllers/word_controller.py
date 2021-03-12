from models.Word import Word
from models.User import User
from models.SavedWord import SavedWord
from schemas.WordSchema import word_schema, words_schema
from schemas.SavedWordSchema import savedword_schema, savedwords_schema
from main import db
from sqlalchemy.orm import joinedload
from flask import Blueprint, request, jsonify, abort, render_template

words = Blueprint("words", __name__, url_prefix="/words")

@words.route("/", methods=["GET"])
def word_index():
    words = Word.query.all()
    return jsonify(words_schema.dump(words))


@words.route("/", methods=["POST"])
def word_create():
    """Create word as user"""
    word_fields = word_schema.load(request.json)

    word = Word.query.filter_by(word=word_fields["word"]).first()

    if word:
        return abort(400, description="Word already in database")
    
    new_word = Word()
    new_word.word = word_fields["word"]                         # using schema loaded above, insert new value into "word_self" column 
    new_word.definition = word_fields["definition"]             # using schema loaded above, insert new value into "definition" column 
    new_word.pronunciation = word_fields["pronunciation"]       # using schema loaded above, insert new value into "pronunciation" column 

    db.session.add(new_word)
    db.session.commit()
    return jsonify(word_schema.dump(new_word))

@words.route("/<int:id>", methods=["GET"])
def single_word(id):
    """Return a single word"""
    word = Word.query.get(id)

    if word:
        return render_template("single_word.html", word = word)
    else:
        return "No such word"


@words.route("/<int:id>", methods=["DELETE"])
def word_delete(id):
    """Allow deletion of a word if user is_admin"""
    word = Word.query.filter_by(id=id).first()

    if not word:
        return abort(400, description="This word does not exist")

    db.session.delete(word)
    db.session.commit()
    return "Word deleted"