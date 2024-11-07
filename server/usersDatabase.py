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

def addUser(database, username, userId, password):
    """Add a new user to the database with encrypted password."""
    try:
        # Input validation
        if not all([username, userId, password]):
            return "FAILURE: Missing required fields"
        
        users = database['users']
        
        # Check if user exists (by username only)
        if users.find_one({"username": username}):
            return "FAILURE: Username already exists"
            
        # Create new user with encrypted password
        new_user = {
            'username': username,
            'userId': userId,
            'password': cipher.encrypt(password, 5, 1),
            'projects': []
        }
        
        result = users.insert_one(new_user)
        
        if result.inserted_id:
            print(f"User created successfully: {username}")  # Debug logging
            return "SUCCESS: User added"
        return "FAILURE: Database error during user creation"
        
    except Exception as e:
        print(f"Error creating user: {str(e)}")  # Debug logging
        return f"FAILURE: {str(e)}"

def __queryUser(database, username, userId=None):
    """Query a user by username and optionally userId."""
    try:
        users = database['users']
        query = {"username": username}
        if userId:
            query["userId"] = userId
            
        user = users.find_one(query)
        if user:
            print(f"User found: {username}")  # Debug logging
            return user
        print(f"User not found: {username}")  # Debug logging
        return None
        
    except Exception as e:
        print(f"Error querying user: {str(e)}")  # Debug logging
        return None

def login(database, username, userId, password):
    """Authenticate a user and return login status."""
    try:
        # Input validation
        if not all([username, password]):
            return "FAILURE: Missing required fields"
            
        # Find user by username only (ignore userId for login)
        user = __queryUser(database, username)
        
        if not user:
            return "FAILURE: User not found"
            
        # Verify password
        stored_password = cipher.decrypt(user['password'], 5, 1)
        if stored_password == password:
            print(f"Successful login for user: {username}")  # Debug logging
            return "SUCCESS: User logged in"
        
        print(f"Invalid password for user: {username}")  # Debug logging
        return "FAILURE: Incorrect password"
        
    except Exception as e:
        print(f"Error during login: {str(e)}")  # Debug logging
        return f"FAILURE: {str(e)}"

def joinProject(database, userId, projectId):
    """Add a user to a specified project."""
    try:
        users = database['users']
        # Find user by userId
        user = users.find_one({"userId": userId})
        
        if not user:
            return "FAILURE: User not found"
            
        # Check if project exists
        project = projectsDatabase.queryProject(database, projectId)
        if not project:
            return "FAILURE: Project not found"
            
        # Check if user is already in project
        if projectId in user.get('projects', []):
            return "FAILURE: User already in project"
            
        # Add project to user's projects list
        result = users.update_one(
            {"userId": userId},
            {"$addToSet": {"projects": projectId}}
        )
        
        if result.modified_count > 0:
            # Also add user to project's users list
            projectsDatabase.addUser(database, projectId, userId)
            return "SUCCESS: User added to project"
        return "FAILURE: Failed to update user projects"
        
    except Exception as e:
        print(f"Error joining project: {str(e)}")  # Debug logging
        return f"FAILURE: {str(e)}"

def getUserProjectsList(database, userId):
    """Get the list of projects a user is part of."""
    try:
        # Find the user and their projects
        user = database['users'].find_one({"userId": userId})
        if not user:
            return []

        # Get detailed project information for each project ID
        projects = []
        for project_id in user.get('projects', []):
            project = database['projects'].find_one(
                {"projectId": project_id},
                {'_id': 0}  # Exclude MongoDB _id
            )
            if project:
                projects.append({
                    'projectId': project['projectId'],
                    'projectName': project['projectName'],
                    'description': project['description'],
                    'members': project.get('members', []),
                    'creator': project.get('creator', ''),
                    'hardware': project.get('hardware', {})
                })
        
        print(f"Found {len(projects)} projects for user {userId}")  # Debug logging
        return projects
        
    except Exception as e:
        print(f"Error getting user projects: {str(e)}")  # Debug logging
        return []

def updateUserProjects(database, userId, projectId, action='add'):
    """Update user's project list (add or remove)."""
    try:
        users = database['users']
        update_operation = '$addToSet' if action == 'add' else '$pull'
        
        result = users.update_one(
            {"userId": userId},
            {update_operation: {"projects": projectId}}
        )
        
        return result.modified_count > 0
        
    except Exception as e:
        print(f"Error updating user projects: {str(e)}")  # Debug logging
        return False

def checkUserInProject(database, userId, projectId):
    """Check if a user is a member of a specific project."""
    try:
        users = database['users']
        user = users.find_one({
            "userId": userId,
            "projects": projectId
        })
        return user is not None
        
    except Exception as e:
        print(f"Error checking user in project: {str(e)}")  # Debug logging
        return False