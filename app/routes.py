from flask import request, jsonify
from . import app
from .scraper import login_and_fetch_data

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    result = login_and_fetch_data(username, password)
    return jsonify(result)
