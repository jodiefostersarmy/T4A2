from main import db                                                                  # This is the db instance created by SQLAlchemy

class Folder(db.Model):                                                             # Creating a Profile class inheriting from db.Model
    __tablename__ = "folders"                                                       # Explicitally providing the name of the table

    id = db.Column(db.Integer, primary_key=True)                                     # Creates a column called id and sets it al the primary key
    title = db.Column(db.String(), nullable=False, unique=True)                      # Profilename, string, must be present, must be unique
    description = db.Column(db.String(), nullable=False)                             # Firstname, string, must be present
    date_created = db.Column(db.String(), nullable=False)                            # Lastname, string, must be present

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)       # user_id is an integer and the Foreign key comes from the users table id. It is required
    
    def __repr__(self):                                                              # Reresentitive state
        return f"<Profile {self.username}>"                                          # When the Profile is printed it now shows the username instead of the id