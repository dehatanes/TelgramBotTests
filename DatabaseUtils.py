from Constants import Constants
import pymongo

class MongoDB:
	# Connect with the database using pymongo
	conn = pymongo.MongoClient(Constants.MONGODB_URI)
	# Get the database
	db = conn[urlparse(Constants.MONGODB_URI).path[1:]]

	def insertNewUser(user_infos):
		print("NEW USER INSERTED")
		user = {}
		user["first_name"] = user_infos.get("first_name")
		user["last_name"] = user_infos.get("last_name")
		user["username"] = user_infos.get("username")
		user["id"] = user_infos.get("id")
		user["interactions_count"] = 1
		db.test_collection.insert(user)

	def getAllData():
		print("GETTING ALL THE DATA")
		return db.test_collection.find()