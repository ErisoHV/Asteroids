# Spaceship - Erika ^^
import simpleguitk as simplegui
#import simplegui
import random

from Sprite import Sprite
from ImageInfo import ImageInfo
from Ship import Ship
from Utils import Utils

# user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
gameover = False
started = False
explosion_group = set()
#game
FRICTION = 0.97
FACTOR = 2
missile = False
MAX_ROCKS = 12
SAFEDISTANCE = 45
difficulty = [-1, 0.5]

#  ------------- IMAGES ---------------------------#
# art assets created by Kim Lathrop
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://127.0.0.1:8083/debris2_blue.png")
# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://127.0.0.1:8083/nebula_blue.f2013.png")
# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://127.0.0.1:8083/splash.png")
#https://googledrive.com/host/0B0ugO7CFvC4yNEVvc3dpamN6SFU/ricerocksgameover.png
gameover_image = simplegui.load_image("http://127.0.0.1:8083/ricerocksgameover.png")
# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://127.0.0.1:8083/double_ship.png")
# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
#self, center, size, radius = 0, lifespan = None, animated = False
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://127.0.0.1:8083/asteroid_blue.png")
# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://127.0.0.1:8083/explosion_alpha.png")

# ------------------- SOUNDS ----------------------------#
# purchased from sounddogs.com
soundtrack = simplegui.load_sound("http://127.0.0.1:8083/soundtrack.ogg")
explosion_sound = simplegui.load_sound("http://127.0.0.1:8083/explosion.ogg")


def process_sprite_group(group, canvas):
    copy = group.copy()
    for i in copy:
        if i.update():
            group.discard(i)
        else:
            i.draw(canvas)


def group_collide (group, other_object):
    global explosion_group
    copy = group.copy()
    for i in copy:
        if i.collide(other_object):
            #..the colliding object should be removed from the group
            explosion_group.add(Sprite(i.get_position(),[0,0],0,0, explosion_image, explosion_info, WIDTH, HEIGHT, explosion_sound))
            group.discard(i)

            return True
    return False


def group_group_collide(group1, group2):
    copy = group1.copy()
    collisions = 0
    for i in copy:
        if group_collide(group2,i):
            collisions += 1
            group1.discard(i)
    return collisions


#helper functions to the interface
def reset():
    global score,my_ship, lives, time, started, missile, \
        rock_group, cant_rocks, missile_group, gameover, explosion_group
    score = 0
    lives = 3
    time = 0.5
    difficulty = [-1,0.5]
    started = False
    gameover = False
    missile = False
    my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info, WIDTH, HEIGHT)
    cant_rocks = 0
    rock_group = set()
    missile_group = set()
    explosion_group = set()
    explosion_sound.rewind()
    soundtrack.rewind()
    soundtrack.play()


#Key handlers
def keydown(key):
    global missile
    if (started):
        if (key == simplegui.KEY_MAP["left"]):
            my_ship.turn("left")
        elif (key == simplegui.KEY_MAP["right"]):
            my_ship.turn("right")
        elif (key == simplegui.KEY_MAP["up"]):
            my_ship.thrust_on()
        elif (key == simplegui.KEY_MAP["down"]):
            my_ship.thrust_off()
        elif (key == simplegui.KEY_MAP["space"]):
            missile = True
            my_ship.shoot(missile_group)


def keyup(key):
    if (started):
        if (key == simplegui.KEY_MAP["left"] or key == simplegui.KEY_MAP["right"]):
            my_ship.turn()
        elif (key == simplegui.KEY_MAP["up"]):
            my_ship.thrust_off()
        elif (key == simplegui.KEY_MAP["down"]):
            my_ship.thrust_off()


def mouse_handler(position):
    global started, gameover
    if (not started or gameover):
        reset()
        started = True


def draw(canvas):
    global time, lives, score, cant_colli, cant_rocks, started, gameover,difficulty
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    if (started):
        # draw ship and sprites
        my_ship.draw(canvas)
        my_ship.update()
        process_sprite_group(rock_group, canvas)

        #Ship-Rocks Collisions
        if(group_collide (rock_group, my_ship)):
            lives -= 1
            cant_rocks -= 1

        #game over
        if (lives == -1):
            started = False
            gameover = True
            lives = 0
            score = 0

        #Rocks-Missiles Collisions
        if (missile):
            process_sprite_group(missile_group, canvas)
            cant_colli = group_group_collide (missile_group, rock_group)
            score +=  cant_colli
            cant_rocks -=  cant_colli
            if (cant_colli > 0 and difficulty[0] <= 1 and difficulty[1] <= 5):
                difficulty[0] += 0.1
                difficulty[1] += 0.1
                print difficulty

        for explosion in explosion_group.copy():
            explosion.draw(canvas)
            explosion.age += 1
            if explosion.age >= 300:
                explosion_group.remove(explosion)
            explosion.update()
    else:
        if (gameover):
            canvas.draw_image(gameover_image, splash_info.center, splash_info.size, [WIDTH/2, HEIGHT/2], splash_info.size)
            soundtrack.rewind()
            my_ship.stopShipSound()
        else:
            canvas.draw_image(splash_image, splash_info.center, splash_info.size, [WIDTH/2, HEIGHT/2], splash_info.size)

    #score
    canvas.draw_text("Lives", [30,30], 30, "White",  "monospace")
    canvas.draw_text(str(lives), [65,60], 30, "White",  "monospace")
    canvas.draw_text("Score", [650,30], 30, "White",  "monospace")
    canvas.draw_text(str(score), [685,60], 30, "White",  "monospace")


# timer handler that spawns a rock
def rock_spawner():
    if (started):
        global rock_group, cant_rocks
        if(cant_rocks < MAX_ROCKS):
            angvel = random.choice([0.05,0.3]) * random.random()
            vel = [random.choice(difficulty) * random.random(),
                        random.choice(difficulty) * random.random()]
            pos = [random.randint(1,WIDTH),random.randint(1,HEIGHT) ]
            while (Utils().dist(my_ship.pos, pos) < (my_ship.get_radius() + SAFEDISTANCE)):
                pos = [random.randint(1,WIDTH),random.randint(1,HEIGHT) ]

            rock_group.add(Sprite(pos, vel, 0, angvel, asteroid_image, asteroid_info, WIDTH, HEIGHT))
            cant_rocks += 1

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(mouse_handler)
frame.set_keyup_handler(keyup)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()