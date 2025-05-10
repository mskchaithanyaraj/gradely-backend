from app.routes import app

if __name__ == '__main__':
    # Allow external connections by setting host to '0.0.0.0'
    app.run(debug=True, host='0.0.0.0', port=5000)
