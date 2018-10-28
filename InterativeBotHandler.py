from DatabaseUtils import MongoDB
import Constants
import requests
import json

class InterativeBot:
	base_api = Constants.BOT1_BASE_API

	def sendMessageToMultipleUsers(users_list, message):
		for user_id in users_list:
			InterativeBot.sendMessageToOneUser(user_id, message)

	def sendMessageToOneUser(chat_id, message):
		# setup
		endpoint = InterativeBot.base_api + Constants.SEND_MESSAGE_ENDPOINT
		keyboard = {"inline_keyboard": [[
						{ "text": "quero ver a proposta",
						  "callback_data": Constants.CALLBACK_SHOW_PROPOSITION}]]}
		params   = {'chat_id': chat_id,
				    'text': message,
				    'reply_markup': json.dumps(keyboard)}
		# send the message
		requests.get(endpoint, params)

	def handleCallbackData(message_info):
		# TODO
		pass
