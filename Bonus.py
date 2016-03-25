import simpleguitk as simplegui #win
#import SimpleGUICS2Pygame.simpleguics2pygame as simplegui #linux

from Sprite import *
from ImageInfo import *
from Constants import *


class Bonus:

    def __init__(self, pos, bonus, image):
        self.__bonus_info = ImageInfo([45, 45], [90, 90], 40)
        self.pos = [pos[0],pos[1]]
        self.type = bonus
        self.sprite = Sprite(pos, [0.0, 0.0], 0, 0, image,
                             self.__bonus_info, WIDTH, HEIGHT)

    def get_sprite(self):
        return self.sprite

    def get_bonus_type(self):
        return self.type

    def get_position(self):
        return self.pos

    def update(self):
        self.sprite.update()

    def draw(self, canvas):
        self.sprite.draw(canvas)

    def collide(self, other_object):
        return self.sprite.collide(other_object)

