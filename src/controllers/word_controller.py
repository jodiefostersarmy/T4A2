from models.Word import Word                                           # Importing the Profile Model
from models.User import User                                           # Importing the User Model
from schemas.WordSchema import word_schema, words_schema      # Importing the Profile Schema
from main import db                                                    # This is the db instance created by SQLAlchemy
from sqlalchemy.orm import joinedload                                  # 
from flask import Blueprint, request, jsonify, abort                   # Import flask and various sub packages

words = Blueprint("words", __name__, url_prefix="/words")      # Creating the profile blueprint 

@words.route("/", methods=["GET"])                                      # Route for word index
def word_index():                                                       # This function will run when the route is matched
    words = Word.query.all()
    return jsonify(words_schema.dump(words))                            # Returning all the profiles in json

# @words.route("/", methods=["POST"])                                 # Route for the profile create
# @jwt_required                                                          # JWT token is required for this route
# @verify_user                                                           # Auth service to make sure the correct user owns this profile
# def word_create(user):                                              # This function will run when the route is matched

#     if user.profile != []:                                             # If the user already has a profile
#         return abort(400, description="User already has profile")      # Return the error "Email already in use"

#     profile_fields = profile_schema.load(request.json)                 # Retrieving the fields from the request
#     profile = Profile.query.filter_by(username=profile_fields["username"]).first() # Query the user table with the email and return the first user

#     if profile:                                                        # If a user is returned 
#         return abort(400, description="username already in use")       # Return the error "Email already in use"

#     new_profile = Profile()                                            # Create a new profile object from the Profile model 
#     new_profile.username = profile_fields["username"]                  # Add username to the new_profile 
#     new_profile.firstname = profile_fields["firstname"]                # Add username to the new_profile 
#     new_profile.lastname = profile_fields["lastname"]                  # Add username to the new_profile 
#     new_profile.user_id = user.id                                      # Add username to the new_profile 
    
#     user.profile.append(new_profile)                                   # Add profile to the user
#     db.session.commit()                                                # Commit the DB session
      
#     return jsonify(profile_schema.dump(new_profile))                   # Return the newly created profile

# @words.route("/<int:id>", methods=["GET"])                          # Route for the profile create
# def profile_show(id):                                                  # Auth service to make sure the correct user owns this profile
#     profile = Profile.query.get(id)                                    # Query the user table with the id then return that user
#     return jsonify(profile_schema.dump(profile))                       # Returb the profile in JSON
    

# @words.route("/<int:id>", methods=["PUT", "PATCH"])                 # Route for the profile create
# @jwt_required                                                          # JWT token is required for this route
# @verify_user                                                           # Auth service to make sure the correct user owns this profile
# def profile_update(user, id):                             
    
#     profile_fields = profile_schema.load(request.json)                 # Retrieving the fields from the request
#     profile = Profile.query.filter_by(id=id, user_id=user.id)          # Query the user table with the id and the user id then return the first user
#     if not profile:                                                    # If there is no profile found
#         return abort(401, description="Unauthorized to update this profile")  # Return this error

#     print(profile.__dict__)
#     profile.update(profile_fields)                                     # Update the fields with the data from the request
#     db.session.commit()                                                # Commit the session to the db
#     return jsonify(profile_schema.dump(profile[0]))                    # Return the recently committed profile


# @words.route("/<int:id>", methods=["DELETE"])                       # Route for the profile create
# @jwt_required        
# @verify_user                                                           # Auth service to make sure the correct user owns this profile
# def profile_delete(user, id):
#     profile = Profile.query.filter_by(id=id, user_id=user.id).first()  # Query the user table with the id and the user id then return the first user
#     # print(profile[0].__dict__)
#     # return("bills")
#     if not profile:                                                    # If there is any number other than 1
#         return abort(400, description="Unauthorized to update this profile") # Return this error
    
#     db.session.delete(profile)
#     db.session.commit()                                                # Commit the session to the db
#     return jsonify(profile_schema.dump(profile))                       # Return the deleted profile
