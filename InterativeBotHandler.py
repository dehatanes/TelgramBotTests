from DatabaseUtils import MongoDB
import Constants
import requests
import json

class InterativeBot:
	base_api = Constants.BOT1_BASE_API

	def sendMessageToMultipleUsers(users_list, message):
		for user_id in users_list:
			InterativeBot.sendProjectMessageToOneUser(user_id, message)

	def sendProjectMessageToOneUser(chat_id, message):
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

	def handleCallback(message_info):
		# understand the content
		callback_id     = message_info.get("callback_query").get("id")
		callback_type   = message_info.get("callback_query").get("data")
		message_content = message_info.get("callback_query").get("message").get("text")
		message_id      = message_info.get("callback_query").get("message").get("message_id")
		chat_id         = message_info.get("callback_query").get("message").get("chat").get("id")
		# answer the callback to hide the loading in the button
		requests.get(InterativeBot.base_api + Constants.ANSWER_CALLBACK_ENDPOINT, {'callback_query_id':callback_id})
		# properly handle the callback
		if(callback_type == Constants.CALLBACK_SHOW_PROPOSITION):
			InterativeBot.show_url(chat_id, message_id, message_content)
		# TODO -> ADD IN MONGO_DB
	
	def handleTextMessage(message_info):
		# TODO
		pass

	def greetNewUser(message_info):
		# TODO
		pass

	def show_url(self, chat_id, message_id, message_text):
        # setup
        endpoint = InterativeBot.base_api + Constants.EDIT_MESSAGE_ENDPOINT
        keyboard = {"inline_keyboard": [[
                        { "text": "google.com",
                          "url":"https://www.google.com.br/" }]]}
        params = {'chat_id': chat_id,
                  'message_id': message_id,
                  'text': message_text,
                  'reply_markup': json.dumps(keyboard)}
        # request
        requests.get(endpoint, params)