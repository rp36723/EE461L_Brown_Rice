# Import necessary libraries and modules
from pymongo import MongoClient

'''
Structure of Hardware Set entry:
HardwareSet = {
    'hwName': hwSetName,
    'capacity': initCapacity,
    'availability': initCapacity
}
'''

# Function to create a new hardware set
def createHardwareSet(database, hwSetName, initCapacity):
    # Create a new hardware set in the database
    hwSet = {
        'hwName': hwSetName,
        'capacity': initCapacity,
        'availability': initCapacity
    }
    database["hardwareSets"].insert_one(hwSet)
    return "SUCCESS: Hardware set added"

# Function to query a hardware set by its name
def queryHardwareSet(database, hwSetName):
    # Query and return a hardware set from the database
    return database["hardwareSets"].find_one({"hwName": hwSetName})

# Function to update the availability of a hardware set
def updateAvailability(database, hwSetName, newAvailability):
    # Update the availability of an existing hardware set
    #TODO: function
    pass

# Function to request space from a hardware set
def requestSpace(database, hwSetName, amount):
    # Request a certain amount of hardware and update availability
    #TODO: function
    pass

# Function to get all hardware set names
def getAllHwNames(database):
    # Get and return a list of all hardware set names
    hardware_sets = database["hardwareSets"].find({}, {"hwName": 1, "_id": 0})
    hardwareSetNames = [hardware_set["hwName"] for hardware_set in hardware_sets]
    return hardwareSetNames

