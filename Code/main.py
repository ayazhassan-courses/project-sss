import pygame,time,sys,random
from pygame.locals import *
from pygame import mixer
from tkinter import *
import tkinter.font as font
import tkinter.messagebox

pygame.mixer.init()
clock = pygame.time.Clock()


# Window Size, Player and FPS
playerImg = pygame.image.load('dino.png')
policeload = pygame.image.load('police.png')
policeImg = pygame.transform.scale(policeload, (32, 32))
WIDTH = 1024
HEIGHT = 768
TILESIZE = 32
Velocity = 32
playerX = 5*32
playerY = 5*32
playerX_change = 0
playerY_change = 0
# Police Settings
policeX = 64
policeY = 96 
counter = 0
##################
FPS = 20
Score = 50
riddleNum = 0
Answer = ''

def player(x,y):
    screen.blit(playerImg, (x, y))

def police(x,y):
    screen.blit(policeImg, (x, y))

# Map File
x = open('Map.txt', 'r')
x = x.read()
x = x.split('\n')
maps = []
nodes = {}
# Making a graph
for i in x:
    c = []
    for j in i:
        c+=j
    maps.append(c)

for y in range(len(maps)):
    for x in range(len(maps[0])):
        if maps[y][x]=='.' or maps[y][x]=='@':
            nodes[(x,y)]=[]
        else:
            pass
for y in range(len(maps)):
    for x in range(len(maps[0])):
        if maps[y][x]=='.' or maps[y][x]=='@':
            if maps[y][x+1]=='.' or maps[y][x+1]=='@':
                nodes[(x,y)]=nodes.get((x,y))+[(x+1,y,1)]
                nodes[(x+1,y)]=nodes.get((x+1,y))+[(x,y,1)]
            if maps[y+1][x]=='.' or maps[y+1][x]=='@':
                nodes[(x,y)]=nodes.get((x,y))+[(x,y+1,1)]
                nodes[(x,y+1)]=nodes.get((x,y+1))+[(x,y,1)]
# print(nodes)

def reset():
    global policeX, policeY, playerX, playerY, playerX_change, playerY_change
    policeX = 64
    policeY = 96 
    playerX = 5*32
    playerY = 5*32
    playerX_change = 0
    playerY_change = 0
def Enqueue(Q,item):
    Q.append(item)

def Dequeue(Q):
    return Q.pop(0)

def is_empty(lst):
    return len(lst)==0

def Dijkstra(G,s):
    dist = {}
    for i in G:
        dist[i]= ['',9999]
    dist[s]=[s,0]
    q = []
    visited = []
    Enqueue(q,s)
    while is_empty(q)==False:
        u = Dequeue(q)
        for i in G[u]:
            if dist[u][-1]+i[-1]<dist[i[:2]][-1] and u not in visited:
                dist[i[:2]][-1]= dist[u][-1]+i[-1]
                dist[i[:2]][0] = u
                Enqueue(q,i[:2])
        visited.append(u)
    return dist

def findshortestpath(nodes, policeX, policeY, playerX, playerY):
    polxcor = policeX//TILESIZE
    polycor = policeY//TILESIZE
    chrxcor = playerX//TILESIZE
    chrycor = playerY//TILESIZE
    path = Dijkstra(nodes,(polxcor,polycor))
    to = (chrxcor,chrycor)
    lst = []
    frm = (polxcor,polycor)
    while to != frm:
        lst.append((path[to][0],to,path[to][1]))
        to = path[to][0]
    return lst[::-1]

def translator(path):
    commands = []
    for i in path:
        frm = i[0]
        to = i[1]
        if (frm[0]+1,frm[1])==to:
            commands.append('Right')
        elif (frm[0]-1,frm[1])==to:
            commands.append('Left')
        elif (frm[0],frm[1]+1)==to:
            commands.append('Down')
        elif (frm[0],frm[1]-1)==to:
            commands.append('Up')
    return commands

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
    'yellow': (255,225,0), 'purple': (140,50,225),
    'red': (200,0,0), 'light red': (255,100,100),
    'orange': (255,100,0), 'light pink': (255,110,180),
    'grey': (220,240,240), 'pink': (255,60,150),
    'light orange': (250,140,10), 'light purple': (180,100,210),
    'light grey':(100, 100, 100), 'dark grey':(40, 40, 40),
    'solid green':(0,255,0), 'solid red':(255,0,0),
    'solid blue':(0,0,255)
}

########################################################################################################################################

RiddleQ = {
    "Cash me outside, how about that?": 'bank', 
    "No man's land.": "female lounge" , 
    "Nahi parha mene pura saal, ab kia hoga mera haal?\nA ayega B ayega kis ko hai mera ehsas?":"ehsas",
	"You might think there are swings and slides in this space\nBut in Habib that is not the case": 'playground',
	"Long ago, the four nations lived together in harmony.\nThen everything changed...":'fire courtyard',
	"Yahan pe loug umedein le kar aate hain,\nPaise de kar udhar bojh uthane jaate hain,\nAj ko jitna bhari bojh uthaoge,\nKal ko utna he meetha phal khaoge": 'gym',
	"Where water runs but doesn't flow,\nwhere life is still but always grows,\nif you're too close to central street,\nwalking here is quite a feat!": 'zen garden',
	"You may be tired, do your joints ache?\nBy now, your lungs will be out of air,\nyour next clue lies where you least surmise,\nyou fill your lungs with something else there": 'baithak',
    "A pile of words \n Jackets of hordes \n Take a quick look \n In the place of the book": "library",
    "To solve this little fix \n Liquids, solids, gases mix \n Head to the place of some reaction \n To further this puzzle transaction": "lab",
    "Walk or run but just don't stumble \n to where we cure our belly's rumble": "cafeteria",
    "A site of work and getting things done \n Of piles of paper and not much fun \n In the clash of desk and of chair \n You will have to go there": "academic block"
    }
RiddleA = {
    'bank':"Cash me outside, how about that?", 
    'female lounge':"No man's land", 
    'ehsas':"Nahi parha mene pura saal, ab kia hoga mera haal?\nA ayega B ayega kis ko hai mera ehsas?", 
    'playground':"You might think there are swings and slides in this space\nBut in Habib that is not the case", 
    'fire courtyard':"Long ago, the four nations lived together in harmony.\nThen everything changed...", 
    'gym':"Yahan pe loug umedein le kar aate hain,\nPaise de kar udhar bojh uthane jaate hain,\nAj ko jitna bhari bojh uthaoge,\nKal ko utna he meetha phal khaoge", 
    'zen garden':"Where water runs but doesn't flow,\nwhere life is still but always grows,\nif you're too close to central street,\nwalking here is quite a feat!",  
    'baithak':"You may be tired,\ndo your joints ache?\nBy now, your lungs will be out of air,\nyour next clue lies where you least surmise,\nyou fill your lungs with something else there", 
    'library':"A pile of words \n Jackets of hordes \n Take a quick look \n In the place of the book", 
    'lab':"To solve this little fix \n Liquids, solids, gases mix \n Head to the place of some reaction \n To further this puzzle transaction", 
    'cafeteria': "Walk or run but just don't stumble \n to where we cure our belly's rumble", 
    'academic block':"A site of work and getting things done \n Of piles of paper and not much fun \n In the clash of desk and of chair \n You will have to go there"
    }

# This will keep a log of all the locations the  
pathLog = []
# Character Coordinates
charcoords = {'academic block': (160, 32), 'playground': (382, 192), 'lab':(64, 544), 'ehsas':(800, 64), 'library':(928, 192), 'bank':(96, 192), 'playground':(384, 192), 'female lounge':(576, 288), 'fire courtyard':(64, 384), 'gym':(640, 384), 'baithak':(160, 608), 'zen garden':(640, 640), 'cafeteria': (864,448)}
# List of all 12 locations
allLocations = list(charcoords.keys())

# Randomly making a stack of 4 locations
def is_empty(stack):
    if len(stack)==0:
        return True
    else:
        return False

def push(stack,item):
    stack.append(item)

def pop(stack):
    return stack.pop()

def top(stack):
    return lst[-1]
nums = []
locations = []
while len(nums) < 4:
    x = random.randint(0,11)
    if x not in nums:
        nums.append(x)
for num in nums:
    push(locations, allLocations[num])

# Helper to check if player went to the place he was told
def playerorder(playerX, playerY):
    if (playerX,playerY) == charcoords[pathLog[-1]]:
        return True
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
        if click[0] == 1 and action != None:
            action()         # because fn could not have been called as button fn parameter
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))

    smallText = pygame.font.SysFont(None,30)
    textSurface = smallText.render(msg, True, colors['yellow'])
    textSurf, textRect = textSurface, textSurface.get_rect()
    textRect.center = ( (x+(w//2)), (y+(h//2)) )
    screen.blit(textSurf, textRect)

########################################################################################################################################
def Wall(x,y,color):
    image = pygame.Surface((TILESIZE, TILESIZE))
    image.fill(colors[color])
    pygame.draw.rect(screen, colors[color], (y*TILESIZE,x*TILESIZE,TILESIZE, TILESIZE))

def Map():
    chars= ['student1.png','student2.png','student3.png','student4.png','student5.png','student6.png','student7.png','student8.png']
    for x in range(0, WIDTH, TILESIZE):
        pygame.draw.line(screen, colors['black'], (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILESIZE):
        pygame.draw.line(screen, colors['black'], (0, y), (WIDTH, y))
    count = 0
    for x in range(len(maps)):
        for y in range(len(maps[0])):
            if maps[x][y]=='#':
                Wall(x,y,'green')
            elif maps[x][y]=='!':
                Wall(x,y,'pink')
            elif maps[x][y]=='$':
                Wall(x,y,'blue')       
            elif maps[x][y]=='%':
                Wall(x,y,'orange')
            elif maps[x][y]=='-':
                Wall(x,y,'purple')
            elif maps[x][y]=='+':
                Wall(x,y,'light grey')
            elif maps[x][y]=='@':
                if count >= 8:
                    count = 0
                load1 = pygame.image.load(chars[count])
                count += 1
                playerImg1 = pygame.transform.scale(load1, (32, 36))
                screen.blit(playerImg1, (y*TILESIZE, x*TILESIZE))
            else:
                pass

def wallcollide(playerX, playerY, playerX_change, playerY_change):
    global maps
    wallChars = '-+!$%#'
    xcor = playerX//TILESIZE
    ycor = playerY//TILESIZE
    if playerX_change>0:   
        if maps[ycor][xcor+1] in wallChars:
            return True
        else:
            return False
    elif playerX_change<0:
        if maps[ycor][xcor-1] in wallChars:
            return True
        else:
            return False
    elif playerY_change>0:
        if maps[ycor+1][xcor] in wallChars:
            return True
        else:
            return False
    elif playerY_change<0:
        if maps[ycor-1][xcor] in wallChars:
            return True
        else:
            return False
    else:
    
        return False

def playerInteraction(playerX, playerY):
    global maps
    xcor = playerX//TILESIZE
    ycor = playerY//TILESIZE
    if maps[ycor][xcor] == '@':
        return True
    else:
        return False

def placesText():
    draw_text('Ehsas', 27, colors['white'], screen, 880, 110, True)
    draw_text('Reception', 27, colors['white'], screen, 605, 100, True)
    draw_text('Academic', 25, colors['white'], screen, 175, 95, True)    
    draw_text('Block', 24, colors['white'], screen, 175, 115, True)
    draw_text('Bank', 25, colors['white'], screen, 175, 207, True)
    draw_text('Fire', 25, colors['white'], screen, 140, 370, True)
    draw_text('Courtyard', 25, colors['white'], screen, 145, 395, True)
    draw_text('Playground', 30, colors['white'], screen, 508, 223, True)
    draw_text('Female Lounge', 30, colors['white'], screen, 430, 320, True)
    draw_text('Gym', 35, colors['white'], screen, 460, 415, True)
    draw_text('Library', 38, colors['white'], screen, 812, 240, True)
    draw_text('Cafe2go', 25, colors['white'], screen, 880, 350, True)
    draw_text('Cafeteria', 25, colors['white'], screen, 910, 520, True)
    draw_text('Classroom', 30, colors['white'], screen, 688, 545, True)
    draw_text('Zen Garden', 31, colors['white'], screen, 803, 657, True)
    draw_text('Court', 30, colors['white'], screen, 270, 595, True)
    draw_text('Court', 30, colors['white'], screen, 430, 595, True)
    draw_text('Baithak', 22, colors['white'], screen, 129, 640, True)
    draw_text('Lab', 25, colors['white'], screen, 128, 542, True)
    draw_text('Auditorium', 25, colors['white'], screen, 399, 109, True)
    
########################################################################################################################################
def tkinternext():
    root = Tk()
    root.resizable(0,0)
    frame = Frame(root,padx=10,pady=10)
    frame.pack(padx=25,pady=25)
    root.configure(bg='coral2')
    myFont = font.Font(family='Fixedsys', size=12, weight='bold')
    def evaluate(event):
        root.destroy()  
    Label1 = Label(frame, text="Next go to "+str(pathLog[-1]))
    Label1.grid(row=0,column=0)
    Label1['font'] = myFont

    root.bind_all("<Return>",evaluate)

    Evaluate = Button(frame,text="Okay",height=1,width=5,bd=1,command=lambda:evaluate(True),bg='brown2',  activebackground='brown2', fg='gold', border=3)
    Evaluate.grid(row=2,column=2)

    root.mainloop()   

def tkintercorrect():
    root = Tk()
    root.resizable(0,0)
    frame = Frame(root,padx=10,pady=10)
    frame.pack(padx=25,pady=25)
    root.configure(bg='forest green')
    myFont = font.Font(family='Fixedsys', size=12, weight='bold')
    def evaluate(event):
        root.destroy()  
    Label1 = Label(frame, text="Congrats! That is correct answer! 10+ Score")
    Label1.grid(row=0,column=0)
    Label1['font'] = myFont

    root.bind_all("<Return>",evaluate)

    Evaluate = Button(frame,text="Okay",height=1,width=5,bd=1,command=lambda:evaluate(True),bg='brown2',activebackground='brown2', fg='gold', border=3)
    Evaluate.grid(row=5,column=5)

    root.mainloop()   

def tkinterwrong(x):
    root = Tk()
    root.resizable(0,0)
    frame = Frame(root,padx=10,pady=10)
    frame.pack(padx=25,pady=25)
    root.configure(bg='red2')
    myFont = font.Font(family='Fixedsys', size=12, weight='bold')
    def evaluate(event):
        root.destroy()  
    Label1 = Label(frame, text="Uh Ohh!! The correct answer is "+str(x.lower()))
    Label1.grid(row=0,column=0)
    Label1['font'] = myFont

    root.bind_all("<Return>",evaluate)

    Evaluate = Button(frame,text="Okay",height=1,width=5,bd=1,command=lambda:evaluate(True),bg='brown2',  activebackground='brown2', fg='gold', border=3)
    Evaluate.grid(row=2,column=2)

    root.mainloop()

def tkintererror():
    global Answer
    root = Tk()
    root.resizable(0,0)
    frame = Frame(root,padx=10,pady=10)
    frame.pack(padx=25,pady=25)
    root.configure(bg='firebrick3')
    myFont = font.Font(family='Fixedsys', size=12, weight='bold')
    def evaluate(event):
        root.destroy()
    Label1 = Label(frame, text="You must go to the right person!")
    Label1.grid(row=0,column=0)
    Label1['font'] = myFont

    root.bind_all("<Return>",evaluate)

    Evaluate = Button(frame,text="Okay",height=1,width=5,bd=1,command=lambda:evaluate(True),bg='brown2',  activebackground='brown2', fg='gold', border=3)
    Evaluate.grid(row=2,column=2)

    root.mainloop()

def tkinterfunction():
    global locations
    global pathLog
    root = Tk(className='Riddle') #initializing with title name
    root.resizable(0,0) #make window resizable
    frame = Frame(root,padx=10,pady=10)
    frame.pack(padx=25,pady=25)
    root.configure(bg='DeepSkyBlue4')
    myFont = font.Font(family='Fixedsys', size=12, weight='bold')
    def evaluate(event):
        global Answer
        x = entry.get()
        x = x.lower()
        Answer = x
        root.destroy()
    a = pop(locations)
    pathLog.append(a)
    Label1 = Label(frame, text=RiddleA[a])
    Label1.grid(row=0,column=0)
    Label1['font'] = myFont

    entry = Entry(frame,text="Enter Answer",bg='grey75', border=3)# Make a text input box\ Entry box
    entry.grid(row=1,column=2)  

    root.bind_all("<Return>",evaluate)

    Evaluate = Button(frame,text="Check",height=1,width=5,bd=1,command=lambda:evaluate(True),bg='brown2',  activebackground='brown2', fg='gold', border=3 )
    Evaluate.grid(row=2,column=2)

    root.mainloop()
##########################################################################################################################################
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        screen.fill(colors['black'])
        draw_text('Paused',50,colors['white'], screen, WIDTH//2, 180, True)
        button('Exit',WIDTH//2-50 , 600//2-25+100, 100, 50, colors['pink'],colors['light pink'], quit_game)
        button('Main Menu',WIDTH//2-75, 600//2-25+25, 150, 50, colors['pink'],colors['light pink'], game_intro)
        button('Resume',WIDTH//2-50, 600//2-25-50, 100, 50, colors['pink'],colors['light pink'], unpause)
        
        pygame.display.update()
        clock.tick(15) 

def game_over():
    global colors
    loop = True
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(gover_sound)
    reset()
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(colors['black'])
        draw_text('GAME OVER!',80,colors['red'], screen, WIDTH//2, 180, True)
        button('Exit',WIDTH//2-50 , HEIGHT//2-45, 100, 50, colors['orange'],colors['light orange'], quit_game)
        button('Main Menu',WIDTH//2-75, HEIGHT//2-130, 150, 50, colors['orange'],colors['light orange'], game_intro)
        
        pygame.display.update()
        clock.tick(15)

def you_win():
    global colors
    reset()
    loop = True
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(success_sound)
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(colors['black'])
        draw_text('Congratulations, you helped Dino find his friend!',45,colors['pink'], screen, WIDTH//2, 150, True)
        draw_text('YOU WIN!',80,colors['pink'], screen, WIDTH//2, 220, True)
        button('Exit',WIDTH//2-50 , HEIGHT//2-20, 100, 50, colors['purple'],colors['light purple'], quit_game)
        button('Main Menu',WIDTH//2-75, HEIGHT//2-105, 150, 50, colors['purple'],colors['light purple'], game_intro)
    
        pygame.display.update()
        clock.tick(15)

def instructions():
    global colors
    loop = True
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(colors['black'])
        draw_text('Instructions',50,colors['purple'], screen, WIDTH//2, 50, True)
        draw_text('• You are given 20 points initially.',25,colors['light blue'],screen,260,114,True)
        draw_text('• There are 3 destinations that Dino must visit (i.e 3 riddles).',25,colors['light blue'],screen,370,144,True)
        draw_text('• Upon reaching each destination, a new riddle will pop up.',25,colors['light blue'],screen,361,174,True)
        draw_text('• Solve each riddle correctly to know where to go next.',25,colors['light blue'],screen,343,204,True)
        draw_text('• Use the up,down,left,right keys in order to move Dino in the respective directions.',25,colors['light blue'],screen,460,234,True)
        draw_text('• Once Dino meets his friend without being caught, you win.',25,colors['light blue'],screen,366,264,True)
        draw_text('• If Dino is caught by a security guard, you lose.',25,colors['light blue'],screen,316,294,True)
        draw_text('Rules',50,colors['purple'], screen, WIDTH//2, 350, True)
        draw_text('• Cost of one hint is: 10 points. Cost of slowing down the guards speed: 5 points.',25,colors['light blue'],screen,452,390,True)
        draw_text('• Security guards are at random places and on the watch, try to keep Dino out of their way.',25,colors['light blue'],screen,490,420,True)
        draw_text('• You will be timed! If you take too long on a riddle, the security guards can spot Dino.',25,colors['light blue'],screen,472,450,True)
        draw_text('• If any guard spots Dino, they will chase him.',25,colors['light blue'],screen,307,480,True)
        draw_text('• If time runs out while solving a riddle, a guard will automatically catch Dino.',25,colors['light blue'],screen,440,510,True)
        draw_text('• If your points run out, you have no choice but to solve riddles without a hint and keep',25,colors['light blue'],screen,475,540,True)
        draw_text('Dino out of the sight of guards but the game will continue.',25,colors['light blue'],screen,368,570,True)

        button('Main Menu',720, 600, 120, 50, colors['green'],colors['light green'], game_intro)
        
        pygame.display.update()
        clock.tick(15)

def story():
    global colors
    loop = True
    while loop: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(colors['black'])
        draw_text('Background Story',50,colors['light red'], screen, WIDTH//2, 70, True)
        draw_text('A Dino had a rough day and goes out for a walk.',25,colors['white'],screen,260,144,True)
        draw_text('Lost in his thoughts, he loses track of where he is and',25,colors['white'],screen,680,144,True)
        draw_text('ends up entering Habib University.',25,colors['white'],screen,210,165,True)
        draw_text('He has entered HU accidentally and has realised that the security is tight',25,colors['white'],screen,663,165,True)
        draw_text('and anyone caught will be questioned. Dino is worried because he is unaware of ',25,colors['white'],screen,393,187,True)
        draw_text('what the security might do.',25,colors['white'],screen,835,187,True)
        draw_text('Luckily, Dino knows a student in HU and he is sure that his friend will help him escape!',25,colors['white'],screen,422,208,True)
        draw_text('However,',25,colors['white'],screen,820,208,True)
        draw_text('he doesn’t know where he is.',25,colors['white'],screen,182,228,True)
        draw_text('You are to help Dino find his friend!',30,colors['light red'],screen,515,260,True)
        draw_text('It is your responsibility to navigate Dino and help him keep out of the sight of others especially security guards.',25,colors['white'],screen,525,300,True)
        draw_text('In order to help, you will be given riddles based on the HU campus. The solution of each',25,colors['white'],screen,424,320,True)
        draw_text('riddle is the destination',25,colors['white'],screen,885,320,True)
        draw_text('you must go to where you will be given another riddle. These riddles will lead Dino to his friend who will tell him',25,colors['white'],screen,525,342,True)
        draw_text('where the exit is. Make sure to watch out for security guards!',25,colors['white'],screen,318,362,True)
        button('Main Menu',680, 520, 120, 50, colors['green'],colors['light green'], game_intro)
        
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
  
        draw_text('DINOVENTURE', 80, colors['orange'], screen, WIDTH//2, 150, True)    
        button('New Game',WIDTH//2 - 170//2,235,160,50, colors['blue'], colors['light blue'], game)
        button('Rules and Controls',WIDTH//2 - 230//2,330,220,50,colors['blue'], colors['light blue'], instructions)
        button('Story',WIDTH//2 - 75//2-2,425,75,50,colors['blue'], colors['light blue'], story)
        button('Exit',WIDTH//2 - 75//2-2,520,75,50,colors['blue'], colors['light blue'], quit_game) 
        
        pygame.display.update()
        clock.tick(15)

#####################################################################################################################################
# Game Loop
def game():
    global pause
    # global exiting
    global playerX
    global playerX_change
    global playerY
    global playerY_change
    global Score
    global riddleNum
    global policeX
    global policeY
    global counter
    running = True

    # BackGround Sound
    pygame.mixer.music.load('background.wav')
    pygame.mixer.music.play(-1)
    while running:
        # This will delay the game the given amount of milliseconds. In our casee 0.1 seconds will be the delay
        clock.tick(FPS)
        screen.fill(colors['black'])
        Map()
        
        # score 
        draw_text('Score:' + str(Score), TILESIZE, colors['black'], screen, 60, 15,True)
        placesText()
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
                if Score == 0:
                    game_over()
                if riddleNum == 4 and playerorder(playerX, playerY) == True:
                    you_win()
                if event.key == pygame.K_SPACE and playerInteraction(playerX, playerY) == True  and riddleNum == 0: 
                    tkinterfunction()
                    if Answer == pathLog[-1].lower():
                        tkintercorrect()
                        Score +=10
                        tkinternext()
                    else:
                        tkinterwrong(pathLog[-1].lower())
                        Score-=5
                    riddleNum += 1
                elif event.key == pygame.K_SPACE and playerInteraction(playerX, playerY) == True and playerorder(playerX, playerY) == True:
                    tkinterfunction()
                    if Answer == pathLog[-1].lower():
                        tkintercorrect()
                        Score += 10
                        tkinternext()
                    else:
                        tkinterwrong(pathLog[-1].lower())
                        Score-= 5
                    riddleNum += 1
                elif event.key == pygame.K_SPACE and playerInteraction(playerX, playerY) == True and playerorder(playerX, playerY) == False:
                    Score -= 5
                    tkintererror()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0
                if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    playerY_change = 0
            if (playerX,playerY) == (policeX,policeY):
                    game_over()
        pc = wallcollide(playerX,playerY,playerX_change,playerY_change)
        if pc==False:
            playerX += playerX_change
            playerY += playerY_change
        path = findshortestpath(nodes, policeX, policeY, playerX, playerY)
        command = translator(path)
        # print(command)
        if command==[]:
            game_over()
        else:
            if counter%2==0:
                counter = 0
                if command[0]=='Up':
                    policeY-=32
                elif command[0]=='Down':
                    policeY+=32
                elif command[0]=='Right':
                    policeX+=32
                elif command[0]=='Left':
                    policeX-=32
        counter = counter + 1
        player(playerX, playerY)
        police(policeX, policeY)
        pygame.display.update()

game_intro()

