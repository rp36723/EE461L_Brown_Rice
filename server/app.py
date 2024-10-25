from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Temporary list of current usernames and passwords
users = [
    {"username": "admin", "password": "password123"},
    {"username": "user1", "password": "pass1"},
    {"username": "user2", "password": "pass2"}
]

# Route for user login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"success": False, "message": "Missing username or password"}), 400

    for user in users:
        if user['username'] == username and user['password'] == password:
            return jsonify({"success": True, "message": "Login successful"}), 200

    return jsonify({"success": False, "message": "Invalid credentials"}), 401

# Route for adding a new user
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json() or {}
    new_username = data.get('username')
    new_password = data.get('password')

    if not new_username or not new_password:
        return jsonify({"success": False, "message": "Missing username or password"}), 400

    # Check if username already exists
    for user in users:
        if user['username'] == new_username:
            return jsonify({"success": False, "message": "Username already exists"}), 400

    # Add the new user to the list
    users.append({"username": new_username, "password": new_password})
    return jsonify({"success": True, "message": f"User {new_username} added successfully"}), 201

if __name__ == '__main__':
    app.run(port=5000)
