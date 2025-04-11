from sprite import *
from image_info import *
from constants import *

class Bonus:

    def __init__(self, pos, bonus, image):
        self.__bonus_info = ImageInfo([45, 45], [90, 90], 40)
        self.pos = [pos[0],pos[1]]
        self.type = bonus
        self.angle = 0
        self.angle_vel = 0.003

        self.sprite = Sprite(pos, [0.0, 0.0], self.angle, self.angle_vel, image,
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
        #angle
        self.angle += self.angle_vel
        #position (static)
        self.pos[0] += self.pos[0]
        self.pos[1] += self.pos[1]
        self.sprite.draw(canvas)

    def collide(self, other_object):
        return self.sprite.collide(other_object)

