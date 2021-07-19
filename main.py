import time
from pygame import Surface
from Engine import Game
from Actor import Actor
from Asteroid import Asteroid

from pygame.locals import *  # pylint: disable=unused-wildcard-import
from random import randint

from Engine.Canvas import Colors

import random

def main():
  game = Game("Asteroid")

  # game.Canvas.set_max_fps(600)

  player = Actor(Colors.WHITE, 30, Canvas=game.Canvas, Game = game)

  game.add_actor(player, 'player')
  game.add_actor(None, 'bullets')

  for i in range(randint(5, 13)):
    asteroid = Asteroid(Colors.WHITE,
                        random.randint(30, 45),
                        Canvas=game.Canvas,
                        Game=game)
    game.add_actor(asteroid, 'asteroids')

  last_fps_print = 0.0
  last_fps = 0.0
  def draw_fps(canvas: Surface):
    nonlocal last_fps_print, last_fps
    last_update = time.time()
    if(last_update - last_fps_print >= .1):
      last_fps_print = last_update
      last_fps = game.Canvas.text(f'FPS: {round(game.Canvas.get_fps(), 2)}', Colors.WHITE, 'arial', 18, True)
    return canvas.blit(last_fps, (0, 0))
  
  last_frametime_print = 0.0
  last_frametime = 0.0
  def draw_frametime(canvas: Surface):
    nonlocal last_frametime_print, last_frametime
    last_update = time.time()
    if(last_update - last_frametime_print >= .1):
      last_frametime_print = last_update
      last_frametime = game.Canvas.text(f'FRAMETIME: {game.Canvas.get_frametime()}', Colors.WHITE, 'arial', 18, True)
    return canvas.blit(last_frametime, (0, 18))
    

  game.Canvas.add_draw_fun(draw_fps)
  game.Canvas.add_draw_fun(draw_frametime)

  game.start()

if __name__ == "__main__":
  main()
