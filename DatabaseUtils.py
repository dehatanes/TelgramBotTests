from Constants import Constants
import pymongo

class MongoDB:
	# Connect with the database using pymongo
	conn = pymongo.Connection(Constants.MONGO_URL)
    # Get the database
    db = conn[urlparse(Constants.MONGO_URL).path[1:]]

    def insertNewUser(user_infos):
    	user = {}
    	user["first_name"] = user_infos.get("first_name")
    	user["last_name"] = user_infos.get("last_name")
    	user["username"] = user_infos.get("username")
    	user["id"] = user_infos.get("id")
    	user["interactions_count"] = 1
    	db.test_collection.insert(user)

    def getAllData():
		print db.test_collection.find()