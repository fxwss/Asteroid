from pygame import transform, Surface
from pygame.sprite import Sprite
from pygame.math import Vector2
from pygame import draw

from Engine.Utils.time import *
from Engine.Utils.math import *

from Engine.Canvas import Colors, Canvas as Canvas_t

class Object(Sprite):

  def update(self, *args, **kwargs):
    pass

  def move(self, v):
    self.pos.x += v.x
    self.pos.y += v.y
    self.rect.x = int(self.pos.x - self.rect.width / 2)
    self.rect.y = int(self.pos.y - self.rect.height / 2)

  def rotate(self, angle):
    self.rotation += angle
    if img := transform.rotate(self.__image, self.rotation):
      self.image = img
      self.rect = self.image.get_rect(center = self.rect.center)
      return True
    return False

  def kill(self, clear_memory=False):
    self._kill(self)
    del self

  def debug(self, *args, **kwargs):
    
    Canvas: Canvas_t = kwargs['Canvas']

    def draw_hitbox(canvas):
      points = [
        self.rect.topleft,
        self.rect.topright,
        self.rect.bottomright,
        self.rect.bottomleft
      ]
      return draw.aalines(canvas, Colors.RED, True, points, 1)

    def draw_pos(canvas):
      pos = Canvas.text(f" pos = ({round(self.pos.x, 2)}, {round(self.pos.y, 2)})", Colors.WHITE, 'Arial', 12, antialias=True)
      return canvas.blit(pos, self.rect.topright)

    def draw_center(canvas):
      return draw.aalines(
        canvas,
        Colors.BLUE,
        False,
        [
          self.rect.center,
          self.rect.midright,
          self.rect.center,
          self.rect.midtop,
          self.rect.center,
          self.rect.midleft,
          self.rect.center,
          self.rect.midbottom
        ]
      )

    Canvas.add_draw_fun(draw_hitbox)
    Canvas.add_draw_fun(draw_pos)
    Canvas.add_draw_fun(draw_center)



  def __init__(self, img = None):
    Sprite.__init__(self)

    if img == None:
      img = Surface([0, 0])

    self.__image = img.copy()

    self.rotation = 0.0
    self.rotation_multiplier = 270.0 # pixel / second

    self.pos = Vector2(0.0, 0.0)
    self.image = self.__image.copy()
    self.rect = self.image.get_rect()

    self._kill = Sprite.kill

    self.born = now()
