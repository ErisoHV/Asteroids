from so import *
import random
from bonus import *
from constants import *
from ship import Ship
from utils import Utils

# user interface
score = 0
lives = 3
time = 0.5
game_over = False
started = False
explosion_group = set()
rock_group = set()
bonus_group = set()

# game
missile = False

#  ------------- IMAGES ---------------------------#
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image(DEBRIS)

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image(NEBULA)
# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image(SPLASH)
gameover_image = simplegui.load_image(GAMEOVER)
# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image(SHIP)
# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image(ASTEROID)

# bonus
bonus_info = ImageInfo([45, 45], [90, 90], 40)
bonus_image1 = simplegui.load_image(BONUS1)
bonus_image2 = simplegui.load_image(BONUS2)
bonus_image3 = simplegui.load_image(BONUS3)
bonus_image4 = simplegui.load_image(BONUS4)

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image(EXPLOSION)

# bonus
seconds = 0
timer3 = None
immortal = False
scoreBonus = False

# ------------------- SOUNDS ------------------------#
try:
    soundtrack = simplegui.load_sound(SOUNDTRACK)
except Exception:
    soundtrack = None

try:
    explosion_sound = simplegui.load_sound(EXPLOSIONSOUND)
except Exception:
    explosion_sound = None

try:
    tick_tock_sound = simplegui.load_sound(TICKTOCKSOUND)
except Exception:
    tick_tock_sound = None

asteroid_image = simplegui.load_image(ASTEROID)
# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image(EXPLOSION)

def process_sprite_group(group, canvas):
    copy = group.copy()
    for i in copy:
        if i.update():
            group.discard(i)
        else:
            i.draw(canvas)


def process_bonus(bonus):
    global lives, explosion_group, rocks_number, rock_group, timer3, score, \
        immortal, scoreBonus, seconds, functionTimer
    if bonus.type == 3:  # lives++
        lives += 1
    elif bonus.type == 4:  # exploit all the asteroids
        copy = rock_group.copy()
        for i in copy:
            explosion_group.add(Sprite(i.get_position(), [0, 0], 0, 0,
                                       explosion_image, explosion_info,
                                       WIDTH, HEIGHT, explosion_sound))
            rock_group.discard(i)
            rocks_number -= 1
            score += 1
    else:
        if bonus.type == 2:  #each asteroid is +2
            scoreBonus = True
            immortal = False
        elif bonus.type == 1:  #the asteroids not hurt you
            immortal = True
            scoreBonus = False

        if timer3 is not None:
            timer3.stop()
            seconds = 0

        timer3 = simplegui.create_timer(1000, timer_bonus_1_2)
        tick_tock_sound.rewind()
        tick_tock_sound.play()
        timer3.start()


def timer_bonus_1_2():
    global seconds, timer3, scoreBonus, immortal
    if seconds < 10:
        seconds += 1
    else:
        seconds = 0
        tick_tock_sound.rewind()
        scoreBonus = False
        immortal = False
        timer3.stop


def group_collide(group, other_object, isBonus = False):
    global explosion_group, bonus_group
    copy = group.copy()
    for i in copy:
        if i.collide(other_object):
            # the colliding object should be removed from the group
            if isBonus:
                process_bonus(i)

            explosion_group.add(Sprite(i.get_position(),[0,0],0,0, explosion_image, explosion_info, 
                                       WIDTH, HEIGHT, explosion_sound))
            group.discard(i)
            return True
    return False


def group_group_collide(group1, group2):
    copy = group1.copy()
    collisions = 0
    for i in copy:
        if group_collide(group2, i):
            collisions += 1
            group1.discard(i)
    return collisions


# helper functions to the interface
def reset():
    global score, my_ship, lives, time, started, missile, \
        rock_group, rocks_number, missile_group, game_over, difficulty, \
        explosion_group, bonus_group
    global score,my_ship, lives, time, started, missile, \
    rock_group, rocks_number, missile_group, game_over, difficulty, explosion_group

    explosion_group, difficulty
    score = 0
    lives = 3
    time = 0.5
    difficulty = [-1, 0.5]
    started = False
    game_over = False
    missile = False
    my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info, WIDTH, HEIGHT)
    rocks_number = 0
    rock_group = set()
    missile_group = set()
    explosion_group = set()
    bonus_group = set()
    explosion_sound.rewind()
    soundtrack.rewind()
    soundtrack.play()
    tick_tock_sound.rewind()


# Key handlers
def keydown(key):
    global missile
    if started:
        if key == simplegui.KEY_MAP["left"]:
            my_ship.turn("left")
        elif key == simplegui.KEY_MAP["right"]:
            my_ship.turn("right")
        elif key == simplegui.KEY_MAP["up"]:
            my_ship.thrust_on()
        elif key == simplegui.KEY_MAP["down"]:
            my_ship.thrust_off()
        elif key == simplegui.KEY_MAP["space"]:
            missile = True
            my_ship.shoot(missile_group)


def keyup(key):
    if started:
        if key == simplegui.KEY_MAP["left"] or key == simplegui.KEY_MAP["right"]:
            my_ship.turn()
        elif key == simplegui.KEY_MAP["up"]:
            my_ship.thrust_off()
        elif key == simplegui.KEY_MAP["down"]:
            my_ship.thrust_off()
        elif key == simplegui.KEY_MAP["P"] or key == simplegui.KEY_MAP["p"]:
            # TODO
            print ("Pause")

def mouse_handler(position):
    global started, game_over
    if not started or game_over:
        reset()
        started = True

def draw(canvas):
    global time, lives, score, cant_collision, rocks_number, \
        started, game_over, difficulty, seconds, scoreBonus, immortal
    # animate background
    time += 1
    wtime = (time / 4) % WIDTH
    # Background
    center = debris_info.get_center()
    size = debris_info.get_size()

    canvas.draw_image(nebula_image, nebula_info.get_center(),
                      nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                      [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2),
                      (WIDTH, HEIGHT))

    if started:
        # draw ship and sprites
        my_ship.draw(canvas)
        my_ship.update()
        process_sprite_group(rock_group, canvas)
        process_sprite_group(bonus_group, canvas)

        # Ship-Rocks Collisions
        if group_collide(rock_group, my_ship, False):
            if not immortal:
                lives -= 1
            else:
                score += 1
            rocks_number -= 1

        group_collide(bonus_group, my_ship, True)

        # game over
        if lives == -1:
            started = False
            game_over = True
            seconds = 0
            immortal = False
            scoreBonus = False
            if timer3 is not None:
                timer3.stop()
            lives = 0
            score = 0

        # Rocks-Missiles Collisions
        if missile:
            process_sprite_group(missile_group, canvas)
            cant_collision = group_group_collide(missile_group, rock_group)
            if not scoreBonus:
                score += cant_collision
            else:
                score += cant_collision * 2
            rocks_number -= cant_collision
            if cant_collision > 0 and difficulty[0] <= 1 and difficulty[1] <= 5:
                difficulty[0] += 0.1
                difficulty[1] += 0.1

        for explosion in explosion_group.copy():
            explosion.draw(canvas)
            explosion.age += 1
            if explosion.age >= 300:
                explosion_group.remove(explosion)
            explosion.update()
    else:
        if game_over:
            canvas.draw_image(gameover_image, splash_info.center, splash_info.size,
                              [WIDTH / 2, HEIGHT / 2], splash_info.size)
            soundtrack.rewind()
            my_ship.stop_ship_sound()
            explosion_sound.rewind()
            tick_tock_sound.rewind()
        else:
            canvas.draw_image(splash_image, splash_info.center, splash_info.size,
                              [WIDTH / 2, HEIGHT / 2], splash_info.size)

    # score
    canvas.draw_text("Lives", [30, 30], 30, "White", FONT)
    if lives < 2:
        canvas.draw_text(str(lives), [65, 60], 30, "Red", FONT)
    else:
        canvas.draw_text(str(lives), [65, 60], 30, "White", FONT)
    canvas.draw_text("Score", [650, 30], 30, "White", FONT)
    canvas.draw_text(str(score), [688, 60], 30, "White", FONT)

    # Bonus
    if scoreBonus:
        text = "Score time:" + str(10 - seconds)
        posX = 625
    elif immortal:
        text = "Immortal time:" + str(10 - seconds)
        posX = 600
    else:
        posX = 0
        text = ""
    canvas.draw_text(text, [posX, 580], 20, "White", FONT)


def get_data_position():
    angvel = random.choice([0.05, 0.3]) * random.random()
    vel = [random.choice(difficulty) * random.random(),
           random.choice(difficulty) * random.random()]
    pos = [random.randint(1, WIDTH), random.randint(1, HEIGHT)]
    while Utils().dist(my_ship.pos, pos) < (my_ship.get_radius() + SAFEDISTANCE):
        pos = [random.randint(1, WIDTH), random.randint(1, HEIGHT)]

    return {"angle": angvel, "position": pos, "velocity": vel}

# timer handler that spawns a rock
def rock_spawner():
    if started:
        global rock_group, rocks_number
        if rocks_number < MAX_ROCKS:
            data = get_data_position()
            rock_group.add(Sprite(data["position"], data["velocity"],
                                  0, data["angle"], asteroid_image,
                                  asteroid_info, WIDTH, HEIGHT))
            rocks_number += 1


def bonus_spawner():
    if started:
        global bonus_group, bonus_type
        if len(bonus_group) < MAX_BONUS:
            random_bonus = random.uniform(-1, 1)
            bonus = None

            if -1 <= random_bonus < -0.5 and not immortal:
                bonus = bonus_image1
                bonus_type = 1

            if -0.5 <= random_bonus < 0 and not scoreBonus:
                bonus = bonus_image2
                bonus_type = 2

            if 0 <= random_bonus < 0.5 and lives <= 4 and not immortal:
                # extra life
                bonus = bonus_image3
                bonus_type = 3

            if 0.5 <= random_bonus <= 1 and len(bonus_group) == 0 and len(rock_group) > 4:
                bonus = bonus_image4
                bonus_type = 4

            # test
            # type = 1
            if bonus is not None:
                exist = False
                for i in bonus_group:
                    if i.type == bonus_type:
                        exist = True
                        break
                if not exist:
                    data = get_data_position()
                    bonus_group.add(Bonus(data["position"], bonus_type, bonus))


# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(mouse_handler)
frame.set_keyup_handler(keyup)

timer = simplegui.create_timer(1000.0, rock_spawner)
timer2 = simplegui.create_timer(10000.0, bonus_spawner)

# get things rolling
timer.start()
timer2.start()
frame.start()
