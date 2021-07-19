from pygame.sprite import Sprite
from pygame import Surface
from pygame.locals import * # pylint: disable=unused-wildcard-import
from pygame.math import Vector2 # pylint: disable=no-name-in-module
from pygame import draw
from pygame import transform

from math import cos, sin, pi, sqrt, pow

from Engine.Object import Object

class Bullet(Object):

  def update(self, *args, **kwargs):

    #kwargs = kwargs['kwargs']

    Input = kwargs['Input']
    Canvas = kwargs["Canvas"]
    delta_time = kwargs["delta_time"]
    groups = kwargs['groups']

    # Moviment

    self.move(Vector2(
      self.velocity.x * delta_time,
      self.velocity.y * delta_time
    ))

    # End Moviment

    # In bounds

    if not Canvas.rect.collidepoint(self.rect.center):
      self.kill(clear_memory=True)

    # End In bounds

    
  def make_sprite(self, size, color):
    original_image = Surface([size, size], SRCALPHA) # pylint: disable=undefined-variable
    rect = original_image.get_rect()

    draw.ellipse(original_image, color, rect)

    return original_image.copy()

  def __init__(self, color, size, origin, angle, **kwargs):

    Canvas = kwargs["Canvas"]
    Game = kwargs["Game"]

    self.image = self.make_sprite(size, color)
    Object.__init__(self, self.image)

    self.rotation = angle
    self.direction = Vector2(
      -sin(self.rotation * pi / 180),
      -cos(self.rotation * pi / 180)
    )

    self.velocity = Vector2(0.0, 0.0) # pixel / second
    self.max_velocity = 800.0 # pixel / second
    self.stop_rate = 0 # pixel / second

    self.velocity.x = self.max_velocity * self.direction.x
    self.velocity.y = self.max_velocity * self.direction.y

    if self.velocity.length() > self.max_velocity:
      self.velocity = self.velocity.normalize() * self.max_velocity

    self.move(Vector2(origin))
