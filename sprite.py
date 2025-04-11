from utils import Utils
# Sprite class


class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info,
                 Wwidth, WHeight, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        self.parentWidth = Wwidth
        self.parentHeight = WHeight

        if sound:
            sound.rewind()
            sound.play()

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def draw(self, canvas):
        if (not self.animated):
            canvas.draw_image(self.image,self.image_center, self.image_size, self.pos,
                              self.image_size, self.angle)
        else:
            self.image_center[0]=64*(1+self.age)
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos,
                              self.image_size, self.angle)

    def update(self):
        #angle
        self.angle += self.angle_vel
        #position
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.pos[0] %= self.parentWidth
        self.pos[1] %= self.parentHeight
        #age
        self.age += 1
        return self.age >= self.lifespan

    def collide(self,other_object):
        d = Utils().dist(self.pos, other_object.get_position())
        if d < self.radius + other_object.get_radius():
            return True
        return False