import sys, getopt, os
import requests
import json
from bottle import Bottle, response, request as bottle_request
from UserModel import User
from DatabaseUtils import MongoDB

class BotHandler(Bottle):
    #----------------
    # API ENDPOINTS
    #----------------
    ROOT_ENDPOINT                  = "/"
    RECEIVED_MESSAGE_FROM_CHATBOT1 = "/received-message-chatbot1"
    GET_DATABASE_ENDPOINT          = "/get-database"

    
    # Database simulation
    users_list = {}

    # METHODS
    def __init__(self, token):
        # Setup
        super(BotHandler, self).__init__()
        self.token = token
        self.api_base_url = self.api_base_url.format(token)
        # Handle conversation
        self.route(self.ROOT_ENDPOINT, callback=self.send_message_to_all_users, method="POST")
        self.route(self.GET_DATABASE_ENDPOINT, callback=self.return_database, method="GET")
        self.route(self.RECEIVED_MESSAGE_FROM_CHATBOT1, callback=self.handle_updates, method="POST")

    def send_message_to_all_users(self):
        users = MongoDB.getAlluserIds()
        for userid in users:
            print("messaging user {0}".format(userid))
            self.send_message_to_specific_person(userid,"messaging everybody. I AM ALIVE!")
        response.headers['Content-Type'] = 'application/json'
        return {"Status":"Ok", "users_messaged": list(users)}

    def return_database(self):
        resp = MongoDB.getAllData()
        response.headers['Content-Type'] = 'application/json'
        return json.dumps(resp)

    def send_message_to_specific_person(self, chat_id, text):
        # setup
        method = self.send_message_endpoint
        keyboard = {"inline_keyboard": [[
                        { "text": "botão A",
                          "callback_data": "button-A-pressed"}, 
                        { "text": "show url",
                          "callback_data": "google-pressed"}]]}

        params = {'chat_id': chat_id,
                  'text': text,
                  'reply_markup': json.dumps(keyboard)}
        # request
        resp = requests.get(self.api_base_url + method, params).json()
        if(resp.get("ok")):
            return resp

    def show_url(self, chat_id, message_id):
        # setup
        method = "editMessageText"
        keyboard = {"inline_keyboard": [[
                        { "text": "botão A",
                          "callback_data": "button-A-pressed"}, 
                        { "text": "google.com",
                          "url":"https://www.google.com.br/" }]]}

        params = {'chat_id': chat_id,
                  'message_id': message_id,
                  'text': "Vou te mostrar a url. clique no link",
                  'reply_markup': json.dumps(keyboard)}
        # request
        resp = requests.get(self.api_base_url + method, params).json()
        if(resp.get("ok")):
            return resp

    def start_the_chat(self, user):
        # greet
        greeting_text = "Ola, {0}!\nPrazer te conhecer.\n\nSou um bot bem interessante, me mande uma mensagem que te responderei com absolutamente nada de relevante."
        self.send_message_to_specific_person(user.user_id, greeting_text.format(user.first_name))
        user.greeted = True

    def send_initial_message(self, user):
        text = "Tem certeza? Está preparado para absolutamente nada, {0}?"
        self.send_message_to_specific_person(user.user_id, text.format(user.first_name))
        user.received_inicial_message = True

    def handle_updates(self):
        update = bottle_request.json
        print("\n\nNEW UPDATE\n{}\n\n".format(update)) #just for log

        if(update.get("callback_query")): #handle button click
            requests.get(self.api_base_url + "answerCallbackQuery", {'callback_query_id':update.get("callback_query").get("id")})
            user_id = update.get("callback_query").get("from").get("id")
            if(update.get("callback_query").get("data") == "google-pressed"):
                self.show_url(update.get("callback_query").get("message").get("chat").get("id"), update.get("callback_query").get("message").get("message_id"))
            else:
                self.send_message_to_specific_person(user_id, update.get("callback_query").get("data"))
            return

        user_id = update.get("message").get("from").get("id")
        user = self.users_list.get(user_id)
        if(user):
            MongoDB.newInteractionFromUser(user_id)
            if(not user.greeted):
                self.start_the_chat(user)
                return
            elif(not user.received_inicial_message):
                self.send_initial_message(user)
            else:
                self.send_message_to_specific_person(user_id, "A partir daqui eu ainda nao sei o que fazer hehehe desculpa")
        else:
            # setup users
            MongoDB.insertNewUser(update.get("message").get("from"))
            first_name = update.get("message").get("from").get("first_name")
            last_name  = update.get("message").get("from").get("last_name")
            username   = update.get("message").get("from").get("username")
            user = User(user_id, first_name, last_name, username)
            self.users_list[user_id] = user
            # greet user
            self.start_the_chat(user)

        return {"status":"up"}
