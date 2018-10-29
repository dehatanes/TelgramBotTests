from DatabaseUtils import MongoDB
import MessageModels
import Constants
import requests
import json

class SimpleBot:
	base_api = Constants.BOT2_BASE_API

	def sendMessageToMultipleUsers(users_list, message):
		for user_id in users_list:
			SimpleBot.sendProjectMessageToOneUser(user_id, message)

	def sendProjectMessageToOneUser(chat_id, message):
		# setup
		endpoint = SimpleBot.base_api + Constants.SEND_MESSAGE_ENDPOINT
		keyboard = {"inline_keyboard": [[
						{ "text": "quero ver a proposta",
						  "callback_data": Constants.CALLBACK_SHOW_PROPOSITION}]]}
		params   = {'chat_id': chat_id,
				    'text': message,
				    'reply_markup': json.dumps(keyboard)}
		# send the message
		SimpleBot.send(endpoint, params)

	def handleCallback(message_info):
		# understand the content
		callback_id     = message_info.get("callback_query").get("id")
		callback_type   = message_info.get("callback_query").get("data")
		message_content = message_info.get("callback_query").get("message").get("text")
		message_id      = message_info.get("callback_query").get("message").get("message_id")
		chat_id         = message_info.get("callback_query").get("message").get("chat").get("id")
		# answer the callback to hide the loading in the button
		requests.get(SimpleBot.base_api + Constants.ANSWER_CALLBACK_ENDPOINT, {'callback_query_id':callback_id})
		# properly handle the callback
		if(callback_type == Constants.CALLBACK_SHOW_PROPOSITION):
			SimpleBot.show_url(chat_id, message_id, message_content)
		elif(callback_type == Constants.CALLBACK_SHOW_PROP_EXAMPLE):
			newPL = MongoDB.returnUsedPL()
			message = MessageModels.NEW_PL_MESSAGE_MODEL.format(newPL.get('numero'),
																newPL.get('ano'),
																newPL.get('ementa'),
																newPL.get('statusProposicao').get('despacho'),
																newPL.get('statusProposicao').get('descricaoTramitacao'),
																newPL.get('statusProposicao').get('descricaoSituacao'),
																newPL.get('justificativa'),
																newPL.get('statusProposicao').get('dataHora'),
																newPL.get('id'))
			SimpleBot.sendProjectMessageToOneUser(chat_id, message)
	
	def handleTextMessage(message_info):
		received_message = message_info.get("message").get("text")
		if('/start' in received_message):
			SimpleBot.greetNewUser(message_info)
		else:
			# setup
			endpoint = SimpleBot.base_api + Constants.SEND_MESSAGE_ENDPOINT
			message_to_send = MessageModels.DONT_KNOW_WHAT_TO_SAY
			params   = {'chat_id': message_info.get("message").get("from").get("id"),
				   		'text': message_to_send}
			# send the message
			SimpleBot.send(endpoint, params)

	def greetNewUser(message_info):
		user_id    = message_info.get("message").get("from").get("id")
		user_name  = message_info.get("message").get("from").get("first_name", "pessoa")
		# setup
		endpoint = SimpleBot.base_api + Constants.SEND_MESSAGE_ENDPOINT
		message = MessageModels.SIMPLE_BOT_GREETING_MESSAGE.format(user_name)
		keyboard = {"inline_keyboard": [[
						{ "text": "me mande um exemplo, por favor",
						  "callback_data": Constants.CALLBACK_SHOW_PROP_EXAMPLE}]]}
		params   = {'chat_id': user_id,
				    'text': message,
				    'reply_markup': json.dumps(keyboard)}
		# send the message
		SimpleBot.send(endpoint, params)

	def show_url(chat_id, message_id, message_text):
		# get the PL url
		pl_id = eval(message_text.split('ID da PL na API de Dados Abertos: ')[-1])
		url = MongoDB.getUrlFromPL(pl_id)
		# setup
		endpoint = SimpleBot.base_api + Constants.EDIT_MESSAGE_ENDPOINT
		if(url):
			keyboard = {"inline_keyboard": [[
	                        { "text": "CLIQUE: link para proposta na íntegra",
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
		SimpleBot.send(endpoint, params)

	def send(endpoint, params):
		# save to mongo
		MongoDB.insertNewSendedMessage(params, Constants.BOT2_TOKEN)
		# request
		return requests.get(endpoint, params)