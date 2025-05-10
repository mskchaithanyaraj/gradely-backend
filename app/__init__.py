from flask import Flask
from flask_cors import CORS

app = Flask(__name__)  # Define the Flask app here
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})  # Enable CORS for your frontend
