import requests
from BotHandler import BotHandler

if __name__ == '__main__':
        bot_token = input("Token: ")       # <-- Token recebido pelo botFather no telegram
        my_bot = BotHandler(bot_token)     # <-- Configurando o meu bot
        my_bot.run()
