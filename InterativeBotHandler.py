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
		keyboard = {"inline_keyboard": [
						[{ "text": "quero ver a proposta",
						   "callback_data": Constants.CALLBACK_SHOW_PROPOSITION}],
						[{ "text": "autores",
						   "callback_data": Constants.CALLBACK_SHOW_AUTHORS},
						 { "text": "palavras-chave",
						   "callback_data": Constants.CALLBACK_SHOW_KEY_WORDS}],
						[{ "text": "histórico",
						   "callback_data": Constants.CALLBACK_SHOW_HISTORY},
						   { "text": "despacho",
						   "callback_data": Constants.CALLBACK_DESPACHO}]]}
		params   = {'chat_id': chat_id,
				    'text': message,
				    'reply_markup': json.dumps(keyboard)}
		# send the message
		InterativeBot.send(endpoint, params)

	def handleCallback(message_info):
		# understand the content
		callback_id     = message_info.get("callback_query").get("id")
		callback_type   = message_info.get("callback_query").get("data")
		message_text	= message_info.get("callback_query").get("message").get("text")
		message_id      = message_info.get("callback_query").get("message").get("message_id")
		chat_id         = message_info.get("callback_query").get("message").get("chat").get("id")
		# answer the callback to hide the loading in the button
		requests.get(InterativeBot.base_api + Constants.ANSWER_CALLBACK_ENDPOINT, {'callback_query_id':callback_id})
		# properly handle the callback
		if(callback_type == Constants.CALLBACK_SHOW_PROPOSITION):
			InterativeBot.show_url(chat_id, message_id, message_text)
		elif(callback_type == Constants.CALLBACK_SHOW_AUTHORS):
			InterativeBot.send_project_authors(chat_id, message_id, message_text)
		elif(callback_type == Constants.CALLBACK_SHOW_KEY_WORDS):
			InterativeBot.send_keywords(chat_id, message_id, message_text)
		elif(callback_type == Constants.CALLBACK_SHOW_HISTORY):
			InterativeBot.send_project_history(chat_id, message_id, message_text)
		elif(callback_type == Constants.CALLBACK_DESPACHO):
			InterativeBot.send_despacho(chat_id, message_id, message_text)
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
			InterativeBot.sendProjectMessageToOneUser(chat_id, message)
	
	def handleTextMessage(message_info):
		received_message = message_info.get("message").get("text")
		if('/start' in received_message):
			InterativeBot.greetNewUser(message_info)
		else:
			# setup
			endpoint = InterativeBot.base_api + Constants.SEND_MESSAGE_ENDPOINT
			message_to_send = MessageModels.DONT_KNOW_WHAT_TO_SAY
			params   = {'chat_id': message_info.get("message").get("from").get("id"),
				   		'text': message_to_send}
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
		params   = {'chat_id': user_id,
				    'text': message,
				    'reply_markup': json.dumps(keyboard)}
		# send the message
		InterativeBot.send(endpoint, params)

	# ------------------------
	# HANDLE CALLBACK METHODS
	# ------------------------
	def show_url(chat_id, message_id, message_text):
		# get the PL url
		pl_id = InterativeBot.getProjectIdFromMessage(message_text)
		url = MongoDB.getUrlFromPL(pl_id)
		# setup
		endpoint = InterativeBot.base_api + Constants.EDIT_MESSAGE_ENDPOINT
		if(url):
			url = "https://docs.google.com/viewer?url=" + url # para abrir o pdf no drive e a pessoa nao precisar baixar
			keyboard = {"inline_keyboard": [
						[{ "text": "CLIQUE: link para proposta na íntegra",
							"url":url}],
						[{ "text": "autores",
						   "callback_data": Constants.CALLBACK_SHOW_AUTHORS},
						 { "text": "palavras-chave",
						   "callback_data": Constants.CALLBACK_SHOW_KEY_WORDS}],
						[{ "text": "histórico",
						   "callback_data": Constants.CALLBACK_SHOW_HISTORY},
						   { "text": "despacho",
						   "callback_data": Constants.CALLBACK_DESPACHO}]]}
			params = {'chat_id': chat_id,
	                  'message_id': message_id,
	                  'text': message_text,
	                  'reply_markup': json.dumps(keyboard)}
		else:
			keyboard = {"inline_keyboard": [
						[{ "text": "autores",
						   "callback_data": Constants.CALLBACK_SHOW_AUTHORS},
						 { "text": "palavras-chave",
						   "callback_data": Constants.CALLBACK_SHOW_KEY_WORDS}],
						[{ "text": "histórico",
						   "callback_data": Constants.CALLBACK_SHOW_HISTORY},
						   { "text": "despacho",
						   "callback_data": Constants.CALLBACK_DESPACHO}]]}
			params = {'chat_id': chat_id,
	                  'message_id': message_id,
	                  'text': 'ESSA PL NÃO POSSUI LINK PARA PROPOSTA NA ÍNTEGRA \n\n' + message_text,
	                  'reply_markup': json.dumps(keyboard)}
		# request
		InterativeBot.send(endpoint, params)

	def send_project_authors(chat_id, message_id, message_text):
		# setup
		endpoint = InterativeBot.base_api + Constants.SEND_MESSAGE_ENDPOINT
		params   = {'chat_id': chat_id,
				    'text': "AUTORES DO PROJETO AQUI",
				    'reply_to_message_id': message_id}
		# send the message
		InterativeBot.send(endpoint, params)

	def send_keywords(chat_id, message_id, message_text):
		# get the PL url
		pl_id = InterativeBot.getProjectIdFromMessage(message_text)
		keywords = MongoDB.getKeywordsFromPL(pl_id)
		# building the message
		if(keywords and keywords.get('keywords')):
			message = MessageModels.PL_KEYWORDS_MESSAGE.format( keywords.get('numero'),
																keywords.get('ano'),
																keywords.get('keywords'))
		else:
			message = MessageModels.PL_KEYWORDS_ERROR_MESSAGE
		# setup
		endpoint = InterativeBot.base_api + Constants.SEND_MESSAGE_ENDPOINT
		params   = {'chat_id': chat_id,
				    'text': message,
				    'reply_to_message_id': message_id}
		# send the message
		InterativeBot.send(endpoint, params)

	def send_project_history(chat_id, message_id, message_text):
		# setup
		endpoint = InterativeBot.base_api + Constants.SEND_MESSAGE_ENDPOINT
		params   = {'chat_id': chat_id,
				    'text': "HISTORICO DO PROJETO AQUI",
				    'reply_to_message_id': message_id}
		# send the message
		InterativeBot.send(endpoint, params)

	def send_despacho(chat_id, message_id, message_text):
		# get the PL url
		pl_id = InterativeBot.getProjectIdFromMessage(message_text)
		keywords = MongoDB.getDespachoFromPL(pl_id)
		# building the message
		if(keywords and keywords.get('statusProposicao').get('despacho')):
			message = MessageModels.PL_DESPACHO_MESSAGE.format( keywords.get('numero'),
																keywords.get('ano'),
																keywords.get('statusProposicao').get('despacho'))
		else:
			message = MessageModels.PL_DESPACHO_ERROR_MESSAGE
		# setup
		endpoint = InterativeBot.base_api + Constants.SEND_MESSAGE_ENDPOINT
		params   = {'chat_id': chat_id,
				    'text': message,
				    'reply_to_message_id': message_id}
		# send the message
		InterativeBot.send(endpoint, params)

	# -------------
	# AUXILIARES
	# -------------
	def getProjectIdFromMessage(message):
		return eval(message.split('ID da PL na API de Dados Abertos: ')[-1])

	def send(endpoint, params):
		# save to mongo
		MongoDB.insertNewSendedMessage(params, Constants.BOT1_TOKEN)
		# request
		return requests.get(endpoint, params)
