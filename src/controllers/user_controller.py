from models.User import User
from schemas.UserSchema import users_schema, user_schema
from main import db
from main import bcrypt
from flask_jwt_extended import create_access_token
from datetime import timedelta
from flask import Blueprint, request, jsonify, abort

user = Blueprint('user', __name__, url_prefix="/user")

@user.route("/", methods=["GET"])
def all_users():
    """Return all users""" 
    users = User.query.all()
    return jsonify(users_schema.dump(users))
    
    # Goal: Only return all users if_admin=True
    # admin = User.query.filter_by(is_admin=user_fields["is_admin"]).first() 
    # if admin:
    #     return jsonify(users_schema.dump(users))
    # else:
    #     return abort(401, description="You are not authorized to make this request")

@user.route("/<int:id>", methods=["GET"])
def get_user(id):
    """Return single user"""
    user = User.query.get(id)
    return jsonify(user_schema.dump(user))

@user.route("/<int:id>", methods=["DELETE"])
# @jwt_required // Throw these in later when you've outlined whole backend
# @verify_user
def delete_user(id):
    """Delete single user"""
    # note: still need user_id verification for authorised deletion or is_admin
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify(user_schema.dump(user))

@user.route("/<int:id>", methods=["PUT", "PATCH"])  # when browser hits this endpoint
def update_user(id):                                # it will run user update method
    """Update single user"""                        # i want to update a single user
    user_fields = user_schema.load(request.json)    # I will load all the attributes for the User model              
    user = User.query.filter_by(id=id)              # I want to select the user with id = <int:id> from the URI

    user.update(user_fields)                        # I want you to update the User account with fields input in the JSON body from insomnia
    db.session.commit()                             # commit session to db with updated details
    
    # return jsonify(user_schema.dump(user))
    return "Updated User"                           # Return if successful


@user.route("/register", methods=["POST"])
def user_register():
    """Create user account"""
    user_fields = user_schema.load(request.json)
    email = User.query.filter_by(email=user_fields["email"]).first()
    mobile = User.query.filter_by(mobile_number=user_fields["mobile_number"]).first() 
    
    if email:
        return abort(400, description="Email already in use")
    
    if mobile:
        return abort(400, description="Mobile already in use")

    user = User()

    user.name = user_fields["name"]
    user.mobile_number = user_fields["mobile_number"]
    user.join_date = user_fields["join_date"]
    user.email = user_fields["email"]
    user.password = bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8")

    db.session.add(user)
    db.session.commit()

    return jsonify(user_schema.dump(user))


@user.route("/login", methods=["POST"])
def user_login():
    """Log in user with user details"""
    user_fields = user_schema.load(request.json)
    user = User.query.filter_by(email=user_fields["email"]).first()

    if not user or not bcrypt.check_password_hash(user.password, user_fields["password"]):
        return abort(401, description="Incorrect username or password")

    expiry = timedelta(days=1)
    access_token = create_access_token(identity=str(user.id), expires_delta=expiry)

    return jsonify({ "token": access_token })


# @user.route("/logout", methods=["GET"])
# def user_logout():
#     session.clear()
#     return "Logged out"