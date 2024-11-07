from pymongo import MongoClient

def test_mongodb():
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['hardware_checkout']
        
        # Create a test user
        test_user = {
            'username': 'test',
            'userId': 'test',
            'password': 'test123',
            'projects': []
        }
        
        # Clear existing users and insert test user
        db.users.delete_many({})
        db.users.insert_one(test_user)
        
        # Verify user was inserted
        user = db.users.find_one({'username': 'test'})
        if user:
            print("Test user created successfully!")
            print("Username: test")
            print("Password: test123")
        
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_mongodb()