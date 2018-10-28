from bottle import Bottle, response, request as bottle_request
from ApiDadosAbertosSrcScripts import ApiDadosAbertos
from InterativeBotHandler import InterativeBot
from SimpleBotHandler import SimpleBot
from DatabaseUtils import MongoDB
import requests, json
import MessageModels
import Constants

class AppHandler(Bottle):
	#----------------
	# API ENDPOINTS
	#----------------
	ROOT_ENDPOINT                  = "/"
	RECEIVED_MESSAGE_FROM_CHATBOT1 = "/received-message-chatbot1"
	RECEIVED_MESSAGE_FROM_CHATBOT2 = "/received-message-chatbot2"

	# START APP
	def __init__(self):
		# Setup
		super(AppHandler, self).__init__()
		# Set bot webhooks
		requests.get((Constants.BOT1_BASE_API + Constants.SET_WEBHOOK_ENDPOINT), {'url': (Constants.HEROKU_URL + AppHandler.RECEIVED_MESSAGE_FROM_CHATBOT1)})
		requests.get((Constants.BOT2_BASE_API + Constants.SET_WEBHOOK_ENDPOINT), {'url': (Constants.HEROKU_URL + AppHandler.RECEIVED_MESSAGE_FROM_CHATBOT2)})
		# Config endpoints
		self.route(self.ROOT_ENDPOINT, callback=self.scheduled_script, method="GET")
		self.route(self.RECEIVED_MESSAGE_FROM_CHATBOT1, callback=self.handle_chatbot1_updates, method="POST")
		self.route(self.RECEIVED_MESSAGE_FROM_CHATBOT2, callback=self.handle_chatbot2_updates, method="POST")

	# METHODS
	def scheduled_script(self):
		# TODO() -> check if needs to send the message
		# ------------------------------------------------
		# get a new PL from the Dados Abertos API and turn it to a message
		newPL = ApiDadosAbertos.showMeSomeNews() # <- Already saves the PL in our database
		message = MessageModels.NEW_PL_MESSAGE_MODEL.format(newPL.get('numero'),
															newPL.get('ano'),
															newPL.get('ementa'),
															newPL.get('statusProposicao').get('despacho'),
															newPL.get('statusProposicao').get('descricaoTramitacao'),
															newPL.get('statusProposicao').get('descricaoSituacao'),
															newPL.get('justificativa'),
															newPL.get('statusProposicao').get('dataHora'),
															newPL.get('id'))
		# get all users from Mongo
		users = MongoDB.getAlluserIds()
		# send message
		InterativeBot.sendMessageToMultipleUsers(users.get(Constants.BOT1_TOKEN), message)
		#SimpleBot.sendMessageToMultipleUsers(users.get(Constants.BOT2_TOKEN))
		# save in Mongo the sended message (and users involved)
		data = {'message':message, 'sended_to':users}
		MongoDB.insertNewSendedMessage(data)
		# response
		print(data)
		#response.headers['Content-Type'] = 'application/json'
		#return json.dumps(data)

	def handle_chatbot1_updates(self):
		# verify type of message
		# if text message
			# if /start message
				# save user in DB
				# InterativeBotHandler.greetNewUser
			# else
				# check if user inDB
					# false -> add user in DB
				# InterativeBotHandler.handleTextMessage
			# save message in database
		# if callback
			# InterativeBotHandler.handleCallback
			# save in database
		print('handle_chatbot1_updates')

	def handle_chatbot2_updates(self):
		# verify type of message
		# if text message
			# if /start message
				# save user in DB
				# InterativeBotHandler.greetNewUser
			# else
				# check if user inDB
					# false -> add user in DB
				# InterativeBotHandler.handleTextMessage
			# save message in database
		# if callback
			# InterativeBotHandler.handleCallback
			# save in database
		print('handle_chatbot2_updates')