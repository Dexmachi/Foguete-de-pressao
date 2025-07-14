from flask import Flask
import logging
from flask_cors import CORS
from app.config import Config

Config.setup_logging()

#app = Flask(__name__, template_folder=Config.TEMPLATES_DIR, static_folder=Config.STATIC_DIR)
#app = Flask('app', template_folder=Config.TEMPLATES_DIR, static_folder=Config.STATIC_DIR)
app = Flask(__name__)
CORS(app)

from app import routes