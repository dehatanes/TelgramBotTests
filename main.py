import sys, getopt
from bottle import Bottle, response, request as bottle_request
from BotHandler import BotHandler

if __name__ == '__main__':
    #-----------
    # SETUP
    #-----------    
    try:
        opts, args = getopt.getopt(sys.argv[1:],"",longopts=["token"]) # parametrizar o webhook depois
        bot_token = args[0]            # <-- Token recebido por parâmetro ao iniciar o app
                                       #     conseguido através do botFather no telegram
    except getopt.GetoptError:
        print()
        print('Wrong usage!')
        print("Use the parameter --token <BOT_TOKEN> to run.")
        print()
        sys.exit()

    #----------------
    # START THE BOT
    #----------------
    app = BotHandler(bot_token)                  # <-- Configurando o meu bot
    port = int(os.environ.get("PORT", 5000))     # <-- Como o Heroku muda de porta o tempo todo temos qu nos adaptar
    app.run(host='0.0.0.0', port=port)           # <-- IT'S ALIVE!
