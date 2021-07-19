import Engine
from time import time as now

from Engine.Utils.math import *
from Engine.Utils.time import *

from pygame.locals import * # pylint: disable=unused-wildcard-import
from pygame.sprite import Group, LayeredUpdates
from pygame.display import set_caption, set_icon

from concurrent.futures import ThreadPoolExecutor

class Game:

  def __init__(self, title="", icon=None):
    
    set_caption(title)
    if not icon == None:
      set_icon(icon)

    self.groups = {
      'main' : Group(),
      '__render' : LayeredUpdates()
    }

    self.Canvas = Engine.Canvas(self.groups['__render'])
    self.Events = Engine.Events()
    self.delta_time = now()
    self.running = True
    
    self.__tick = 300
    self.__time_to_sleep = calc_time_to_sleep(self.__tick)
    self.__debug = True

    self.Events.on(QUIT, callback=lambda Input: self.stop()) # pylint: disable=undefined-variable

  def set_tick(self, tick):
    self.__tick = tick
    self.__time_to_sleep = calc_time_to_sleep(self.__tick)

  def add_actor(self, actor, group_name='main'):

    if not group_name in self.groups.keys():
      self.groups[group_name] = Group()
    
    if actor == None:
      return

    if not group_name == 'main':
      self.groups[group_name].add(actor)

    self.groups['main'].add(actor)
    self.groups['__render'].add(actor)

  def start(self):
    self.logic()

  def stop(self):
    self.running = False

  def logic(self):
    last_update = now()
    while(self.running):
      n = now()
      self.Events.prevent_stop_working()
      self.groups['main'].update(
        Input = self.Events.Input,
        Canvas = self.Canvas,
        delta_time = (n - last_update) / 1000,
        groups = self.groups,
        game = self
      )
      sleep(self.__time_to_sleep)
      last_update = n

if __name__ == "__main__":
  pass

