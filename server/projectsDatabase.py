# Import necessary libraries and modules
from pymongo import MongoClient

import hardwareDatabase

'''
Structure of Project entry:
Project = {
    'projectName': projectName,
    'projectId': projectId,
    'description': description,
    'hwSets': {HW1: 0, HW2: 10, ...},
    'users': [user1, user2, ...]
}
'''

# Function to query a project by its ID
def queryProject(database, projectId):
    # Query and return a project from the database
    projects = database["projects"]
    try:
        return projects.find_one({"projectID": projectId})
    except Exception as e:
        print("Project Query FAILURE: " + str(e))
        return None

# Function to add a user to a project
def addUser(database, projectId, userId):
    # Add a user to the specified project
    pass

# Function to update hardware usage in a project
def updateUsage(database, projectId, hwSetName):
    # Update the usage of a hardware set in the specified project
    pass


def createProject(database, project_name, project_id, description, creator_id):
    """Create a new project."""
    try:
        # Check if project ID already exists
        if database.projects.find_one({"projectId": project_id}):
            return "FAILURE: Project ID already exists"

        project = {
            'projectName': project_name,
            'projectId': project_id,
            'description': description,
            'creator': creator_id,
            'members': [creator_id],  # Creator is automatically a member
            'hardware': {
                'HWSet1': 0,
                'HWSet2': 0
            }
        }
        
        # Insert project
        result = database.projects.insert_one(project)
        
        if result.inserted_id:
            # Add project to creator's project list
            update_result = database.users.update_one(
                {"userId": creator_id},
                {"$addToSet": {"projects": project_id}}
            )
            
            if update_result.modified_count > 0:
                print(f"Project {project_id} created and added to user {creator_id}")
                return "SUCCESS: Project created"
            else:
                print(f"Project created but failed to update user {creator_id}")
                return "FAILURE: Failed to update user projects"
            
        return "FAILURE: Database error"
        
    except Exception as e:
        print(f"Error creating project: {str(e)}")
        return f"FAILURE: {str(e)}"

def joinProject(database, project_id, user_id):
    """Add a user to an existing project."""
    try:
        # Check if project exists
        project = database.projects.find_one({"projectId": project_id})
        if not project:
            return "FAILURE: Project not found"

        # Check if user is already a member
        if user_id in project['members']:
            return "FAILURE: User is already a member of this project"

        # Add user to project members
        result = database.projects.update_one(
            {"projectId": project_id},
            {"$addToSet": {"members": user_id}}
        )

        if result.modified_count > 0:
            # Add project to user's project list
            database.users.update_one(
                {"userId": user_id},
                {"$addToSet": {"projects": project_id}}
            )
            return "SUCCESS: Joined project"
        return "FAILURE: Failed to join project"

    except Exception as e:
        return f"FAILURE: {str(e)}"

def checkOutHW(database, project_id, hw_set_name, quantity, user_id):
    """Check out hardware for a project."""
    try:
        # Verify user is a member of the project
        project = database.projects.find_one({
            "projectId": project_id,
            "members": user_id
        })
        
        if not project:
            return "FAILURE: User is not authorized for this project"

        # Get hardware set
        hw_set = database.hardwareSets.find_one({"hwName": hw_set_name})
        if not hw_set:
            return "FAILURE: Hardware set not found"

        # Check availability
        if hw_set['availability'] < quantity:
            return "FAILURE: Not enough units available"

        # Update hardware set availability
        new_availability = hw_set['availability'] - quantity
        result = database.hardwareSets.update_one(
            {"hwName": hw_set_name},
            {"$set": {"availability": new_availability}}
        )

        if result.modified_count > 0:
            # Update project's checked out hardware
            current_checkout = project['hardware'].get(hw_set_name, 0)
            database.projects.update_one(
                {"projectId": project_id},
                {"$set": {f"hardware.{hw_set_name}": current_checkout + quantity}}
            )
            return "SUCCESS: Hardware checked out"
        return "FAILURE: Failed to update hardware"

    except Exception as e:
        return f"FAILURE: {str(e)}"

def checkInHW(database, project_id, hw_set_name, quantity, user_id):
    """Check in hardware for a project."""
    try:
        # Verify user is a member of the project
        project = database.projects.find_one({
            "projectId": project_id,
            "members": user_id
        })
        
        if not project:
            return "FAILURE: User is not authorized for this project"

        # Verify project has enough units checked out
        current_checkout = project['hardware'].get(hw_set_name, 0)
        if current_checkout < quantity:
            return "FAILURE: Project doesn't have that many units checked out"

        # Update hardware set availability
        result = database.hardwareSets.update_one(
            {"hwName": hw_set_name},
            {"$inc": {"availability": quantity}}
        )

        if result.modified_count > 0:
            # Update project's checked out hardware
            database.projects.update_one(
                {"projectId": project_id},
                {"$set": {f"hardware.{hw_set_name}": current_checkout - quantity}}
            )
            return "SUCCESS: Hardware checked in"
        return "FAILURE: Failed to update hardware"

    except Exception as e:
        return f"FAILURE: {str(e)}"

def getProjectInfo(database, project_id):
    """Get detailed project information."""
    try:
        project = database.projects.find_one({"projectId": project_id}, {'_id': 0})
        if project:
            return project
        return None
    except Exception as e:
        print(f"Error getting project info: {str(e)}")
        return None