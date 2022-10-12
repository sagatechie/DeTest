"""
This module is used to initialize the DB for the application.
"""

# Import the modules
from sqlalchemy_utils import database_exists, create_database
from config import db, DB_URL



# First check if DB already exist or not.
if database_exists(DB_URL):
    print('Requested DB Already Exists')

# create DB only if DB not exist
if not database_exists(DB_URL):
    print('Creating the requested DB')
    create_database(DB_URL)

# Create the DB objects registerd in the app
print("Create the DB objects registerd in the app")
db.create_all()


