# SQLite3 setup
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
DATABASE_CONNECT_OPTIONS = {}
SQLALCHEMY_TRACK_MODIFICATIONS = False

# MySQL setup
# import pymysql
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://<user>:<pass>@<host>/<db>'
# DATABASE_CONNECT_OPTIONS = {}
# SQLALCHEMY_TRACK_MODIFICATIONS = False

# Statement for enabling the development environment
DEBUG = False
TESTING = False

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "<secret>"

# Secret key for signing cookies
SECRET_KEY = "<secret>"

UPLOAD_FOLDER = './uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'csv'}

ADMIN_PER_PAGE = 10

MINIFY_PAGE = True
