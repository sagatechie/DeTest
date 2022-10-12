"""
This module contains the required configs to support the application.
"""

# Import the built-in modules
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy


DB_URL = r"sqlite:///db\weather_crop.db" # DB URI where application data will be stored

# Create the flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL # configure the DB

# Create DB object - will be used to interact with the actual DB.
db = SQLAlchemy(app)

# Create the marshmallow object for easy serialization/deserialization of Data Model objects
ma = Marshmallow(app)
