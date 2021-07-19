from pygame.sprite import Sprite
from pygame import Surface
from pygame.locals import * # pylint: disable=unused-wildcard-import
from pygame.math import Vector2 # pylint: disable=no-name-in-module
from pygame import draw
from pygame import transform

from math import cos, sin, pi, sqrt

from Engine.Object import Object
from Engine.Canvas import Colors
from Engine.Utils.math import *
from Engine.Utils.time import *

from Bullet import Bullet

class Actor(Object):

  def update(self, *args, **kwargs):

    #kwargs = kwargs['kwargs']

    Input = kwargs['Input']
    Canvas = kwargs["Canvas"]
    delta_time = kwargs["delta_time"]
    groups = kwargs['groups']
    game = kwargs['game']

    # Rotation

    rotation = 0.0

    if Input.Keyboard.is_pressed(K_RIGHT): # pylint: disable=undefined-variable
      rotation -= self.rotation_multiplier * delta_time
    
    if Input.Keyboard.is_pressed(K_LEFT): # pylint: disable=undefined-variable
      rotation += self.rotation_multiplier * delta_time

    if abs(rotation) > 0.0:
      self.rotate(rotation)
    
    # End Rotation

    # Moviment

    speed = Vector2(0.0, 0.0)

    if Input.Keyboard.is_pressed(K_UP): # pylint: disable=undefined-variable
      speed.y -= self.acceleration * delta_time
    
    if Input.Keyboard.is_pressed(K_DOWN): # pylint: disable=undefined-variable
      speed.y += self.acceleration * delta_time

    rotated = speed.rotate(-self.rotation)

    self.velocity.x += rotated.x
    self.velocity.y += rotated.y

    if self.velocity.length() > self.max_velocity:
      self.velocity = self.velocity.normalize() * self.max_velocity

    if abs(self.velocity.x) > 0.0:
      self.velocity.x += self.stop_rate * delta_time * -(self.velocity.x / abs(self.velocity.x))

    if abs(self.velocity.y) > 0.0:
      self.velocity.y += self.stop_rate * delta_time * -(self.velocity.y / abs(self.velocity.y))

    self.move(Vector2(
      self.velocity.x * delta_time,
      self.velocity.y * delta_time
    ))

    # End Moviment

    # Shooting


    # End Shooting

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

    if Input.Keyboard.is_pressed(K_SPACE) and timediff(self.last_shot) > self.shot_cooldown: # pylint: disable=undefined-variable
      direction = Vector2(
        -sin(angle_to_rad(self.rotation)),
        -cos(angle_to_rad(self.rotation))
      )
      pit = sqrt(pow(self.rect.width, 2) + pow(self.rect.height, 2)) / 2
      pos =[self.rect.center[0] + direction.x * pit, self.rect.center[1] + direction.y * pit]
      b = Bullet(Colors.WHITE, 5, pos, self.rotation, Canvas = Canvas, Game = game)
      game.add_actor(b, 'bullets')
      self.last_shot = now()

    # Collision
    sprites = groups['asteroids'].sprites()
    rects = list(map(lambda s: s.rect, sprites))
    if self.rect.collidelist(rects) > -1:
      self.kill()

    # End coliision

  def make_sprite(self, size, color):
    original_image = Surface([size, size], SRCALPHA) # pylint: disable=undefined-variable
    rect = original_image.get_rect()

    padding = 1

    bottom_right = Vector2(rect.bottomright)
    bottom_left = Vector2(rect.bottomleft)
    mid_top = Vector2(rect.midtop)

    bottom_right.x -= padding
    bottom_right.y -= padding

    bottom_left.y -= padding
    bottom_left.x += padding
    
    mid_top.y += padding

    # Triangle
    points = [
      bottom_left,
      mid_top,
      bottom_right,
      [rect.center[0], rect.center[1] * 1.5],
    ]

    draw.polygon(original_image, color, points, 1)

    return original_image.copy()

  def __init__(self, color, size, **kwargs):

    Canvas = kwargs["Canvas"]
    Game = kwargs["Game"]

    self.image = self.make_sprite(size, color)
    #self.image.fill([255, 0, 0])
    Object.__init__(self, self.image)

    self.rotation = 0.0
    self.rotation_multiplier = 270.0 # pixel / second
    self.shot_cooldown = 300 # ms
    self.last_shot = now()

    self.velocity = Vector2(0.0, 0.0) # pixel / second
    self.max_velocity = 250.0 # pixel / second
    self.acceleration = self.max_velocity * 2 # pixel / second²
    self.stop_rate = 60 # pixel / second

    self.move(Vector2(Canvas.rect.center))
