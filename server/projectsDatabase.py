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

# Function to create a new project
def createProject(database, projectName, projectId, description):
    # Create a new project in the database
    pass

# Function to add a user to a project
def addUser(database, projectId, userId):
    # Add a user to the specified project
    pass

# Function to update hardware usage in a project
def updateUsage(database, projectId, hwSetName):
    # Update the usage of a hardware set in the specified project
    pass

# Function to check out hardware for a project
def checkOutHW(database, projectId, hwSetName, qty, userId):
    # Check out hardware for the specified project and update availability
    pass

# Function to check in hardware for a project
def checkInHW(database, projectId, hwSetName, qty, userId):
    # Check in hardware for the specified project and update availability
    pass

