from flask import Blueprint, request, jsonify, abort
from main import db, bcrypt
from models.User import User
from schemas.UserSchema import user_schema
from flask_jwt_extended import create_access_token
from datetime import timedelta

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route("/register", methods=["POST"])
def auth_register():
    user_fields = user_schema.load(request.json)

    user = User.query.filter_by(email=user_fields["email"]).first()
    user_number = User.query.filter_by(mobile_number=user_fields["mobile_number"]).first()

    if user:
        return abort(400, description="Email already registered")

    if user_number:
        return abort(400, description="Mobile already registered")

    user = User()
    user.name = user_fields["name"]
    user.mobile_number = user_fields["mobile_number"]
    user.email = user_fields["email"]
    if "is_admin" in user_fields:
        user.is_admin = user_fields["is_admin"]
    user.password = bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8")

    db.session.add(user)
    db.session.commit()

    return jsonify(user_schema.dump(user))


@auth.route("/login", methods=["POST"])
def auth_login():
    user_fields = user_schema.load(request.json)

    user = User.query.filter_by(email=user_fields["email"]).first()

    if not user or not bcrypt.check_password_hash(user.password, user_fields["password"]):
        return abort(401, description="Incorrect username and password")

    expiry = timedelta(days=1)
    access_token = create_access_token(identity=str(user.id), expires_delta=expiry)

    return jsonify({ "token": access_token })