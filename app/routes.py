from flask import request, jsonify
from . import app
from .scraper import login_and_fetch_data
import socket

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    result = login_and_fetch_data(username, password)
    return jsonify(result)

@app.route('/api/hello')
def hello_world():
    return 'Hello from Flask!'


@app.route("/api/debug-dns")
def debug_dns():
    try:
        ip = socket.gethostbyname("gecgudlavalleruonlinepayments.com")
        return jsonify({"status": "success", "ip": ip})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)})