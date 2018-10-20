from apscheduler.schedulers.blocking import BlockingScheduler
import requests

def timed_job():
  bot_token = os.environ.get("TOKEN")          # <-- Token nas variavais de ambiente do Heroku
    if(bot_token):
		bot_send_message = "https://api.telegram.org/bot{0}/sendMessage".format(bot_token)
		params = {'chat_id': os.environ.get("DEFAULT_USER_CHAT_ID"),
                  'text': "I am still alive :)"}
		requests.get(bot_send_message, params)

sched = BlockingScheduler()

sched.add_job(timed_job)
sched.add_job(timed_job, 'interval', minutes=5)

sched.start()