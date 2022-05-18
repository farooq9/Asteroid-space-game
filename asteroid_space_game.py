import pygame, sys, os, random, math
from pygame.locals import *

#sounds
pygame.mixer.pre_init()
pygame.init()

#init game
pygame.init()
fps = pygame.time.Clock()

#colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

#globals
WIDTH = 1326  #800
HEIGHT = 600
time = 0

#canvas declaration
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Asteroids (Space Game)')

#load images
bg = pygame.image.load('bg.jpg')
debris = pygame.image.load('debris2_brown.png')
ship = pygame.image.load('ship.png')
ship_thrusted = pygame.image.load('ship_thrusted.png')
asteroid = pygame.image.load('asteroid.png')
shot = pygame.image.load('shot2.png')

#missile sound
missile_sound = pygame.mixer.Sound('missile.ogg')
missile_sound.set_volume(0.3)

#thrust sound
thruster_sound = pygame.mixer.Sound('thrust.ogg')
thruster_sound.set_volume(1)

#explosion sound
explosion_sound = pygame.mixer.Sound('explosion.ogg')
explosion_sound.set_volume(10)

#background music
pygame.mixer.music.load('The_Drum.mp3')  #game.ogg
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play()

#All variables
ship_x = WIDTH/2 -50
ship_y = HEIGHT/2 -50
ship_angle = 0
ship_is_rotating = False
ship_is_forward = False
ship_direction = 0
ship_speed = 0

asteroid_x = [] #random.randint(0, WIDTH)
asteroid_y = [] #random.randint(0, HEIGHT)
asteroid_angle = []
asteroid_speed = 2 # we can add random speed for the asteroids as asteroid angle
no_of_asteroids = 10

bullet_x = []
bullet_y = []
bullet_angle = []
no_of_bullets = 0

score = 0
game_over = False

for i in range(0, no_of_asteroids):
    asteroid_x.append( random.randint(0, WIDTH))
    asteroid_y.append( random.randint(0, HEIGHT))
    asteroid_angle.append( random.randint(0, 365))
    # asteroid_speed.append( random.randint(0, 365))

#rotate ship image
def rot_center(image, angle):

    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

#draw game function
def draw(canvas):
    global time, bullet_x, bullet_y
    global ship_is_forward, score
    canvas.fill(BLACK)
    canvas.blit(bg,(0,0))
    canvas.blit(debris,(time*.3,0))
    canvas.blit(debris,(time*.3-WIDTH,0))
    
    time = time + 1

    for i in range(0, no_of_bullets):
        canvas.blit(shot, (bullet_x[i], bullet_y[i]))

    for i in range(0, no_of_asteroids):
        canvas.blit( rot_center(asteroid, time), (asteroid_x[i], asteroid_y[i]))

    if ship_is_forward:
        canvas.blit(rot_center(ship_thrusted, ship_angle), (ship_x, ship_y))
    else:
        canvas.blit(rot_center(ship, ship_angle), (ship_x, ship_y))

    #draw Score
    myfont1 = pygame.font.SysFont("Comic Sans MS", 40)
    label1 = myfont1.render("Score : "+str(score), 1, (255, 255, 0))
    canvas.blit(label1, (50, 20))

    if game_over:
        myfont2 = pygame.font.SysFont("Comic Sans MS", 80)
        label2 = myfont2.render("GAME OVER ", 1, (255, 0, 40))
        canvas.blit(label2, (WIDTH/2 -230,HEIGHT/2 - 60))

        myfont3 = pygame.font.SysFont('Comic Sans MS', 40)
        label13 = myfont3.render('Total Score: '+ str(score), 1, (250, 0, 0))
        canvas.blit(label13, (520, 348))
        pygame.mixer.music.stop()

#handle input function
def handle_input():
    global ship_angle, ship_is_rotating, ship_direction
    global ship_x, ship_y, ship_speed, ship_is_forward
    global bullet_x, bullet_y, bullet_angle, no_of_bullets
    global missile_sound, thruster_sound

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:   
            if event.key == K_LEFT:
                ship_is_rotating = True
                ship_direction = 1
            elif event.key == K_RIGHT:
                ship_is_rotating = True
                ship_direction = 0
            elif event.key == K_UP:
                ship_is_forward = True
                ship_speed = 10
                thruster_sound.play()                    
            elif event.key == K_DOWN:
                ship_is_forward = False
                ship_speed = 0
            elif event.key == K_SPACE:
                bullet_x.append( ship_x + 50 )
                bullet_y.append( ship_y + 50 )
                bullet_angle.append( ship_angle )
                no_of_bullets = no_of_bullets + 1
                missile_sound.play()
            elif event.key == K_LCTRL:
                ship_is_forward = True
                ship_speed = 20                
                thruster_sound.play()
            elif event.key == K_q:
                sys.exit()

        elif event.type == KEYUP:  
            if event.key == K_LEFT or event.key == K_RIGHT:
                ship_is_rotating = False
            else:
                ship_is_forward = False
                thruster_sound.stop()
            if event.key == K_SPACE:  #my code to run ship continuesly even after pressing space
                ship_is_forward = True
            

    if ship_is_rotating:
        if ship_direction == 0:
            ship_angle = ship_angle - 10
        else:
            ship_angle = ship_angle + 10

    if ship_is_forward or ship_speed > 0:
        ship_x = (ship_x + math.cos(math.radians(ship_angle))*ship_speed )
        ship_y = (ship_y + -math.sin(math.radians(ship_angle))*ship_speed )
        if ship_is_forward == False:
            ship_speed = ship_speed - 0.1 #0.5



#update screen
def update_screen():
    pygame.display.update()
    fps.tick(60)

def isCollision(enemyX, enemyY, bulletX, bulletY, dist):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)) )
    if distance < dist:
        return True
    else:
        return False
    
#game logic
def game_logic():
    global asteroid_y, bullet_x, bullet_y, no_of_bullets
    global game_over, score
    for i in range(0, no_of_bullets):
        bullet_x[i] = (bullet_x[i] + math.cos(math.radians(bullet_angle[i]))*10 )
        bullet_y[i] = (bullet_y[i] + -math.sin(math.radians(bullet_angle[i]))*10 )
   
    for i in range(0, no_of_asteroids):
        asteroid_x[i] = (asteroid_x[i] + math.cos(math.radians(asteroid_angle[i]))*asteroid_speed )
        asteroid_y[i] = (asteroid_y[i] + -math.sin(math.radians(asteroid_angle[i]))*asteroid_speed )

        if asteroid_y[i] < 0:
            asteroid_y[i] = HEIGHT
        
        if asteroid_y[i] > HEIGHT:
            asteroid_y[i] = 0

        if asteroid_x[i] < 0:
                asteroid_x[i] = WIDTH
        
        if asteroid_x[i] > WIDTH:
            asteroid_x[i] = 0

        if isCollision(ship_x, ship_y, asteroid_x[i], asteroid_y[i], 27):
            game_over = True
            print('\nGame Over\n')
            # exit()
    
    for i in range(0, no_of_bullets):
        for j in range(0, no_of_asteroids):
            if isCollision(bullet_x[i], bullet_y[i], asteroid_x[j], asteroid_y[j], 50):
                asteroid_x[j] = (random.randint(0, WIDTH) )
                asteroid_y[j] = (random.randint(0, HEIGHT) )
                asteroid_angle[j] = (random.randint(0, 365))
                explosion_sound.play()
                score = score + 1

#asteroids game loop
while True:
    draw(window)
    handle_input()
    if not game_over:
        game_logic()
    update_screen()