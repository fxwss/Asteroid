from pygame import display, Surface
from pygame import font as pgFont
from threading import Thread, Lock

from Engine.Utils.time import *
from . import Colors

display.init()

class Canvas:

  def __init__(self, group, auto_start=True):
    self._sprites = group
    self._canvas = display.set_mode((800, 600))
    self.rect = self._canvas.get_rect()
    self.__max_fps = 300
    self.__time_to_sleep = calc_time_to_sleep(self.__max_fps)
    self._thread = None
    self._last_update_timediff = 0.0
    self.perimeter = []
    self.geometry = []
    self.font_buffer = {}

    if auto_start:
      self.start()

  def add_font(self, name, font_obj):
    self.font_buffer[name] = font_obj

  def remove_font(self, name):
    if name in self.font_buffer.keys():
      del self.font_buffer[name]

  def remove_draw_fun(self, func):
    if func in self.geometry:
      self.geometry.remove(func)
      return True
    return False

  def add_draw_fun(self, func):
    self.geometry.append(func)
    return func

  def set_max_fps(self, fps):
    self.__max_fps = fps
    self.__time_to_sleep = calc_time_to_sleep(self.__max_fps)

  def get_fps(self):
    if self._last_update_timediff > 0:
      return 1.0 / (self._last_update_timediff / 1000)
    return 0.0
  
  def get_frametime(self):
    return self._last_update_timediff

  def start(self):
    self._thread = Thread(
      target=self.__loop,
      daemon=True
    )

    self._thread.start()

  def text(self, text, color, font, size, antialias = False):

    font_id = f"{font},{size}"

    font = None
    if font_id in self.font_buffer.keys():
      font = self.font_buffer[font_id]
    else:
      font = pgFont.SysFont(font, size)
      self.add_font(font_id, font)

    return font.render(text, antialias, color)

  def __loop(self):
    rects = []
    while(1):
      start = now()
      self._canvas.fill(Colors.BLACK)
      rects += self._sprites.draw(self._canvas)
      g_rects = list(map(lambda f: f(self._canvas), self.geometry))

      for t in g_rects:
        if type(t) is list:
          g_rects.remove(t)
          for i in t:
            g_rects.append(i)

      rects += g_rects
      display.update(rects)
      rects.clear()
      rects += g_rects
      sleep(self.__time_to_sleep - 1.000244140625)
      self._last_update_timediff = timediff(start)