from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
from bson.objectid import ObjectId
import os

import usersDatabase
import projectsDatabase
import hardwareDatabase

load_dotenv()

# Use local MongoDB if no environment variable is set
MONGODB_SERVER = os.getenv("MONGODB_URI", "mongodb://localhost:27017/hardware_checkout")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

def get_db():
    try:
        client = MongoClient(MONGODB_SERVER)
        # Test the connection
        client.admin.command('ping')
        return client, client['hardware_checkout']
    except Exception as e:
        print(f"Database connection error: {e}")
        raise

# Test route to verify backend is working
@app.route('/')
def home():
    return jsonify({"message": "Server is running!"})

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        userId = data.get('userId', username)

        print(f"Login attempt for user: {username}")  # Debug logging

        if not all([username, password]):
            print("Missing credentials")  # Debug logging
            return jsonify({'success': False, 'message': 'Missing credentials'}), 400

        client, db = get_db()
        result = usersDatabase.login(db, username, userId, password)
        client.close()

        print(f"Login result: {result}")  # Debug logging

        if result.startswith('SUCCESS'):
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'username': username,
                'userId': userId
            })
        return jsonify({'success': False, 'message': result}), 401
        
    except Exception as e:
        print(f"Login error: {str(e)}")  # Debug logging
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/add_user', methods=['POST'])
def add_user():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        userId = data.get('userId', username)

        if not all([username, password]):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400

        client, db = get_db()
        result = usersDatabase.addUser(db, username, userId, password)
        client.close()

        if "Username already exists" in result:
            return jsonify({
                'success': False,
                'message': 'This username is already taken. Please choose another one.'
            }), 400

        if result.startswith('SUCCESS'):
            return jsonify({'success': True, 'message': 'User registered successfully'})
        return jsonify({'success': False, 'message': result}), 400

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/get_hardware_sets', methods=['GET'])
def get_hardware_sets():
    try:
        client, db = get_db()
        hardware_sets = list(db.hardwareSets.find({}, {'_id': 0}))
        client.close()
        return jsonify({'success': True, 'hardware_sets': hardware_sets})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/create_project', methods=['POST'])
def create_project():
    try:
        data = request.get_json()
        project_name = data.get('projectName')
        project_id = data.get('projectId')
        description = data.get('description')
        user_id = data.get('userId')  # Get the userId from the request
        
        if not all([project_name, project_id, user_id]):  # Add user_id to required fields
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400

        client, db = get_db()
        # Pass the user_id as creator_id to the createProject function
        result = projectsDatabase.createProject(db, project_name, project_id, description, user_id)
        client.close()

        if result.startswith('SUCCESS'):
            return jsonify({'success': True, 'message': 'Project created successfully'})
        return jsonify({'success': False, 'message': result}), 400

    except Exception as e:
        print(f"Error creating project: {str(e)}")  # Add error logging
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/join_project', methods=['POST'])
def join_project():
    try:
        data = request.get_json()
        project_id = data.get('projectId')
        user_id = data.get('userId')

        if not all([project_id, user_id]):
            return jsonify({
                'success': False,
                'message': 'Missing required fields'
            }), 400

        client, db = get_db()
        result = projectsDatabase.joinProject(db, project_id, user_id)
        client.close()

        if result.startswith('SUCCESS'):
            return jsonify({
                'success': True,
                'message': 'Successfully joined project'
            })
        return jsonify({
            'success': False,
            'message': result.replace('FAILURE: ', '')
        }), 400

    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/check_out', methods=['POST'])
def check_out():
    try:
        data = request.get_json()
        project_id = data.get('projectId')
        hw_set_name = data.get('hwSetName')
        quantity = data.get('quantity')
        user_id = data.get('userId')

        if not all([project_id, hw_set_name, quantity, user_id]):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400

        client, db = get_db()
        result = projectsDatabase.checkOutHW(db, project_id, hw_set_name, quantity, user_id)
        client.close()

        if result.startswith('SUCCESS'):
            return jsonify({'success': True, 'message': 'Hardware checked out successfully'})
        return jsonify({'success': False, 'message': result}), 400

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/check_in', methods=['POST'])
def check_in():
    try:
        data = request.get_json()
        project_id = data.get('projectId')
        hw_set_name = data.get('hwSetName')
        quantity = data.get('quantity')
        user_id = data.get('userId')

        if not all([project_id, hw_set_name, quantity, user_id]):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400

        client, db = get_db()
        result = projectsDatabase.checkInHW(db, project_id, hw_set_name, quantity, user_id)
        client.close()

        if result.startswith('SUCCESS'):
            return jsonify({'success': True, 'message': 'Hardware checked in successfully'})
        return jsonify({'success': False, 'message': result}), 400

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/get_user_projects', methods=['GET'])
def get_user_projects():
    try:
        user_id = request.args.get('userId')
        if not user_id:
            return jsonify({'success': False, 'message': 'Missing user ID'}), 400

        client, db = get_db()
        print(f"Fetching projects for user: {user_id}")  # Debug logging
        projects = usersDatabase.getUserProjectsList(db, user_id)
        client.close()

        print(f"Found projects: {projects}")  # Debug logging
        return jsonify({
            'success': True,
            'projects': projects
        })
    except Exception as e:
        print(f"Error in get_user_projects: {str(e)}")  # Debug logging
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)