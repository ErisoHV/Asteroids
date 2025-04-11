from so import *
from sprite import Sprite
from image_info import ImageInfo
from utils import Utils
from constants import *

try:
    ship_thrust_sound = simplegui.load_sound(THRUST)
except Exception:
    ship_thrust_sound = None

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 150)
missile_image = simplegui.load_image(SHOT)

try:
    missile_sound = simplegui.load_sound(MISSILE)
except Exception:
    missile_sound = None

FRICTION = 0.97
FACTOR = 2

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 150)
missile_image = simplegui.load_image(SHOT)

missile_sound.set_volume(.5)

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info, Wwith, WHeight):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.parentWidth = Wwith
        self.parentHeight = WHeight

    def draw(self,canvas):
        canvas.draw_image(self.image,self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def update(self):
        #angle
        self.angle += self.angle_vel
        #velocity
        if (self.thrust):
            #forward
            forward = Utils().angle_to_vector(self.angle)
            #acceleration
            self.vel[0] += forward[0]/6
            self.vel[1] += forward[1]/6
        #friction
        self.vel = [self.vel[0] * FRICTION, self.vel[1] * FRICTION]
        #position
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        #wraps
        self.pos[0] %= self.parentWidth
        self.pos[1] %= self.parentHeight

    def thrust_on(self):
        self.thrust = True
        self.image_center[0] = 135
        ship_thrust_sound.play()

    def thrust_off(self):
        self.thrust = False
        self.image_center[0] = 45
        #stops with slowdown
        self.vel[0] *= (1-.5)
        self.vel[1] *= (1-.5)
        ship_thrust_sound.rewind()

    def turn (self, direction = None):
        if (direction == "right"):
            self.angle_vel += 0.06
        elif (direction == "left"):
            self.angle_vel -= 0.06
        #Stop!
        else:
            self.angle_vel = 0

    def shoot(self, missile_group):
        #global missile_group
        forward = Utils().angle_to_vector(self.angle)
        #tip of the ship cannon
        pos = [self.pos[0] + self.radius * forward[0],
        self.pos[1] + self.radius * forward[1]]
        #velocity of the missile
        vel = [self.vel[0] + FACTOR * forward[0] ,
        self.vel[1] + FACTOR * forward[1]]
        missile_group.add(Sprite(pos, vel, self.angle, self.angle_vel, missile_image,
                                 missile_info, self.parentWidth,
        self.parentHeight, missile_sound))

    def stopShipSound(self):
        ship_thrust_sound.rewind()
        missile_sound.rewind()
