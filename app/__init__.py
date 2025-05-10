from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for your frontend
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5173", "https://gradely-srgec.netlify.app"]}})

# Import routes
from . import routes
