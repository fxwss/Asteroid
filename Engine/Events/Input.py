from pygame.key import get_focused, get_pressed

class Keyboard:

  @staticmethod
  def is_pressed(key_code):
    if get_focused():
      return get_pressed()[key_code]

class Mouse:
  pass
