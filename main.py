import sys, getopt
from BotHandler import BotHandler

if __name__ == '__main__':
    # SETUP
    try:
        opts, args = getopt.getopt(sys.argv[1:],"",longopts=["token"])
        bot_token = args[0]            # <-- Token recebido por parâmetro ao iniciar o app
                                       #     conseguido através do botFather no telegram
    except getopt.GetoptError:
        print()
        print('Wrong usage!')
        print("Use the parameter --token <BOT_TOKEN> to run.")
        print()
        sys.exit()
    # START THE BOT
    my_bot = BotHandler(bot_token)     # <-- Configurando o meu bot
    my_bot.run()                       # <-- IT'S ALIVE!
