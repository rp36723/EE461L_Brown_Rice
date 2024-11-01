# Import necessary libraries and modules
from pymongo import MongoClient

import projectsDatabase
import cipher

'''
Structure of User entry:
User = {
    'username': username,
    'userId': userId,
    'password': password,
    'projects': [project1_ID, project2_ID, ...]
}
'''

# Function to add a new user
def addUser(database, username, userId, password):
    # Add a new user to the database
    users = database['users']
    if not username or not userId or not password:
        return "FAILURE: Missing required fields"
    try:
        if users.find_one({"username": username, 'userId': userId}):
            return "FAILURE: Username already exists"
        new_user = {
            'username': username,
            'userId': userId,
            'password': cipher.encrypt(password, 5, 1),
            'projects': []
        }
        server_response = users.insert_one(new_user)
        if server_response.acknowledged:
            return "SUCCESS: User added"
        else:
            return "FAILURE: User not added"
    except Exception as e:
        return "FAILURE: " + str(e)

# Helper function to query a user by username and userId
def __queryUser(database, username, userId):
    # Query and return a user from the database
    users = database['users']
    try:
        return users.find_one({"username": username, 'userId': userId})
    except Exception as e:
        print("User Query FAILURE: " + str(e))
        return None

# Function to log in a user
def login(database, username, userId, password):
    # Authenticate a user and return login status
    users = database['users']
    if not username or not userId or not password:
        return "FAILURE: Missing required fields"
    try:
        user = __queryUser(database, username, userId)
        if user:
            if cipher.decrypt(user['password'], 5, 1) == password:
                return "SUCCESS: User logged in"
            else:
                return "FAILURE: Incorrect password"
        else:
            return "FAILURE: User not found"
    except Exception as e:
        return "FAILURE: " + str(e)

# Function to add a user to a project
def joinProject(database, userId, projectId):
    # Add a user to a specified project
    #TODO: Implement this function
    pass

# Function to get the list of projects for a user
def getUserProjectsList(database, userId):
    # Get and return the list of projects a user is part of
    #TODO: Implement this function
    pass

