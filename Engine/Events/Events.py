import pygame
from threading import Thread

from Engine.Utils.time import *
from . import Input

class Events:

  def __init__(self, auto_start=True):
    self.__pre_events = {}
    self.__after_events = {}
    self.__on_events = {}
    self.actions = (self.__pre_events, self.__on_events, self.__after_events)
    self._thread = None
    self.Input = Input

    if auto_start:
      self.start()

  def start(self):
    self._thread = Thread(
      target=self.__loop,
      daemon=True
    )
    self._thread.start()

  def __loop(self):
    while(1):
      while(event := pygame.event.poll()):
        self.call(event)
      sleep(1)

  @staticmethod
  def prevent_stop_working():
    pygame.event.pump()

  def call(self, event):
    for action in self.actions:
      if event.type in action:
        for function in action[event.type]:
          function(Input)

  def remove_callback(self, callback):
    for action in self.actions:
      for key in action.keys():
        if callback in action[key]:
          action[key].remove(callback)

  def after(self, *events, callback):
    for event_type in events:
      if not event_type in self.__after_events:
        self.__after_events[event_type] = []
      self.__after_events[event_type].append(callback)
      return callback

  def pre(self, *events, callback):
    for event_type in events:
      if not event_type in self.__pre_events:
        self.__pre_events[event_type] = []
      self.__pre_events[event_type].append(callback)
      return callback

  def on(self, *events, callback):
    for event_type in events:
      if not event_type in self.__on_events:
        self.__on_events[event_type] = []
      self.__on_events[event_type].append(callback)
      return callback
