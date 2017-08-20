import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.auth.views import auth

# Initialize application
app = Flask(__name__)

# app configuration
app_settings = os.getenv(
    'APP_SETTINGS',
    'app.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

# Initialize Flask Sql Alchemy
db = SQLAlchemy(app)

# Initialize Flask Migrate
migrate = Migrate(app, db)

# Register blue prints
app.register_blueprint(auth)
