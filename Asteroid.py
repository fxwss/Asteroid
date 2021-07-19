from pygame.sprite import Sprite
from pygame import Surface
from pygame.locals import * # pylint: disable=unused-wildcard-import
from pygame.math import Vector2 # pylint: disable=no-name-in-module
from pygame import draw
from pygame import transform

from math import cos, sin, pi, sqrt, pow

from Engine.Object import Object
from Engine.Utils.math import *
from Engine.Utils.time import *

import random

class Asteroid(Object):

  def update(self, *args, **kwargs):

    #kwargs = kwargs['kwargs']

    Input = kwargs['Input']
    Canvas = kwargs["Canvas"]
    delta_time = kwargs["delta_time"]
    groups = kwargs['groups']
    game = kwargs['game']

    # Moviment

    self.move(Vector2(
      self.velocity.x * delta_time,
      self.velocity.y * delta_time
    ))

    # End Moviment

    # Collision

    for bullet in groups['bullets'].sprites():
      distance = ((bullet.rect.center[0] - self.rect.center[0]) ** 2 + (bullet.rect.center[1] - self.rect.center[1]) ** 2) ** (1/2)
      if distance <= self.size / 2 and timediff(self.born) > self.invulnerable_time:
        if self.lifes > 1:
          asteroids_ = [Asteroid(self.color, self.size * (random.randint(50, 80) / 100), Canvas = Canvas, Game = game, pos = self.pos, lifes = self.lifes - 1) for i in range(random.randint(1, 4))]
          for a in asteroids_:
            game.add_actor(a, 'asteroids')
        self.kill(clear_memory=True)

    # sprites = groups['bullets'].sprites()
    # rects = list(map(lambda s: s.rect, sprites))
    # if self.rect.collidelist(rects) > -1 and timediff(self.born) > self.invulnerable_time:
    #   if self.lifes > 1:
    #     asteroids_ = [Asteroid(self.color, self.size * (random.randint(50, 80) / 100), Canvas = Canvas, Game = game, pos = self.pos, lifes = self.lifes - 1) for i in range(random.randint(1, 4))]
    #     for a in asteroids_:
    #       game.add_actor(a, 'asteroids')
    #   self.kill(clear_memory=True)

    # End collision

    # In bounds

    if self.rect.center[0] > Canvas.rect.right:
      self.move(Vector2(
        -Canvas.rect.right,
        0.0
      ))
      #self.rect.move_ip(-Canvas.rect.right, 0)
    
    elif self.rect.center[0] < Canvas.rect.left:
      self.move(Vector2(
        Canvas.rect.right,
        0.0
      ))

    if self.rect.center[1] > Canvas.rect.bottom:
      self.move(Vector2(
        0.0,
        -Canvas.rect.bottom
      ))
    
    elif self.rect.center[1] < Canvas.rect.top:
      self.move(Vector2(
        0.0,
        Canvas.rect.bottom
      ))

    # End In bounds
    
  def make_sprite(self, size, color):
    original_image = Surface([size, size], SRCALPHA) # pylint: disable=undefined-variable
    rect = original_image.get_rect()

    draw.ellipse(original_image, color, rect, width = 1)

    return original_image.copy()

  def __init__(self, color, size, **kwargs):

    Canvas = kwargs["Canvas"]
    Game = kwargs["Game"]

    self.invulnerable_time = 200

    self.lifes = 2

    if 'lifes' in kwargs.keys():
      self.lifes = kwargs['lifes']

    self.color = color
    self.size = size

    self.image = self.make_sprite(size, color)
    Object.__init__(self, self.image)

    self.velocity = Vector2(0.0, 0.0) # pixel / second
    self.max_velocity = 80.0 # pixel / second

    self.velocity.x += self.max_velocity * random.random()
    self.velocity.y += self.max_velocity * random.random()

    if self.velocity.length() > self.max_velocity:
      self.velocity = self.velocity.normalize() * self.max_velocity


    non_spawnanble_area = Canvas.rect.copy()

    non_spawnanble_area.inflate_ip(
      non_spawnanble_area.width * -0.4,
      non_spawnanble_area.height * -0.4
    )

    non_spawnanble_area.move_ip(Vector2(
      Canvas.rect.center[0] - non_spawnanble_area.width / 2,
      Canvas.rect.center[1] - non_spawnanble_area.height / 2
    ))

    pos = Vector2(
      random.randrange(0, Canvas.rect.right),
      random.randrange(0, Canvas.rect.bottom)
    )

    while non_spawnanble_area.collidepoint(pos):
      pos = Vector2(
        random.randrange(0, Canvas.rect.right),
        random.randrange(0, Canvas.rect.bottom)
      )

    if 'pos' in kwargs.keys():
      pos = kwargs['pos']

    self.move(pos)


