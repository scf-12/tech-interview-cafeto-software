"""
Flask application configuration file, in charge of initializing
and setting the required information for the app to execute.
"""
from flask import Flask

app = Flask(__name__)

from app import views
from app import models
from app import handlers
