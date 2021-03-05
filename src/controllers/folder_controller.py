from models.Folder import Folder
from models.User import User
from models.FolderWord import FolderWord
from models.Word import Word
from schemas.WordSchema import word_schema, words_schema
from schemas.FolderedWordSchema import folderword_schema, folderwords_schema
from schemas.FolderSchema import folder_schema, folders_schema
from main import db
from sqlalchemy.orm import joinedload
from flask import Blueprint, request, jsonify, abort

folders = Blueprint("folders", __name__, url_prefix="/folders")

@folders.route("/", methods=["GET"])
def folder_index():
    folders = Folder.query.all()
    return jsonify(folders_schema.dump(folders))


@folders.route("/", methods=["POST"])
def folder_create():
    """Create folder as user"""
    folder_fields = folder_schema.load(request.json)

    folder = Folder.query.filter_by(title=folder_fields["title"]).first()

    if folder:
        return abort(400, description='Folder title is already in use')

    new_folder = Folder()
    new_folder.title = folder_fields["title"]
    new_folder.description = folder_fields["description"]
    new_folder.date_created = folder_fields["date_created"]
    new_folder.image = folder_fields["image"]

    db.session.add(new_folder)
    db.session.commit()
    return jsonify(folder_schema.dump(new_folder))


@folders.route("/<int:id>", methods=["GET"])
def single_folder(id):
    """Return a single folder with all words"""

    folder_words = FolderWord.query.all()
    return jsonify(words_schema.dump(folder_words))


@folders.route("/<int:id>", methods=["PUT", "PATCH"])
def folder_update(id):                             
    """Update a folder"""

    folder_fields = folder_schema.load(request.json)
    folder = Folder.query.filter_by(id=id)

    folder.update(folder_fields)
    db.session.commit()
    return jsonify(folder_schema.dump(folder[0]))


@folders.route("/<int:id>", methods=["DELETE"])
def folder_delete(id):
    """Allow deletion of a folder if user owns folder"""
    folder = Folder.query.filter_by(id=id).first()
    
    db.session.delete(folder)
    db.session.commit()
    return jsonify(folder_schema.dump(folder))

