from flask import Blueprint, request, jsonify, abort, render_template, flash, redirect, url_for
from main import db, bcrypt
from models.User import User
from schemas.UserSchema import user_schema, users_schema
from flask_jwt_extended import create_access_token
import time
from datetime import timedelta
from flask_login import login_user, current_user, logout_user

auth = Blueprint('auth', __name__)

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
    # user.mobile_number = user_fields["mobile_number"]                             # kept this here, for when I fix up the app post bootcamp
    user.email = email
    # if admin:
    #     user.is_admin = admin                                                     # kept this here, for when I fix up the app post bootcamp
    user.password = bcrypt.generate_password_hash(password).decode("utf-8")
    user.join_date = time.time()

    db.session.add(user)
    db.session.commit()

    return redirect(url_for('user.all_users'))


@auth.route("/login", methods=["GET","POST"])
def auth_login():
    if request.method == "GET":
        return render_template('login.html')

    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()

    if not user or not bcrypt.check_password_hash(user.password, password):
        return abort(401, description="Incorrect username or password")
    print(current_user)
    login_user(user)
    print(current_user.id)
    # expiry = timedelta(days=1)
    # access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
    # return jsonify({ "token": access_token })
    return redirect(url_for('user.search'))


# @auth.route("/users", methods=["GET"])
# def user_index():
#     users = User.query.all()
#     return jsonify(users_schema.dump(users))

@auth.route("/", methods=["GET"])
def index():
    return render_template('search.html')

@auth.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for('auth.auth_register'))