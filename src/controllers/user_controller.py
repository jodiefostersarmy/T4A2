from models.User import User
from schemas.UserSchema import users_schema, user_schema
from models.Word import Word
from schemas.WordSchema import word_schema, words_schema
from models.SavedWord import SavedWord
from schemas.SavedWordSchema import savedword_schema, savedwords_schema
from main import db, bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import timedelta
from flask import Blueprint, request, jsonify, abort, render_template, Response
import json
import requests
from services.auth_service import verify_user

user = Blueprint('user', __name__, url_prefix="/user")

@user.route("/", methods=["GET"])
def all_users():
    """Return all users"""
    
    users = User.query.all()

    return render_template("users_index.html", users = users)
    # return jsonify(users_schema.dump(users))
    

@user.route("/<int:id>", methods=["GET"])
# @jwt_required
def get_user(id):
    """Return single user"""
    user = User.query.get(id)
    if user:
        return render_template("account_details.html", user=user)   # we assign the variable we want to access for our html template to the SQLalchemy query we have just defined.
    else:
        return "This user does not exist!"          # turn this into an error page
    # return jsonify(user_schema.dump(user))
    

@user.route("/<int:id>", methods=["DELETE"])
# @jwt_required
def delete_user(id):
    """Delete single user"""

    user = User.query.get(id)
    
    db.session.delete(user)
    db.session.commit()

    return "User deleted"


@user.route("/<int:id>", methods=["PUT", "PATCH"])  # when browser hits this endpoint
# @jwt_required
def update_user(id):                                # it will run user update method
    """Update single user"""                        # i want to update a single user

    user_fields = user_schema.load(request.json)    # I will load all the attributes for the User model              
    user = User.query.filter_by(id=id)              # I want to select the user with id = <int:id> from the URI

    user.update(user_fields)                        # I want you to update the User account with fields input in the JSON body from insomnia
    db.session.commit()                             # commit session to db with updated details
    
    return "Updated User"                           # Return if successful


@user.route("/<int:id>/words", methods=["GET"])
@jwt_required
@verify_user
def saved_words(id, user=None):
    """Return words saved by specific user"""

    # user_jwt = get_jwt_identity()
    # user = User.query.get(user_jwt)

    # if user.id != id:
    #     return abort(401, description="You are not authorized to view this database")

    saved_word = SavedWord.query.filter_by(user_id=id)
    is_there_a_word = SavedWord.query.filter_by(user_id=id).first()

    if not is_there_a_word:
        return render_template("no_words.html")
    else:
        return render_template("user_words.html", saved = saved_word) 

@user.route("/<int:id>/save", methods=["POST"])
# @jwt_required
def save_user_word(id):
    """Save word by user"""

    saveword_fields = savedword_schema.load(request.json)

    save_word = SavedWord.query.filter_by(word_id=saveword_fields["word_id"], user_id=id).first()
    """
    word_id is equal to post input.
    user_id is equal to id in uri 
    first() accesses first element in list return as a query is always returned as a list.

    :return: filtered query data
    :rtype: list
    """
    if save_word:                                                                        # checks saved words to see if save_word exists in db
        return abort(400, description='Word is already saved')                           # if exist, throw error and return message

    new_save = SavedWord()
    new_save.user_id = id
    new_save.word_id = saveword_fields["word_id"]
    new_save.date_added = 0
    new_save.notification = saveword_fields["notification"]

    db.session.add(new_save)
    db.session.commit()

    return jsonify(savedword_schema.dump(new_save))

@user.route("/<int:user_id>/words/<int:word_id>", methods=["DELETE"])
# @jwt_required
def delete_user_word(user_id, word_id):
    "delete a user saved word"

    saved_word = SavedWord.query.filter_by(user_id=user_id, word_id=word_id).first()

    if saved_word:
        db.session.delete(saved_word)
        db.session.commit()
        return "Word deleted"    
    else:
        return abort(400, description='This word does not exist in your saved words!')

@user.route("/search/<string:word>", methods=["GET"])
def search(word):
    r = requests.get(f'https://dictionaryapi.com/api/v3/references/collegiate/json/{word}?key=2e5594a3-a9a1-48a8-a698-0cf76ece81e1')
    return render_template("search.html", request=r.json())