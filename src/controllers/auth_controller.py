from flask import Blueprint, request, jsonify, abort, render_template, flash
from main import db, bcrypt
from models.User import User
from schemas.UserSchema import user_schema, users_schema
from flask_jwt_extended import create_access_token
import time

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route("/create-account", methods=["GET","POST"])
def auth_register():
    error = None
    if request.method == "GET":
        return render_template('register.html')


    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    # user_number = User.query.filter_by(mobile_number=user_fields["mobile_number"]).first()

    if user:
        error='This email has already been registered'
        return render_template('register.html', error=error)

    # if user_number:
    #     return abort(400, description="Mobile already registered")                # kept this here, for when I fix up the app post bootcamp

    user = User()
    user.name = name
    # user.mobile_number = user_fields["mobile_number"]
    user.email = email
    # if admin:
    #     user.is_admin = admin
    user.password = bcrypt.generate_password_hash(password).decode("utf-8")
    user.join_date = time.time()

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


# @auth.route("/create-account", methods=["GET"])
# def create_account():
#     return render_template('register.html')

@auth.route("/users", methods=["GET"])
def user_index():
    users = User.query.all()
    return jsonify(users_schema.dump(users))