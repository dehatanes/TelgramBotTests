from urllib.parse import urlparse
from bson.json_util import dumps
from datetime import datetime
import Constants
import pymongo

class MongoDB:
	#--------
	# SETUP
	#--------
	# Connect with MongoDB using pymongo
	conn = pymongo.MongoClient(Constants.MONGODB_URI)
	# Get the database
	db = conn[urlparse(Constants.MONGODB_URI).path[1:]]

	#----------------
	# COLLECTIONS
	#----------------
	USERS_COLLECTION         = 'subscribed_users'
	SCHEDULER_COLLECTION     = 'schedule_control'
	SENDED_MSGS_COLLECTION   = 'sended_messages'
	RECEIVED_MSGS_COLLECTION = 'received_messages'
	USED_PLS_COLLECTION      = 'used_pls_collection'

	#---------------------------
	# USERS_COLLECTION METHODS
	#---------------------------
	def checkIfUserExistsInBot(user_id, bot_token):
		search_query  = {'user_id':user_id, 'interacting_with_bot':bot_token}
		search_result = MongoDB.db[MongoDB.USERS_COLLECTION].find_one(search_query)
		if(dumps(search_result) == 'null'):
			return False
		return True

	def insertNewUser(user_infos, bot_token):
		print("INSERTING NEW USER")
		user = {}
		user["user_id"]              = user_infos.get("id")
		user["username"]             = user_infos.get("username")
		user["last_name"]            = user_infos.get("last_name")
		user["first_name"]           = user_infos.get("first_name")
		user['created_time']         = datetime.now()
		user["interacting_with_bot"] = bot_token
		MongoDB.db[MongoDB.USERS_COLLECTION].insert_one(user)

	def getAlluserIds():
		print("GETTING ALL THE USERS")
		users_list = eval(dumps(MongoDB.db[MongoDB.USERS_COLLECTION].find()))
		response = dict()
		for user in users_list:
			user_bot_token = user.get('interacting_with_bot')
			if(not response.get(user_bot_token)):
				response[user_bot_token] = set()
			response[user_bot_token].add(user.get("user_id"))
		response[Constants.BOT1_TOKEN] = list(response.get(Constants.BOT1_TOKEN,()))
		response[Constants.BOT2_TOKEN] = list(response.get(Constants.BOT2_TOKEN,()))
		return response

	#-----------------------------
	# USED_PLS_COLLECTION METHODS
	#-----------------------------
	def insertNewUsedPL(pl_infos):
		print("INSERTING NEW PL")
		if(not pl_infos.get('id')):
			return 'fail'
		pl_infos['pl_id']        = pl_infos.get('id')
		pl_infos['created_time'] = datetime.now()
		MongoDB.db[MongoDB.USED_PLS_COLLECTION].insert_one(pl_infos)
		return 'success'

	def verifyIfUsedPL(pl_id):
		search_query  = {'pl_id':pl_id}
		search_result = MongoDB.db[MongoDB.USED_PLS_COLLECTION].find_one(search_query)
		if(dumps(search_result) == 'null'):
			return False
		return True

	def returnUsedPL(pl_id):
		search_query  = {'pl_id':pl_id}
		search_result = MongoDB.db[MongoDB.USED_PLS_COLLECTION].find_one(search_query)
		return dumps(search_result)

	#---------------------------------
	# SENDED_MSGS_COLLECTION METHODS
	#---------------------------------
	def insertNewSendedMessage(data_to_be_inserted):
		MongoDB.db[MongoDB.SENDED_MSGS_COLLECTION].insert_one(data_to_be_inserted)

	#---------------------------------
	# RECEIVED_MSGS_COLLECTION METHODS
	#---------------------------------
	def saveReceivedCallback(raw_message):
		#MongoDB.db[MongoDB.RECEIVED_MSGS_COLLECTION].insert_one(raw_message)
		pass

	def saveReceivedMessage(raw_message):
		#MongoDB.db[MongoDB.RECEIVED_MSGS_COLLECTION].insert_one(raw_message)
		pass