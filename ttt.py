import turtle
import random
import asyncio



tur = turtle.Turtle()
tur.color('black')
tur.speed(0)
tur.hideturtle()
tur.up()
def drawboard(game):
    tur.color('black')
    tur.width(1)
    for i in range(game.x-1):
        drawline([-game.size*game.y/2,game.size*game.x/2-(i+1)*game.size],[game.size*game.y/2,game.size*game.x/2-(i+1)*game.size])
    for i in range(game.y-1):
        drawline([game.size*game.y/2-(i+1)*game.size,-game.size*game.x/2],[game.size*game.y/2-(i+1)*game.size,game.size*game.x/2])

def getlocation(game,x,y):
    return [-game.y*game.size/2-game.size/2+game.size*(y),game.x*game.size/2-game.size*0.5-game.size*(x-1)]

def drawline(a,b):
    tur.goto(a)
    tur.down()
    tur.goto(b)
    tur.up()
    
def drawshape(game,x,y):
    if game.turn=="o":
        tur.color('red')
        tur.goto(-game.y*game.size/2-game.size/2+game.size*(y),game.x*game.size/2-game.size*0.9-game.size*(x-1))
        tur.down()
        tur.circle(game.size*0.4)
        tur.up()
    else:
        tur.color('blue')
        tur.goto(-game.y*game.size/2+game.size*0.1+game.size*(y-1),game.x*game.size/2-game.size*0.1-game.size*(x-1))
        tur.down()
        tur.goto(-game.y*game.size/2+game.size*0.9+game.size*(y-1),game.x*game.size/2-game.size*0.9-game.size*(x-1))
        tur.up()
        tur.goto(-game.y*game.size/2+game.size*0.1+game.size*(y-1),game.x*game.size/2-game.size*0.9-game.size*(x-1))
        tur.down()
        tur.goto(-game.y*game.size/2+game.size*0.9+game.size*(y-1),game.x*game.size/2-game.size*0.1-game.size*(x-1))
        tur.up()

class game():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.size = 50
        self.board = [["0" for a in range(y)] for b in range(x)]
        self.player1="o"
        self.player2="x"
        self.turn="o"
        self.end=False
        self.connect = 3
        self.winner=""
        self.round=0
        drawboard(self)

def printboard(game):
    for x in range(game.x):
        print(game.board[x])

def move(game,x,y):
    if game.board[x-1][y-1]=="0":
        game.board[x-1][y-1]=game.turn    
        drawshape(game,x,y)
        game.end = check(game,x,y)
        if game.end == True:
            game.winner=game.turn
            # print([x,y])
        if game.turn=="o":
            game.turn="x"
        else:
            game.turn="o"
        # printboard(game)
        
def check(game,x,y):
    top=[-1,0]
    bot=[1,0]
    left=[0,-1]
    right=[0,1]
    topleft=[-1,-1]
    botright=[1,1]
    topright=[-1,1]
    botleft=[1,-1]
    connected=1
    coun=0
    direct=[top,bot,left,right,topleft,botright,topright,botleft]
    for i in direct:
        t = 1
        try:
            while game.board[x-1+i[0]*t][y-1+i[1]*t] == game.turn and 0 <= x-1+i[0]*t<=game.x and 0 <= y-1+i[1]*t<=game.y:
                connected=connected+1
                t=t+1
        except:
            t=t
        coun=coun+1
        
        if coun == 2:
            if connected >= game.connect:
                # print(connected)
                tur.color("purple")
                tur.width(15)
                drawline(getlocation(game,x-1+i[0]*(t-1)+1,y-1+i[1]*(t-1)+1),getlocation(game,x-1+ i[0]*(t-connected)+1 ,y-1+ i[1]*(t-connected)+1) )
                return True  
            coun = 0
            # print(connected)
            connected=1
    return False  

def ranbot(game,turn):
    while game.turn == turn:
        botx=random.randint(1,game.x)
        boty=random.randint(1,game.y)
        move(game,botx,boty)
    # print([botx,boty])


async def main():
    ranboard=[random.randint(4,10),random.randint(4,10)]
    game1 = game(ranboard[0],ranboard[1])
    game1.connect = 4
    # game1 = game(3,7)
    # game1.connect = 2
    while game1.end == False and game1.round<game1.x*game1.y:
        
        if game1.turn=="o":
            # i=input()
            # x = int(i.split()[0])
            # y = int(i.split()[1])
            # move(game1,x,y)
            ranbot(game1,game1.turn)
        elif game1.turn=="x":ranbot(game1,game1.turn)
        game1.round=game1.round+1
    
    # print(game1.winner," win")
    if game1.winner== "o":
        global owin
        owin=owin+1
    elif game1.winner== "x":
        global xwin
        xwin=xwin+1
    else:
        global draw
        draw=draw+1
    await asyncio.sleep(3)
    tur.clear()
owin = 0 
xwin = 0
draw = 0
while True:

    asyncio.run(main())
    
    print("o had won ",owin," times, x had won ",xwin,"times.",draw," draws!")
