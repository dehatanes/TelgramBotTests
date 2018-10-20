import sys, getopt, os
from BotHandler import BotHandler

if __name__ == '__main__':
    #-----------
    # SETUP
    #-----------    
    bot_token = os.environ.get("TOKEN")          # <-- Token nas variavais de ambiente do Heroku
    if(!bot_token):
        print()
        print('SETUP FAIL!')
        print("Please set the TOKEN config. var. with the bot token.")
        print()
        sys.exit()

    #----------------
    # START THE BOT
    #----------------
    app = BotHandler(bot_token)                  # <-- Configurando o meu bot
    port = int(os.environ.get("PORT", 5000))     # <-- Como o Heroku muda de porta o tempo todo temos qu nos adaptar
    app.run(host='0.0.0.0', port=port)           # <-- IT'S ALIVE!
