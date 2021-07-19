import time

calc_time_to_sleep = lambda fps: (1 / fps) * 1000

def sleep(ms):
  time.sleep(ms / 1000)

def now():
  return time.time() * 1000

def timediff(x, y = None):
  if y == None: y = now()
  return y - x
