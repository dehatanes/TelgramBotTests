from DatabaseUtils import MongoDB
import MessageModels
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
		InterativeBot.send(endpoint, params)

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
		elif(callback_type == Constants.CALLBACK_SHOW_PROP_EXAMPLE):
			"todo"
	
	def handleTextMessage(message_info):
		received_message = message_info.get("callback_query").get("message").get("text")
		if('/start' in received_message):
			InterativeBot.greetNewUser(message_info)
		else:
			# setup
			endpoint = InterativeBot.base_api + Constants.SEND_MESSAGE_ENDPOINT
			message_to_send = MessageModels.DONT_KNOW_WHAT_TO_SAY
			params   = {'chat_id': chat_id,
				   		'text': message}
			# send the message
			InterativeBot.send(endpoint, params)
		

	def greetNewUser(message_info):
		user_id    = message_info.get("message").get("from").get("id")
		user_name  = message_info.get("message").get("from").get("first_name", "pessoa")
		# setup
		endpoint = InterativeBot.base_api + Constants.SEND_MESSAGE_ENDPOINT
		message = MessageModels.INTERATIVE_BOT_GREETING_MESSAGE.format(user_name)
		keyboard = {"inline_keyboard": [[
						{ "text": "me mande um exemplo, por favor",
						  "callback_data": Constants.CALLBACK_SHOW_PROP_EXAMPLE}]]}
		params   = {'chat_id': chat_id,
				    'text': message,
				    'reply_markup': json.dumps(keyboard)}
		# send the message
		InterativeBot.send(endpoint, params)

	def show_url(chat_id, message_id, message_text):
		# get the PL url
		pl_id = eval(message_text.split('ID da PL na API de Dados Abertos: ')[-1])
		url = MongoDB.getUrlFromPL(pl_id)
		# setup
		endpoint = InterativeBot.base_api + Constants.EDIT_MESSAGE_ENDPOINT
		if(url):
			keyboard = {"inline_keyboard": [[
	                        { "text": "link para proposta na íntegra",
	                          "url":url}]]}
			params = {'chat_id': chat_id,
	                  'message_id': message_id,
	                  'text': message_text,
	                  'reply_markup': json.dumps(keyboard)}
		else:
			params = {'chat_id': chat_id,
	                  'message_id': message_id,
	                  'text': message_text + '\n\nESSA PL NÃO POSSUI LINK PARA PROPOSTA NA ÍNTEGRA'}
		# request
		InterativeBot.send(endpoint, params)

	def send(endpoint, params):
		# save to mongo
		MongoDB.insertNewSendedMessage(params, Constants.BOT1_TOKEN)
		# request
		return requests.get(endpoint, params)