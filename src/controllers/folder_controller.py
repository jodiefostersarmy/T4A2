from models.Folder import Folder
from models.User import User
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

    new_folder = Folder()
    new_folder.title = folder_fields["title"]
    new_folder.description = folder_fields["description"]
    new_folder.date_created = folder_fields["date_created"]
    new_folder.image = folder_fields["image"]
    # new_folder.user_id = user.id


    db.session.add(new_folder)
    db.session.commit()
    return jsonify(folder_schema.dump(new_folder))


@folders.route("/<int:id>", methods=["GET"])
def single_folder(id):
    """Return a single folder"""
    folder = Folder.query.get(id)
    return jsonify(folder_schema.dump(folder))


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

