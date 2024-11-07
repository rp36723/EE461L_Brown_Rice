from pymongo import MongoClient
from dotenv import load_dotenv
import os

def test_connection():
    try:
        load_dotenv()
        uri = os.getenv("MONGODB_URI")
        print("Attempting to connect to MongoDB Atlas...")
        client = MongoClient(uri)
        
        # Test connection
        client.admin.command('ping')
        print("Successfully connected to MongoDB Atlas!")
        
        # Get database
        db = client['hardware_checkout']
        print(f"\nConnected to database: {db.name}")
        
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    test_connection()