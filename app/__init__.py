import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.auth.views import auth
from flask_bcrypt import Bcrypt

# Initialize application
app = Flask(__name__)

# app configuration
app_settings = os.getenv(
    'APP_SETTINGS',
    'app.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

# Initialize Bcrypt
bcrypt = Bcrypt(app)

# Initialize Flask Sql Alchemy
db = SQLAlchemy(app)

# Register blue prints
app.register_blueprint(auth)
