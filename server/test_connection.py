from pymongo import MongoClient

def test_connection():
    try:
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        
        # Test connection
        client.server_info()
        print("Successfully connected to MongoDB!")
        
        # Get database and collection
        db = client['hardware_checkout']
        hardware_sets = db.hardwareSets
        
        # Count documents
        count = hardware_sets.count_documents({})
        print(f"Number of hardware sets: {count}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_connection()