import pygame
import random
import serial
from objects import Road, Player, Tree, Button, \
    Obstacle, Coins, Fuel


ser = serial.Serial("COM7", 9600)
pygame.init()
SCREEN = WIDTH, HEIGHT = 432, 768
win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
info = pygame.display.Info()
width = info.current_w
height = info.current_h



lane_pos = [75, 142, 220, 300]

# COLORS **********************************************************************

WHITE = (255, 255, 255)
BLUE = (30, 144, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 20)

# FONTS ***********************************************************************

font = pygame.font.SysFont('cursive', 40)

select_car = font.render('Select Car', True, WHITE)

# IMAGES **********************************************************************

bg = pygame.image.load('Assets/bg.png')
home_img = pygame.image.load('Assets/home.png')
play_img = pygame.image.load('Assets/buttons/play.png')
tour_de_france_img = pygame.image.load('Assets/tour de france.jpg')
tour_de_france_img = pygame.transform.scale(tour_de_france_img,
                                            (WIDTH, HEIGHT))
end_img = pygame.image.load('Assets/end.jpg')
end_img = pygame.transform.scale(end_img, (WIDTH, HEIGHT))
game_over_img = pygame.image.load('Assets/game_over.png')
game_over_img = pygame.transform.scale(game_over_img, (220, 220))
coin_img = pygame.image.load('Assets/coins/1.png')
dodge_img = pygame.image.load('Assets/car_dodge.png')
loading = pygame.image.load('Assets/loading-bar.png')
loading = pygame.transform.scale(loading, (180, 66))

left_arrow = pygame.image.load('Assets/buttons/arrow.png')
right_arrow = pygame.transform.flip(left_arrow, True, False)

home_btn_img = pygame.image.load('Assets/buttons/home.png')
replay_img = pygame.image.load('Assets/buttons/replay.png')
sound_off_img = pygame.image.load("Assets/buttons/soundOff.png")
sound_on_img = pygame.image.load("Assets/buttons/soundOn.png")
bicycle1 = pygame.image.load('Assets/bicycle1.jpg')
bicycle1 = pygame.transform.scale(bicycle1, (WIDTH, HEIGHT))
bicycle2 = pygame.image.load('Assets/bicycle2.jpg')
bicycle2 = pygame.transform.scale(bicycle2, (WIDTH, HEIGHT))
bicycle3 = pygame.image.load('Assets/bicycle3.jpg')
bicycle3 = pygame.transform.scale(bicycle3, (WIDTH, HEIGHT))

cars = []

for i in range(1, 9):
    img = pygame.image.load(f'Assets/cars/{i}.png')
    img = pygame.transform.scale(img, (59, 101))
    cars.append(img)
img = pygame.image.load('Assets/cars/Picture_bike.png')
cars.append(img)

# LIST ******************************************************************
HOME_PAGE_INDEX = 0
CAR_PAGE_INDEX = 1
GAME_PAGE_INDEX = 2
OVER_PAGE_INDEX = 3
MOVE_LEFT_INDEX = 4
MOVE_RIGHT_INDEX = 5
SOUND_ON_INDEX = 6
RUNNING_INDEX = 7
boolean_page_lst = [True, False, False, False, False, False, True, True]

RIGHT = 0
LEFT = 1
left_right_bool = [False,False]

LEFT_POWER_INDEX = 0
RIGHT_POWER_INDEX = 1
PEDAL_COUNTER_INDEX = 2
COLOR_AVERAGE_INDEX = 3
left_right_power = [0,0,0,0]

CAR_TYPE_INDEX=0
COUNTER_INDEX = 1
COUNTER_CHECKER_INDEX = 2
PLAYER_INDEX = 3
COINS_INDEX=4
DODGED_INDEX=5
FUEL_INDEX = 6
ENDX_INDEX=7
ENDXX_INDEX =8
GAME_OVERY_Y_INDEX =9
GAME_OVER_COUNTER_INDEX = 10
SPEED_INDEX = 11
p = Player(100, HEIGHT - 120, 0)

objects_lst = [0,0,0,p,0,0,100,0,0.5,-50,0,10]


# BUTTONS *********************************************************************
def center(image):
    return (WIDTH // 2) - image.get_width() // 2

play_btn = Button(play_img, (100, 34), center(play_img) + 10, HEIGHT - 80)
la_btn = Button(left_arrow, (32, 42), 40, 380)
ra_btn = Button(right_arrow, (32, 42), WIDTH - 60, 380)

home_btn = Button(home_btn_img, (24, 24), WIDTH // 4 - 18, HEIGHT - 80)
replay_btn = Button(replay_img, (36, 36), WIDTH // 2 - 18, HEIGHT - 86)
sound_btn = Button(sound_on_img, (24, 24), WIDTH - WIDTH // 4 - 18,
                   HEIGHT - 80)

# SOUNDS **********************************************************************

click_fx = pygame.mixer.Sound('Sounds/click.mp3')
fuel_fx = pygame.mixer.Sound('Sounds/fuel.wav')
start_fx = pygame.mixer.Sound('Sounds/start.mp3')
restart_fx = pygame.mixer.Sound('Sounds/restart.mp3')
coin_fx = pygame.mixer.Sound('Sounds/coin.mp3')

pygame.mixer.music.load('Sounds/mixkit-tech-house-vibes-130.mp3')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.3)  ##sound here

# OBJECTS *********************************************************************
road = Road()


tree_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
fuel_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()

# VARIABLES *******************************************************************


fule_rate = .5
counter2 = 3

# FUNCTIONS *******************************************************************

# This function displays the car selection page and allows the player to choose a car.
# It takes in the positions of the player's left and right feet, a list of boolean values,
# and a list of objects as parameters.
def car_selection_page(left_foot, right_foot,boolean_lst,object_lst):
    if boolean_lst[CAR_PAGE_INDEX]:
        win.blit(select_car, (center(select_car), 230))
        win.blit(cars[object_lst[CAR_TYPE_INDEX]], (WIDTH // 2 - 30, 350))
        la_btn.draw(win)
        ra_btn.draw(win)
        play_btn.draw(win)

        if right_foot > 50 and left_foot > 50:
            boolean_lst[CAR_PAGE_INDEX] = False
            boolean_lst[GAME_PAGE_INDEX] = True
            start_fx.play()
            object_lst[PLAYER_INDEX] = Player(100, HEIGHT - 120, object_lst[CAR_TYPE_INDEX])
            object_lst[COUNTER_INDEX]= 0

        elif left_foot > 30 and left_foot % 2 == 0:
            object_lst[CAR_TYPE_INDEX] -= 1
            click_fx.play()
            if object_lst[CAR_TYPE_INDEX] < 0:
                object_lst[CAR_TYPE_INDEX] = len(cars) - 1

        elif right_foot > 30 and right_foot % 2 == 0:
            object_lst[CAR_TYPE_INDEX] += 1
            click_fx.play()
            if  object_lst[CAR_TYPE_INDEX] >= len(cars):
                object_lst[CAR_TYPE_INDEX] = 0

#This function is responsible for displaying the game over screen and handling user input.
#Moreover, we are displaying the performance during the last game (distance,number of coins...)
def game_over_page(boolean_lst, object_lst, left_right_power_lst):
    if boolean_lst[OVER_PAGE_INDEX]:
        win.blit(end_img, (object_lst[ENDX_INDEX], 0))
        object_lst[ENDX_INDEX] += object_lst[ENDXX_INDEX]
        if object_lst[ENDX_INDEX] >= 10 or object_lst[ENDX_INDEX] <= -10:
            object_lst[ENDXX_INDEX] *= -1

        win.blit(game_over_img, (center(game_over_img), object_lst[GAME_OVERY_Y_INDEX]))
        if object_lst[GAME_OVERY_Y_INDEX] < 16:
            object_lst[GAME_OVERY_Y_INDEX] += 1

        num_coin_img = font.render(f'{object_lst[COINS_INDEX]}', True, WHITE)
        num_dodge_img = font.render(f'{object_lst[DODGED_INDEX]}', True, WHITE)
        distance_img = font.render(f'Distance : {object_lst[COUNTER_INDEX]:.2f} Meters', True,
                                   WHITE)

        win.blit(coin_img, (250, 240))
        win.blit(dodge_img, (180, 280))
        win.blit(num_coin_img, (300, 250))
        win.blit(num_dodge_img, (300, 300))
        win.blit(distance_img, (center(distance_img), (500)))

        home_btn.draw(win)
        replay_btn.draw(win)

        if object_lst[GAME_OVER_COUNTER_INDEX] < 20:
            object_lst[GAME_OVER_COUNTER_INDEX]+= 1
            return

        # restart the game
        if left_right_power_lst[RIGHT_POWER_INDEX] > 50 and left_right_power_lst[LEFT_POWER_INDEX] > 50:
            boolean_lst[OVER_PAGE_INDEX] = False
            boolean_lst[GAME_PAGE_INDEX] = True
            object_lst[COINS_INDEX] = 0
            object_lst[DODGED_INDEX] = 0
            object_lst[COUNTER_INDEX] = 0
            object_lst[FUEL_INDEX]= 100
            object_lst[ENDX_INDEX]=0
            object_lst[ENDXX_INDEX]=0.5
            object_lst[GAME_OVERY_Y_INDEX]=-50
            restart_fx.play()

        # select car again
        elif left_right_power_lst[LEFT_POWER_INDEX] > 30 and left_right_power_lst[LEFT_POWER_INDEX] % 2 == 0:
            boolean_lst[OVER_PAGE_INDEX] = False
            boolean_lst[CAR_PAGE_INDEX] = True
            object_lst[COINS_INDEX] = 0
            object_lst[DODGED_INDEX] = 0
            object_lst[COUNTER_INDEX] = 0
            object_lst[FUEL_INDEX] = 100
            object_lst[ENDX_INDEX] = 0
            object_lst[ENDXX_INDEX] = 0.5
            object_lst[GAME_OVERY_Y_INDEX] = -50

        elif sound_btn.draw(win):
            sound_on = boolean_lst[SOUND_ON_INDEX]

            if sound_on:
                sound_btn.update_image(sound_on_img)
                pygame.mixer.music.play(loops=-1)
            else:
                sound_btn.update_image(sound_off_img)
                pygame.mixer.music.stop()

#This function updates the game page and manages the game mechanics such as obstacle spawning, player movement,
#fuel consumption, collision detection, and game over conditions. It takes in the boolean list, object list, and
#left_right_power_lst as arguments. The function blits the background image, updates and draws the road, trees,
#obstacles, coins, fuel tanks, and player. It also displays the fuel bar, updates the fuel level and checks if the
#game is over due to fuel depletion or collision. If the game is over, it empties all the groups and sets the game
#over boolean to True.
def update_game_page(boolean_lst, object_lst, left_right_power_lst):
    if boolean_lst[GAME_PAGE_INDEX]:
        win.blit(bg, (0, 0))
        road.update(object_lst[SPEED_INDEX])
        road.draw(win)
        if object_lst[SPEED_INDEX] > 1:
            object_lst[COUNTER_INDEX]+= 1
        if object_lst[COUNTER_INDEX] % 20 == 0:
            tree = Tree(random.choice([-5, WIDTH - 35]), -20)
            tree_group.add(tree)

        manage_obstacles(object_lst)

        obstacle_group.update(object_lst[SPEED_INDEX])
        obstacle_group.draw(win)
        tree_group.update(object_lst[SPEED_INDEX])
        tree_group.draw(win)
        coin_group.update(object_lst[SPEED_INDEX])
        coin_group.draw(win)
        fuel_group.update(object_lst[SPEED_INDEX], left_right_power_lst[COLOR_AVERAGE_INDEX])
        fuel_group.draw(win)
        p.draw(win)

        if object_lst[FUEL_INDEX] > 0:
            pygame.draw.rect(win, GREEN, (20, 20, object_lst[FUEL_INDEX], 15), border_radius=5)
        else:
            pygame.draw.rect(win, RED, p.rect, 1)
            object_lst[SPEED_INDEX] = 1
            boolean_lst[GAME_PAGE_INDEX] = False
            boolean_lst[OVER_PAGE_INDEX] = True

            tree_group.empty()
            coin_group.empty()
            fuel_group.empty()
            obstacle_group.empty()

        pygame.draw.rect(win, WHITE, (20, 20, 100, 15), 2, border_radius=5)
        if object_lst[SPEED_INDEX] > 1:
            object_lst[FUEL_INDEX] -= fule_rate

        # COLLISION DETECTION & KILLS
        collision_detection_and_kills(boolean_lst,object_lst)

#This function manages the appearance of obstacles, coins, and fuel on the game screen.
#All the obstacles are added randomly to the game
#It is called within the update_game_page() function.
def manage_obstacles(lst_object):
    if lst_object[COUNTER_INDEX] % 30 == 0:
        type = random.choices([1, 2], weights=[1, 3], k=1)[0]
        x = random.choice(lane_pos) + 10
        if type == 1:
            lst_object[COUNTER_INDEX]  += 1
            count = random.randint(1, 3)
            for i in range(count):
                coin = Coins(x, -100 - (25 * i))
                coin_group.add(coin)
        elif type == 2:
            lst_object[COUNTER_INDEX] += 1
            fuel = Fuel(x, -100)
            fuel_group.add(fuel)
    elif lst_object[COUNTER_INDEX]  % 20 == 0 and lst_object[SPEED_INDEX]  != 1:
        obs = random.choices([1, 2, 3], weights=[6, 3, 3], k=1)[0]
        obstacle = Obstacle(obs)
        obstacle_group.add(obstacle)

#This function is responsible for collision detection between the player and all the possible obstacles/coins/fuel
#If the player collides with an obstacle, the game over screen is triggered and all groups are emptied
#If the player collides with a coin, the coin is removed from the group and the coin count is incremented
#If the player collides with fuel, the fuel is removed from the group, fuel sound is played, and fuel level is incremented
def collision_detection_and_kills(boolean_lst,lst_object):
    for obstacle in obstacle_group:
        if obstacle.rect.y >= HEIGHT:
            if obstacle.type == 1:
                lst_object[DODGED_INDEX] += 1
            obstacle.kill()

        if pygame.sprite.collide_mask(p, obstacle):
            pygame.draw.rect(win, RED, p.rect, 1)
            lst_object[SPEED_INDEX] = 1

            boolean_lst[GAME_PAGE_INDEX] = False
            boolean_lst[OVER_PAGE_INDEX] = True

            tree_group.empty()
            coin_group.empty()
            fuel_group.empty()
            obstacle_group.empty()
    if pygame.sprite.spritecollide(p, coin_group, True):
        lst_object[COINS_INDEX] += 1
        coin_fx.play()
    if pygame.sprite.spritecollide(p, fuel_group, True):
        lst_object[FUEL_INDEX] += Fuel.getVal(fuel_group)
        fuel_fx.play()
        if lst_object[FUEL_INDEX] >= 100:
            lst_object[FUEL_INDEX] = 100

#This function displays the home page of the game with a background image and a loading image.
#It also updates the counter of the list of objects.
#Once the counter reaches 100, it switches to the car selection page.
def game_home_page(boolean_lst,lst_object):
    if boolean_lst[HOME_PAGE_INDEX]:
        win.blit(bicycle2, (0, 0))
        win.blit(loading, (220, 20))
        lst_object[COUNTER_INDEX]+=1
        if lst_object[COUNTER_INDEX] % 100 == 0:
            boolean_lst[HOME_PAGE_INDEX]= False
            boolean_lst[CAR_PAGE_INDEX] = True

#This function calculates the speed of the player based on the power of the pedals.
#If the total power is less than 30 or the pedal counter is 0, the player moves at a speed of 1.
#If the power on the left pedal is greater than the power on the right pedal and is greater than 100, the player moves left at a speed of 10.
#If the power on the right pedal is greater than the power on the left pedal and is greater than 100, the player moves right at a speed of 10.
#If the power on both pedals is equal or less than 100, the player moves at a speed of 1.
def speed_calculator(left_right_bool, lst_object, left_right_power_lst):
    if left_right_power_lst[RIGHT_POWER_INDEX] + left_right_power_lst[LEFT_POWER_INDEX] < 30 or left_right_power_lst[PEDAL_COUNTER_INDEX] == 0:
        lst_object[SPEED_INDEX]= 1
        road.update(lst_object[SPEED_INDEX])
        p.update(False, False, left_right_power_lst[LEFT_POWER_INDEX], left_right_power_lst[RIGHT_POWER_INDEX])

    elif left_right_power_lst[LEFT_POWER_INDEX] > left_right_power_lst[RIGHT_POWER_INDEX] and left_right_power_lst[LEFT_POWER_INDEX] > 100:
        left_right_bool[LEFT]= True
        left_right_bool[RIGHT] = False
        p.update(left_right_bool[LEFT], left_right_bool[RIGHT], left_right_power_lst[LEFT_POWER_INDEX], left_right_power_lst[RIGHT_POWER_INDEX])
    elif left_right_power_lst[LEFT_POWER_INDEX] <= left_right_power_lst[RIGHT_POWER_INDEX] and left_right_power_lst[RIGHT_POWER_INDEX] > 100:
        left_right_bool[LEFT] = False
        left_right_bool[RIGHT] = True
        p.update(left_right_bool[LEFT], left_right_bool[RIGHT], left_right_power_lst[LEFT_POWER_INDEX], left_right_power_lst[RIGHT_POWER_INDEX])
        lst_object[SPEED_INDEX] = 10
        road.update(lst_object[SPEED_INDEX])
    else:
        left_right_bool[LEFT] = False
        left_right_bool[RIGHT] = False
        p.update(left_right_bool[LEFT], left_right_bool[RIGHT], left_right_power_lst[LEFT_POWER_INDEX], left_right_power_lst[RIGHT_POWER_INDEX])
        lst_object[SPEED_INDEX] = 10
        road.update(lst_object[SPEED_INDEX])

# This function is the main game loop that controls the flow of the game. It receives several parameters,
# including a list of boolean values, a boolean indicating whether the car should move left or right,
# a counter for the pedal cycles, a list of game objects, and a list of power values for the left and right motors.
# It runs a while loop until the boolean value at index RUNNING_INDEX is False, which is set by the user to exit the game.
# Within the loop, it checks for incoming serial data, updates game objects and power values, and handles various game pages
# such as the home screen, car selection screen, and game over screen. It also updates the game display and
# keeps track of the frame rate using Pygame functions.
def play(boolean_lst, left_right_bool, counter2, lst_object, left_right_power_lst):
    counter_checker=0
    while boolean_lst[RUNNING_INDEX]:
        counter_checker += 1
        if ser.in_waiting > 0:
            if counter2 < 0:
                line = ser.readline().decode('utf-8').rstrip()  # decode the bytes from the serial connection and remove any trailing whitespace
                line2 = line.split(',')

                left_right_power_lst[COLOR_AVERAGE_INDEX] = int(line2[11].split(' ')[-1])
                left_right_power_lst[LEFT_POWER_INDEX] = int(line2[12].split(' ')[-1])
                left_right_power_lst[RIGHT_POWER_INDEX]  = int(line2[13].split(' ')[-1])
                left_right_power_lst[PEDAL_COUNTER_INDEX] = int(line2[14].split(' ')[-1])


            else:
                counter2 -= 1
        win.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                boolean_lst[RUNNING_INDEX] = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    boolean_lst[RUNNING_INDEX] = False
        speed_calculator(left_right_bool, lst_object, left_right_power_lst)
        game_home_page(boolean_lst,lst_object)
        car_selection_page(left_right_power_lst[LEFT_POWER_INDEX], left_right_power_lst[RIGHT_POWER_INDEX], boolean_lst, lst_object)
        game_over_page(boolean_lst, lst_object, left_right_power_lst)
        update_game_page(boolean_lst,lst_object,left_right_power)
        pygame.draw.rect(win, BLUE, (0, 0, WIDTH, HEIGHT), 3)
        pygame.display.update()

play(boolean_page_lst,left_right_bool,counter2,objects_lst,left_right_power)
pygame.quit()
