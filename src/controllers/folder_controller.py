from models.Word import Word
from models.User import User
from schemas.WordSchema import word_schema, words_schema
from main import db
from sqlalchemy.orm import joinedload
from flask import Blueprint, request, jsonify, abort

words = Blueprint("words", __name__, url_prefix="/words")

@words.route("/", methods=["GET"])
def word_index():
    words = Word.query.all()
    return jsonify(words_schema.dump(words))

@words.route("/", methods=["POST"])
# @jwt_required
def word_create():
    """Create word as user"""
    word_fields = word_schema.load(request.json)
    
    # word = Word.query.filter_by(username=user_fields["username"]).first()  // see line 32 & 33

    # if not user:
    #     return abort(401, description="Cannot save this word")

    new_word = Word()                                           # create a new instance of the Word object
    new_word.word_self = word_fields["word_self"]               # using schema loaded above, insert new value into "word_self" column 
    new_word.definition = word_fields["definition"]             # using schema loaded above, insert new value into "definition" column 
    new_word.pronunciation = word_fields["pronunciation"]       # using schema loaded above, insert new value into "pronunciation" column 
    
    # new_word.user_id = user.id       // do not need this line until you have savedword controller up and running
    # user.profile.append(new_profile) // as above, so below

    db.session.add(new_word)
    db.session.commit()
    return jsonify(word_schema.dump(new_word))

@words.route("/<int:id>", methods=["GET"])
def single_word(id):
    """Return a single word"""
    word = Word.query.get(id)
    return jsonify(word_schema.dump(word))









# below two routes may not be needed, but this may be an additional feature added later on.


# @words.route("/<int:id>", methods=["DELETE"])
# def word_delete(user, id):
#     """Allow deletion of a word if user is_admin"""
#     word = Word.query.filter_by(id=id, user_id=user.id).first()

#     if not is_admin: 
#         return abort(400, description="Unauthorized to delete this word")
    
#     db.session.delete(word)
#     db.session.commit()
#     return jsonify(word_schema.dump(word))



# @words.route("/<int:id>", methods=["PUT", "PATCH"])
# def profile_update(user, id):                             
#     """Update a word"""

#     profile_fields = profile_schema.load(request.json)
#     profile = Profile.query.filter_by(id=id, user_id=user.id)
#     if not profile:
#         return abort(401, description="Unauthorized to update this profile")

#     print(profile.__dict__)
#     profile.update(profile_fields)
#     db.session.commit()
#     return jsonify(profile_schema.dump(profile[0]))