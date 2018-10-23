import sys, getopt, os
import requests
import json
from bottle import Bottle, response, request as bottle_request
from UserModel import User

class BotHandler(Bottle):
    #----------------
    # API ENDPOINTS
    #----------------
    ROOT_ENDPOINT                      = "/"
    SEND_MESSAGE_TO_BOT_USERS_ENDPOINT = "/{0}/send-message".format(os.environ.get("TOKEN"))
    HANDLE_RECEIVED_MESSAGE_ENDPOINT   = "/{0}/received-message".format(os.environ.get("TOKEN"))
    RUN_SCHEDULED_SCRIPT_ENDPOINT      = "/{0}/scheduled-script".format(os.environ.get("TOKEN"))
    GET_DATABASE_ENDPOINT              = "/get-database"

    # Telegram API constants
    api_base_url          = "https://api.telegram.org/bot{0}/" # {0} = bot_token
    get_updates_endpoint  = "getUpdates"   # no params
    send_message_endpoint = "sendMessage"  # params = chat_id, text

    # Database simulation
    users_list = {}

    # METHODS
    def __init__(self, token):
        # Setup
        super(BotHandler, self).__init__()
        self.token = token
        self.api_base_url = self.api_base_url.format(token)
        # Handle conversation
        self.route(self.ROOT_ENDPOINT, callback=self.handle_updates, method="POST")
        self.route(self.RUN_SCHEDULED_SCRIPT_ENDPOINT, callback=self.send_message_to_all_users, method="POST")
        self.route(self.GET_DATABASE_ENDPOINT, callback=self.return_database, method="GET")

    def send_message_to_all_users(self):
        for userid in self.users_list:
            self.send_message_to_specific_person(userid,"messaging everybody")

    def return_database(self):
        resp = {}
        for userid, user_model in self.users_list.items():
            resp[userid] = user_model.toJSON()
        # return 200 Success
        response.headers['Content-Type'] = 'application/json'
        return json.dumps(resp)

    def send_message_to_specific_person(self, chat_id, text):
        # setup
        method = self.send_message_endpoint
        keyboard = {"inline_keyboard": [[
                        { "text": "botão A",
                          "callback_data": "button-A-pressed"}, 
                        { "text": "botão B",
                          "callback_data": "button-B-pressed"}]]}

        params = {'chat_id': chat_id,
                  'text': text,
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
            user_id = update.get("callback_query").get("from").get("id")
            self.send_message_to_specific_person(user_id, update.get("callback_query").get("data"))
            return

        user_id = update.get("message").get("from").get("id")
        user = self.users_list.get(user_id)
        if(user):
            if(not user.greeted):
                self.start_the_chat(user)
                return
            elif(not user.received_inicial_message):
                self.send_initial_message(user)
            else:
                self.send_message_to_specific_person(user_id, "A partir daqui eu ainda nao sei o que fazer hehehe desculpa")
        else:
            # setup user
            first_name = update.get("message").get("from").get("first_name")
            last_name  = update.get("message").get("from").get("last_name")
            username   = update.get("message").get("from").get("username")
            user = User(user_id, first_name, last_name, username)
            self.users_list[user_id] = user
            # greet user
            self.start_the_chat(user)

        return {"status":"up"}
