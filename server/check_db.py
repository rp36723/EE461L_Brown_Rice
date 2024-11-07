from pymongo import MongoClient
from dotenv import load_dotenv
import os

def verify_database():
    try:
        load_dotenv()
        uri = os.getenv("MONGODB_URI")
        client = MongoClient(uri)
        db = client['hardware_checkout']
        
        print("Database Contents:\n")
        
        print("1. Hardware Sets:")
        for hw in db.hardwareSets.find():
            print(f"  - {hw['hwName']}:")
            print(f"    Capacity: {hw['capacity']}")
            print(f"    Available: {hw['availability']}")
        
        print("\n2. Users:")
        for user in db.users.find():
            print(f"  - Username: {user['username']}")
            print(f"    Projects: {user['projects']}")
        
        print("\n3. Projects:")
        for project in db.projects.find():
            print(f"  - Name: {project['projectName']}")
            print(f"    ID: {project['projectId']}")
            print(f"    Members: {project['members']}")
            print(f"    Hardware: {project['hardware']}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    verify_database()