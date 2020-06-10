import pygame
from pygame.locals import *
from pygame import mixer
import time
import sys
pygame.mixer.init()
clock = pygame.time.Clock()
# Window Size, Player and FPS
playerImg = pygame.image.load('dino.png')
WIDTH = 1024
HEIGHT = 768
TILESIZE = 32
Velocity = 32
playerX = 64
playerY = 64
playerX_change = 0
playerY_change = 0
FPS = 20
Score = 50

# Map File
x = open('Map.txt', 'r')
x = x.read()
x = x.split('\n')
maps = []
wallcoords = []
for i in x:
    c = []
    for j in i:
        c+=j
    maps.append(c)
for x in range(len(maps)):
    for y in range(len(maps[0])):
        if maps[x][y]=='#':
            wallcoords.append((x*TILESIZE,y*TILESIZE))
        else:
            pass

# For resuming
pause = False
exiting = False
gover_sound = pygame.mixer.Sound("game over.wav")
success_sound = pygame.mixer.Sound("success.wav")

# Intialize the pygame
pygame.init()   

# create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Caption and Icon
pygame.display.set_caption("Dinoventure")
icon = pygame.image.load('dino.png')
pygame.display.set_icon(icon)

# Colors using RGB
colors={
    'white': (255,255,255), 'black': (0,0,0),
    'green': (110,180,0), 'light green': (110,220,0),
    'blue': (50,150,150), 'light blue': (80,210,180),       
    'yellow': (255,225,0), 'purple': (180,100,200),
    'red': (200,0,0), 'light red': (255,100,100),
    'orange': (255,100,0), 'light pink': (255,110,180),
    'grey': (220,240,240), 'pink': (255,60,150),
    'light orange': (250,140,10), 'light purple': (200,110,210),
    'light grey':(100, 100, 100), 'dark grey':(40, 40, 40),
    'solid green':(0,255,0), 'solid red':(255,0,0),
    'solid blue':(0,0,255)
}
########################################################################################################################################
def Wall(x,y):
    image = pygame.Surface((TILESIZE, TILESIZE))
    image.fill(colors['solid green'])
    pygame.draw.rect(screen, colors['solid green'], (y*TILESIZE,x*TILESIZE,TILESIZE, TILESIZE))

def Map():
    for x in range(0, WIDTH, TILESIZE):
        pygame.draw.line(screen, colors['light grey'], (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILESIZE):
        pygame.draw.line(screen, colors['light grey'], (0, y), (WIDTH, y))
    for x in range(len(maps)):
        for y in range(len(maps[0])):
            if maps[x][y]=='#':
                Wall(x,y)
            else:
                pass

def wallcollide(playerX, playerY, playerX_change, playerY_change):
    global maps
    xcor = playerX//TILESIZE
    ycor = playerY//TILESIZE
    if playerX_change>0:
        if maps[ycor][xcor+1]=='#':
            return True
        else:
            return False
    elif playerX_change<0:
        if maps[ycor][xcor-1]=='#':
            return True
        else:
            return False
    elif playerY_change>0:
        if maps[ycor+1][xcor]=='#':
            return True
        else:
            return False
    elif playerY_change<0:
        if maps[ycor-1][xcor]=='#':
            return True
        else:
            return False
    else:
    
        return False
    
########################################################################################################################################
def draw_text(text, size, color, surface, x, y, center):
    font = pygame.font.SysFont(None, size)
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    if center==True:
        textrect.center = (x, y)
    else:
        textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def button(msg,x,y,w,h,ic,ac,action=None):
    global pause # hard coding for pause button
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))
        # print(action)
        # if str(action) == 'paused': # Hard coding for pause button
        #     pause == True
        #     print('lol')
        #     if click[0] == 1 and action != None:
        #         print('hehe')
        #         action()
        if click[0] == 1 and action != None:
            action()         # because fn could not have been called as button fn parameter
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))

    smallText = pygame.font.SysFont(None,30)
    textSurface = smallText.render(msg, True, colors['yellow'])
    textSurf, textRect = textSurface, textSurface.get_rect()
    textRect.center = ( (x+(w//2)), (y+(h//2)) )
    screen.blit(textSurf, textRect)

# Quiting function for buttons
def quit_game():
    pygame.quit()
    sys.exit()

# Options Menu/ Pause Game
def unpause():
    global pause
    global exiting
    pygame.mixer.music.unpause()
    pause = False
    exiting = False

def paused():
    global colors
    pygame.mixer.music.pause()
    while pause:
        buttonx = 800//2
        buttony = 600//2 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        screen.fill(colors['black'])
        draw_text('Paused',50,colors['white'], screen, 800//2, 180, True)
        button('Exit',buttonx-50 , buttony-25+100, 100, 50, colors['pink'],colors['light pink'], quit_game)
        button('Main Menu',buttonx-75, buttony-25+25, 150, 50, colors['pink'],colors['light pink'], game_intro)
        button('Resume',buttonx-50, buttony-25-50, 100, 50, colors['pink'],colors['light pink'], unpause)
        
        pygame.display.update()
        clock.tick(15) 

def instructions():
    global colors
    loop = True
    while loop:
        buttonx = 800//2
        buttony = 600//2 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(colors['black'])
        draw_text('Instructions',50,colors['purple'], screen, 800//2, 50, True)
        button('Okay',680, 520, 100, 50, colors['green'],colors['light green'], game_intro)
        
        pygame.display.update()
        clock.tick(15)

def game_over():
    global colors
    loop = True
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(gover_sound)
    while loop:
        buttonx = WIDTH//2
        buttony = HEIGHT//2 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(colors['black'])
        draw_text('GAME OVER!',80,colors['red'], screen, WIDTH//2, 180, True)
        button('Exit',buttonx-50 , buttony-25+100, 100, 50, colors['orange'],colors['light orange'], quit_game)
        button('Main Menu',buttonx-75, buttony-25, 150, 50, colors['orange'],colors['light orange'], game_intro)
        
        pygame.display.update()
        clock.tick(15)

def you_win():
    global colors
    loop = True
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(success_sound)
    while loop:
        buttonx = WIDTH//2
        buttony = HEIGHT//2 
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(colors['black'])
        draw_text('YOU WIN!',80,colors['pink'], screen, WIDTH//2, 180, True)
        button('Exit',buttonx-50 , buttony-25+100, 100, 50, colors['purple'],colors['light purple'], quit_game)
        button('Main Menu',buttonx-75, buttony-25, 150, 50, colors['purple'],colors['light purple'], game_intro)
    
        pygame.display.update()
        clock.tick(15)

# Game intro screen
def game_intro():
    global colors
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(colors['black'])
        draw_text('Dinoventure', 80, colors['orange'], screen, WIDTH//2, 150, True)    
        button('New Game',WIDTH//2 - 170//2,250,170,50, colors['blue'], colors['light blue'], game)
        button('Rules and Controls',WIDTH//2 - 245//2,350,245,50,colors['blue'], colors['light blue'], instructions)
        button('Exit',WIDTH//2 - 75//2,450,75,50,colors['blue'], colors['light blue'], quit_game) 
        
        pygame.display.update()
        clock.tick(15)


def player(x,y):
    screen.blit(playerImg, (x, y))

#####################################################################################################################################
# Game Loop
def game():
    global pause
    # global exiting
    global playerX
    global playerX_change
    global playerY
    global playerY_change
    running = True

    # BackGround Sound
    pygame.mixer.music.load('background.wav')
    pygame.mixer.music.play(-1)
    while running:
        # This will delay the game the given amount of milliseconds. In our casee 0.1 seconds will be the delay
        clock.tick(FPS)

        # RGB = Red, Green, Blue
        screen.fill(colors['black'])
        Map()
        draw_text('Score:'+str(Score),TILESIZE, colors['solid blue'], screen, WIDTH//2, HEIGHT-TILESIZE//2,True)
        button('game over',100, 100, 150, 50, colors['green'],colors['light green'], game_over)
        button('you win',100, 400, 150, 50, colors['green'],colors['light green'], you_win)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # if keystroke is pressed check whether its right or left
            if event.type == pygame.KEYDOWN: #checking if any key was pressed
                if event.key == pygame.K_LEFT and playerX>=0+TILESIZE:
                    playerX_change = -Velocity
                    playerY_change = 0 # to avoid diagonal movement
                if event.key == pygame.K_RIGHT and playerX<=WIDTH-TILESIZE:
                    playerX_change = Velocity
                    playerY_change = 0 
                if event.key == pygame.K_DOWN and playerY<=HEIGHT-TILESIZE:
                    playerY_change = Velocity
                    playerX_change = 0
                if event.key == pygame.K_UP and playerY>0+TILESIZE:
                    playerY_change = -Velocity
                    playerX_change = 0
                if event.key == pygame.K_ESCAPE:
                    pause = True
                    paused()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0
                if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    playerY_change = 0
        pc = wallcollide(playerX,playerY,playerX_change,playerY_change)
        if pc==False:
            playerX += playerX_change
            playerY += playerY_change
        player(playerX, playerY)
        pygame.display.update()

game_intro()
