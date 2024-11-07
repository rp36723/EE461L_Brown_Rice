from pymongo import MongoClient
from pprint import pprint

def test_hardware_sets():
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['hardware_checkout']
    
    # Query all hardware sets
    hardware_sets = list(db.hardwareSets.find({}, {'_id': 0}))  # Exclude MongoDB _id
    
    print("Hardware Sets Found:", len(hardware_sets))
    print("\nDetailed Information:")
    for hw_set in hardware_sets:
        pprint(hw_set)
        print()

if __name__ == "__main__":
    test_hardware_sets()