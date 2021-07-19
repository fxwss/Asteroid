from Engine import Object
from Engine.Canvas import Colors

from pygame import Surface
from pygame.math import Vector2
from pygame.locals import *

class Actor(Object):

  def update(self, *args, **kwargs):

    Input = kwargs['Input']
    delta_time = kwargs['delta_time'] / 1000

    move = Vector2(0.0, 0.0)

    if Input.Keyboard.is_pressed(K_a):
      move.x -= self.speed * delta_time
    elif Input.Keyboard.is_pressed(K_d):
      move.x += self.speed * delta_time
    
    if Input.Keyboard.is_pressed(K_w):
      move.y -= self.speed * delta_time
    elif Input.Keyboard.is_pressed(K_s):
      move.y += self.speed * delta_time
    
    self.move(move)

  def __init__(self, **kwargs):

    Canvas = kwargs['Canvas']

    self.speed = 1000
    self.image = Surface([100, 100])
    self.image.fill(Colors.WHITE)

    Object.__init__(self, self.image)

    self.move(Vector2(Canvas.rect.center))

