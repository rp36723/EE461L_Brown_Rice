from pymongo import MongoClient
from dotenv import load_dotenv
import os
import cipher

def init_atlas_database():
    try:
        load_dotenv()
        uri = os.getenv("MONGODB_URI")
        client = MongoClient(uri)
        db = client['hardware_checkout']
        
        print("Connected to MongoDB Atlas")
        
        # Clear existing collections
        print("\nClearing existing collections...")
        db.users.drop()
        db.projects.drop()
        db.hardwareSets.drop()
        
        # Initialize Hardware Sets
        print("\nInitializing hardware sets...")
        hardware_sets = [
            {
                "hwName": "HWSet1",
                "capacity": 100,
                "availability": 100,
                "description": "Hardware Set 1"
            },
            {
                "hwName": "HWSet2",
                "capacity": 100,
                "availability": 100,
                "description": "Hardware Set 2"
            }
        ]
        result = db.hardwareSets.insert_many(hardware_sets)
        print(f"Created {len(result.inserted_ids)} hardware sets")
        
        # Initialize Test User
        print("\nCreating test user...")
        test_user = {
            'username': 'test',
            'userId': 'test',
            'password': cipher.encrypt('test123', 5, 1),
            'projects': []
        }
        result = db.users.insert_one(test_user)
        print("Test user created")
        
        # Initialize Sample Project
        print("\nCreating sample project...")
        sample_project = {
            'projectName': 'Sample Project',
            'projectId': 'sample-project',
            'description': 'A sample project for testing',
            'creator': 'test',
            'members': ['test'],
            'hardware': {
                'HWSet1': 0,
                'HWSet2': 0
            }
        }
        result = db.projects.insert_one(sample_project)
        print("Sample project created")
        
        # Add project to test user's projects
        db.users.update_one(
            {"userId": "test"},
            {"$push": {"projects": "sample-project"}}
        )
        
        print("\nDatabase initialization complete!")
        print("\nTest Credentials:")
        print("Username: test")
        print("Password: test123")
        
        # Verify setup
        print("\nVerifying setup:")
        print(f"Hardware Sets: {db.hardwareSets.count_documents({})} documents")
        print(f"Users: {db.users.count_documents({})} documents")
        print(f"Projects: {db.projects.count_documents({})} documents")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    init_atlas_database()