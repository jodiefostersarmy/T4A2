from main import db                                             # This is the db instance created by SQLAlchemy
from flask import Blueprint                                     # Use blueprints instead of passing the app object around 

db_commands = Blueprint("db-custom", __name__)                  # Creates the blueprint
"""
A Blueprint is essentially a constructor, and is similar to a Flask application object, but is not an application.
It is a set of operations which can be registered on an application, even multiple times.
They provide separation at a Flask level, share app config, and can change an application object without being registered.
However, you cannot unregister a blueprint once the application has been created, hence the reason why we drop the tables
in testing if we add a new column or change the validations.
"""

@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created")  

@db_commands.cli.command("drop")                                # this function will run when "flask db-custom drop" is run"
def drop_db():
    db.drop_all()                                               # Drop all tables  
    db.engine.execute("DROP TABLE IF EXISTS alembic_version;")  # Drop table for migrations
    print("Tables deleted")                                     # Print message to indicate tables are dropped



@db_commands.cli.command("seed")                                # this fronction will run when "flask db-custom seed" is run"
def seed_db():
    """Create arbitrary data for testing"""
    
    from models.User import User                          # Importing the User model
    from models.Word import Word                          # Importing the Profile model
    from models.Folder import Folder
    from models.SavedWord import SavedWord
    from models.FolderWord import FolderWord
    from main import bcrypt                                     # Hashing module for the passwords
    from faker import Faker                                     # Importing the faker module for fake data
    import random                                               # Importing random from the python standard library

    faker = Faker()
    users = []
    words = []
    folders = []

    for i in range(5):                                                           # Do this 5 times
        user = User()                                                           # Create an user object from the User model
        user.name = faker.name()                                                # assigns fake name for user object from faker module
        user.email = f"test{i+1}@test.com"                                      # Assign an email to the user object
        user.password = bcrypt.generate_password_hash("123456").decode("utf-8") # Assign ta hashed password to the user object
        user.mobile_number = faker.msisdn()
        # user.join_date = faker.msisdn()
        db.session.add(user)                                                    # Add the user to the db session
        users.append(user)                                                      # Append the user to the users list

    db.session.commit()                                                         # Commit the seeion to the db 

    for i in range(5):
        word = Word()                                                     # Create a profile object from the Profile model                 

        word.word = faker.word()                                   # Add a username to the profile object
        word.definition = faker.words()                                  # Add a firstname to the profile object
        word.pronunciation = faker.last_name()                                    # Add a lastname to the profile object
        word.user_id = users[i].id                                           # Add a user_id to the profile object. This comes from real ids from the users list

        words.append(word)
        db.session.add(word)                                                 # Add the profile to the session

    db.session.commit()                                                         # Commit the session to the database

    for i in range(5):
        savedWord = SavedWord()

        savedWord.user_id = users[i].id
        savedWord.word_id = words[i].id
    
        db.session.add(savedWord)
    
    db.session.commit()

    for i in range(5):
        folder = Folder()

        folder.title = faker.word()
        folder.description = faker.words()
        folder.date_created = faker.msisdn()
        folder.image = faker.msisdn()

        folders.append(folder)

        db.session.add(folder)
    
    db.session.commit()

    for i in range(5):
        folderword = FolderWord()

        folderword.word_id = words[i].id
        folderword.folder_id = folders[i].id

        db.session.add(folderword)
    
    db.session.commit()

    print("Tables seeded")                                                      # Print a message to let the user know they 