from AppHandler import AppHandler
import sys, getopt, os
import Constants 

if __name__ == '__main__':
    #-----------
    # SETUP
    #----------- 
    if (not Constants.BOT1_TOKEN || not Constants.BOT2_TOKEN):  
        print()
        print('SETUP FAIL!')
        print("Please set the BOT1_TOKEN and BOT2_TOKEN config. vars.")
        print()
        sys.exit()

    #----------------
    # START THE BOT
    #----------------
    app = AppHandler()
    port = int(os.environ.get("PORT", 5000))     # <-- Como o Heroku muda de porta o tempo todo temos que nos adaptar
    app.run(host='0.0.0.0', port=port)           # <-- IT'S ALIVE!
