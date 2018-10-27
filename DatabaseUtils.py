from Constants import Constants
from urllib.parse import urlparse
from bson.json_util import dumps
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
		MongoDB.db.test_collection.insert(user)

	def newInteractionFromUser(userId):
		MongoDB.db.test_collection.update({ 'id': userId }, {'$inc':{'interactions_count': 1}})

	def getAllData():
		print("GETTING ALL THE DATA")
		return dumps(MongoDB.db.test_collection.find())