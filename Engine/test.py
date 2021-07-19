from Engine import Game
from Engine.Canvas import Colors
from Actor import Actor

from pygame.math import Vector2

if __name__ == '__main__':
  game = Game("test")
  Canvas = game.Canvas

  def draw_fps(canvas):
    fps = Canvas.text(f"FPS: {int(Canvas.get_fps())}", Colors.WHITE, 'Arial', 16, antialias=True)
    frametime = Canvas.text(f"frametime: {round(Canvas.get_frametime(), 4)}ms", Colors.WHITE, 'Arial', 16, antialias=True)
    return [
      canvas.blit(fps, Canvas.rect.topleft),
      canvas.blit(frametime, [Canvas.rect.left, Canvas.rect.top + fps.get_height()])
    ]

  player = Actor(Canvas = Canvas)
  player.debug(Canvas = Canvas)


  Canvas.add_draw_fun(draw_fps)

  game.add_actor(player, 'player')

  game.start()
