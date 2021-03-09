# When you import a directory but you havent given a specific file name then it will import __init__.py by default

from controllers.user_controller import user                 # Importing the user blueprint
from controllers.word_controller import words
from controllers.auth_controller import auth

registerable_controllers = [
    user,
    words,
    auth
]
