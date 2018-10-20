from apscheduler.schedulers.blocking import BlockingScheduler

print("start")
sched = BlockingScheduler()
print("-> sched created")

def timed_job():
  print('This job is run every 5 minutes.')

sched.add_job(timed_job)
sched.add_job(timed_job, 'interval', minutes=5)
print("-> sched scheduled")

sched.start()
print("-> this is the end")
