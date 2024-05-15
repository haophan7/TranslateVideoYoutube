###Pacman
from tkinter import *
import random
import time
import threading
import pygame
root = Tk()

root.wm_title('Pacman')
Pycon = Image('photo', file='PacManTrial2RightOutline.png')
root.tk.call('wm','iconphoto',root._w,Pycon)
root.resizable(False, False)
Canvas_Width = 230
Canvas_height = 310
bigPelletNumList = []
newLevel = False

def UserKey(event):

    global UserDirection
    global newLevel

    if str(event.keysym) in ['Down','Right','Left','Up'] and not newLevel:

        if str(event.keysym) == 'Down':

            UserDirection = 'Down '

        elif str(event.keysym) == 'Right':

            UserDirection = str(event.keysym)

        elif str(event.keysym) == 'Left':

            UserDirection = 'Left '

        elif str(event.keysym) == 'Up':

            UserDirection = 'Up ke'

Line_Width = int(Canvas_Width / 230)

canvas = Canvas(root, width=Canvas_Width, height=Canvas_height, bg='black')
canvas.focus_set()
canvas.bind('<Key>', UserKey)
canvas.pack()
userScore = 0
key = []
ghostSpeed = 21

for bit in range(22):

    key.append(random.choice(['1','0']))

key = ''.join(key)

def HighScoreFinder():

    global originalHighScore
    global encryptedHighscore
    
    time.sleep(0.1)

    try:

        with open('HighScore.txt', 'r') as highScoreFile:

            encryptedHighscore = int(str(highScoreFile.readline()), 2)
            fileKey = int(str(highScoreFile.readline()), 2)
            originalHighScore = str(encryptedHighscore ^ fileKey)
            highScoreLabel2['text'] = originalHighScore

    except:

        with open('HighScore.txt', 'w') as highScoreFile:

            highScoreFile.write(format((0 ^ int(key, 2)), '#024b') + '\n' + key)
            originalHighScore = 0

t = threading.Thread(target=HighScoreFinder)
t.start()
freeze = False

def New_Line(x1, y1, x2, y2, WIDTH=1, FILL='blue'):
    
    canvas.create_line(x1, y1 + 10, x2, y2 + 10, width=WIDTH, fill=FILL)
    canvas.create_line(Canvas_Width - x1,y1 + 10,Canvas_Width - x2,y2 + 10, width=WIDTH, fill=FILL)

New_Line(2,25,(Canvas_Width/2)+1,25)
New_Line(2,25,2,104)
New_Line(39,104,2,104)
New_Line(39,104,39,129)
New_Line(0,129,39,129)

New_Line(6,29,(Canvas_Width/2)-4,29)
New_Line((Canvas_Width/2)-4,61,(Canvas_Width/2)-4,29)
New_Line((Canvas_Width/2)-4,61,(Canvas_Width/2)+1,61)
New_Line(6,29,6,100)
New_Line(43,100,6,100)
New_Line(43,100,43,133)
New_Line(0,133,43,133)

New_Line(0,153,39,153)
New_Line(39,153,39,178)
New_Line(2,178,39,178)
New_Line(2,178,2,274)
New_Line(2,274,(Canvas_Width/2)+1,274)
New_Line(6,270,(Canvas_Width/2)+1,270)
New_Line(6,230,6,270)
New_Line(6,230,19,230)
New_Line(19,230,19,222)
New_Line(19,222,6,222)
New_Line(6,182,6,222)
New_Line(6,182,43,182)
New_Line(43,182,43,149)
New_Line(43,149,0,149)

New_Line((Canvas_Width/2)-30,125,(Canvas_Width/2)-30,158,)
New_Line((Canvas_Width/2)-30,125,(Canvas_Width/2)-8,125)
New_Line((Canvas_Width/2)-30,158,(Canvas_Width/2)+1,158)
New_Line((Canvas_Width/2)-26,154,(Canvas_Width/2)+1,154)
New_Line((Canvas_Width/2)-26,154,(Canvas_Width/2)-26,129)
New_Line((Canvas_Width/2)-26,129,(Canvas_Width/2)-8,129)
New_Line((Canvas_Width/2)-8,129,(Canvas_Width/2)-8,125)

canvas.create_line((Canvas_Width/2)-7,137,(Canvas_Width/2)+1,137, fill='grey', width=2)
canvas.create_line((Canvas_Width/2)-7,136,(Canvas_Width/2)+1,136, fill='grey', width=2) #grey
canvas.create_line(Canvas_Width-((Canvas_Width/2)-9),137,Canvas_Width-((Canvas_Width/2)+1),137,fill='grey', width=2)
canvas.create_line(Canvas_Width-((Canvas_Width/2)-9),136,Canvas_Width-((Canvas_Width/2)+1),136,fill='grey', width=2)

New_Line((Canvas_Width/2)-4,109,(Canvas_Width/2)-4,85)
New_Line((Canvas_Width/2)-4,109,(Canvas_Width/2)+1,109)
New_Line((Canvas_Width/2)-30,85,(Canvas_Width/2)-4,85)
New_Line((Canvas_Width/2)-30,85,(Canvas_Width/2)-30,77)
New_Line((Canvas_Width/2)+1,77,(Canvas_Width/2)-30,77)

New_Line(59,61,(Canvas_Width/2)-20,61)
New_Line(59,45,(Canvas_Width/2)-20,45)
New_Line(59,45,59,61)
New_Line((Canvas_Width/2)-20,45,(Canvas_Width/2)-20,61)

New_Line(43,45,43,61)
New_Line(43,45,22,45)
New_Line(43,61,22,61)
New_Line(22,45,22,61)

New_Line(43,84,43,77)
New_Line(22,77,43,77)
New_Line(22,84,43,84)
New_Line(22,84,22,77)

New_Line(59,77,(Canvas_Width/2)-46,77)
New_Line(59,77,59,133)
New_Line(59,133,(Canvas_Width/2)-46,133)
New_Line((Canvas_Width/2)-20,109,(Canvas_Width/2)-46,109)
New_Line((Canvas_Width/2)-20,101,(Canvas_Width/2)-20,109)
New_Line((Canvas_Width/2)-20,101,(Canvas_Width/2)-46,101)
New_Line((Canvas_Width/2)-46,133,(Canvas_Width/2)-46,109)
New_Line((Canvas_Width/2)-46,77,(Canvas_Width/2)-46,101)

New_Line((Canvas_Width/2)-46,149,(Canvas_Width/2)-46,182)
New_Line((Canvas_Width/2)-46,149,59,149)
New_Line(59,182,59,149)
New_Line(59,182,(Canvas_Width/2)-46,182)

New_Line(43,198,43,230)
New_Line(43,198,22,198)
New_Line(22,198,22,206)
New_Line(35,206,22,206)
New_Line(35,206,35,230)
New_Line(43,230,35,230)

New_Line(22,246,22,246)
New_Line(22,246,22,254)
New_Line((Canvas_Width/2)-20,254,22,254)
New_Line((Canvas_Width/2)-20,254,(Canvas_Width/2)-20,246)
New_Line((Canvas_Width/2)-20,246,(Canvas_Width/2)-46,246)
New_Line((Canvas_Width/2)-46,222,(Canvas_Width/2)-46,246)
New_Line((Canvas_Width/2)-46,222,59,222)
New_Line(59,246,59,222)
New_Line(59,246,22,246)

New_Line((Canvas_Width/2)-20,198,59,198)
New_Line(59,198,59,206)
New_Line((Canvas_Width/2)-20,206,59,206)
New_Line((Canvas_Width/2)-20,198,(Canvas_Width/2)-20,206)

New_Line((Canvas_Width/2)-30,182,(Canvas_Width/2)-30,174)
New_Line((Canvas_Width/2)+1,174,(Canvas_Width/2)-30,174)
New_Line((Canvas_Width/2)-30,182,(Canvas_Width/2)-4,182)
New_Line((Canvas_Width/2)-4,206,(Canvas_Width/2)-4,182)
New_Line((Canvas_Width/2)-4,206,(Canvas_Width/2)+1,206)

New_Line((Canvas_Width/2)-30,230,(Canvas_Width/2)-30,222)
New_Line((Canvas_Width/2)+1,222,(Canvas_Width/2)-30,222)
New_Line((Canvas_Width/2)-30,230,(Canvas_Width/2)-4,230)
New_Line((Canvas_Width/2)-4,254,(Canvas_Width/2)-4,230)
New_Line((Canvas_Width/2)-4,254,(Canvas_Width/2)+1,254)


IMGPAC = PhotoImage(file = 'PacManTrial1.png')
PacPellet = canvas.create_image(116,224, image = IMGPAC)

life1Img = PhotoImage(file = 'PacManTrial2Left .png')
life1 = canvas.create_image(20,298, image = life1Img)

life2Img = PhotoImage(file = 'PacManTrial2Left .png')
life2 = canvas.create_image(40,298, image = life2Img)

life3Img = PhotoImage(file = 'PacManTrial2Left .png')
life3 = canvas.create_image(60,298, image = life3Img)

totalLives = 3
ghostKillCount = 0

playerLevelNumber = 1

loadingLabel = Label(canvas, text='Loading...', fg='white', bg='black', font='Helvetica 10 bold italic')
levelLabel1 = Label(canvas, text='Level:', fg='white', bg='black', font='Helvetica 10 bold italic')
levelLabel2 = Label(canvas, text=str(playerLevelNumber), fg='white', bg='black', font='Helvetica 10 bold italic')
scoreLabel1 = Label(canvas, text='Score:', fg='white', bg='black', font='Helvetica 10 bold italic')
scoreLabel2 = Label(canvas, text=str(userScore), fg='white', bg='black', font='Helvetica 10 bold italic')
highScoreLabel1 = Label(canvas, text='High Score:', fg='white', bg='black', font='Helvetica 10 bold italic')
highScoreLabel2 = Label(canvas, text='0', fg='white', bg='black', font='Helvetica 10 bold italic')


levelLabel1.pack()
levelLabel2.pack()
scoreLabel1.pack()
scoreLabel2.pack()
highScoreLabel1.pack()
highScoreLabel2.pack()

canvas.create_window(170,298,window=levelLabel1)
canvas.create_window(210,298,window=levelLabel2)
canvas.create_window(25,17,window=scoreLabel1)
canvas.create_window(75,17,window=scoreLabel2)
canvas.create_window(135,17,window=highScoreLabel1)
canvas.create_window(200,17,window=highScoreLabel2)

PacX, PacY = canvas.coords(PacPellet)
PacX2 = PacX + 7
PacY2 = PacY + 7
PacX1 = PacX - 7
PacY1 = PacY - 7

PelletsEaten = 0
CurrentDirection = 'Right'

PacFrame = 0
pacDead = False
bigPelletCounter = 0
bigPelletEaten = False
def AnimateBigPellet():

    global bigPelletCounter
    global pacDead
    
    for bigPellet in [bigPellet1,bigPellet2,bigPellet3,bigPellet4]:

        if bigPelletCounter == 0:

            canvas.itemconfig(bigPellet, fill='black')
            canvas.tag_lower(bigPellet)

        else:

            canvas.itemconfig(bigPellet, fill='white')
            canvas.tag_raise(bigPellet)
            canvas.tag_raise(Blinky.ghostPellet)
            canvas.tag_raise(Inky.ghostPellet)
            canvas.tag_raise(Pinky.ghostPellet)
            canvas.tag_raise(Clyde.ghostPellet)

    if bigPelletCounter == 0:

        bigPelletCounter = 1

    else:

        bigPelletCounter = 0

    if freeze:

        TimeWaster()

    if not pacDead:

        if bigPelletCounter == 0:

            canvas.after(175,AnimateBigPellet)

        else:

            canvas.after(150,AnimateBigPellet)

    else:
            
        canvas.tag_lower(Blinky.ghostPellet)
        canvas.tag_lower(Inky.ghostPellet)
        canvas.tag_lower(Pinky.ghostPellet)
        canvas.tag_lower(Clyde.ghostPellet)

bigPelletTimer = 0

def BigPelletEaten():

    global bigPelletEaten
    global ghostSpeed
    global bigPelletTimer
    global ghostKillCount

    if bigPelletTimer == 0:
        
        
        bigPelletEaten = 1
        Blinky.speed = 30
        Pinky.speed = 30
        Inky.speed = 30
        Clyde.speed = 30
        bigPelletTimer += 1
        canvas.after(4000,BigPelletEaten)

    elif bigPelletTimer in range(1,12):

        if bigPelletTimer % 2 == 0:

            bigPelletEaten = 2

        else:

            bigPelletEaten = 1

        bigPelletTimer += 1

        canvas.after(350,BigPelletEaten)

    else:

        bigPelletTimer = 0
        bigPelletEaten = False
        Blinky.speed = ghostSpeed
        Pinky.speed = ghostSpeed
        Inky.speed = ghostSpeed
        Clyde.speed = ghostSpeed
        Blinky.alreadyDied = False
        Pinky.alreadyDied = False
        Inky.alreadyDied = False
        Clyde.alreadyDied = False
        ghostKillCount = 0

def AnimatePac():

    global pacDead
    global PacFrame
    global CurrentDirection
    global UserDirection
    global freeze

    if not pacDead:

        
        AnimateWall = False

        AnimatePacX1, AnimatePacY1 = canvas.coords(PacPellet)
        AnimatePacX2 = AnimatePacX1 + 7
        AnimatePacY2 = AnimatePacY1 + 7
        AnimatePacX1-= 7
        AnimatePacY1 -= 7

        if UserDirection == 'Stop':

            pass

        elif PacFrame in [1,2,3]:

            IMGPAC['file'] = ('PacManTrial' + str(PacFrame + 1) + str(CurrentDirection) + '.png')

        elif PacFrame in [4,5]:

            IMGPAC['file'] = ('PacManTrial' + str(7-PacFrame) + str(CurrentDirection) + '.png')
            
        else:

            IMGPAC['file'] = 'PacManTrial1.png'
            PacFrame = 0

        if CurrentDirection == 'Right':

            for item in canvas.find_overlapping(AnimatePacX2 + 1, AnimatePacY1, AnimatePacX2 + 1, AnimatePacY2):


                try:

                    if canvas.itemcget(item, 'fill') == 'blue':

                        AnimateWall = True

                except:

                    pass

            if not AnimateWall:

                PacFrame += 1

        elif CurrentDirection == 'Left ':

            for item in canvas.find_overlapping(AnimatePacX1 - 1, AnimatePacY1, AnimatePacX1 - 1, AnimatePacY2):

                try:

                    if canvas.itemcget(item, 'fill') == 'blue':

                        AnimateWall = True

                except:

                    pass

            if not AnimateWall:

                PacFrame += 1

                
        elif CurrentDirection == 'Down ':

            for item in canvas.find_overlapping(AnimatePacX1, AnimatePacY2 + 1, AnimatePacX2, AnimatePacY2 + 1):


                try:

                    if canvas.itemcget(item, 'fill') == 'blue':

                        AnimateWall = True

                except:

                    pass

            if not AnimateWall:

                PacFrame += 1

        elif CurrentDirection == 'Up ke':

            for item in canvas.find_overlapping(AnimatePacX1, AnimatePacY1 - 1, AnimatePacX2, AnimatePacY1 - 1):


                try:

                    if canvas.itemcget(item, 'fill') == 'blue':

                        AnimateWall = True

                except:

                    pass

            if not AnimateWall:

                PacFrame += 1


        if freeze:

            TimeWaster()

        
        canvas.after(25,AnimatePac)
        
TimeKeeper = True

def MovePac():

    global pacDead
    global PelletsEaten
    global PacPellet
    global UserDirection
    global CurrentDirection
    global userScore
    global PacX
    global PacY
    global totalLives
    global bigPelletTimer
    global ghostKillCount
    global redPointsDisplay
    global pinkPointsDisplay
    global bluePointsDisplay
    global yellowPointsDisplay
    global playerLevelNumber
    global ghostSpeed
    global newLevel
        
    PacX, PacY = canvas.coords(PacPellet)
    PacX2 = PacX + 7
    PacY2 = PacY + 7
    PacX1 = PacX - 7
    PacY1 = PacY - 7
        
    Wall = False
    Wall2 = False

    missPac = False
    dont = False

    eyesFiles = ['GhostEyesDown.png','GhostEyesLeft.png','GhostEyesRight.png','GhostEyesUp.png']
    scaredFiles = ['ScaredGhost1.png','ScaredGhost2.png','ScaredGhost3.png','ScaredGhost4.png']
    
    for item in canvas.find_overlapping(PacX - 1, PacY - 1, PacX + 1, PacY + 1):

        if item in ghostNumList:

            if item == 197:

                if Blinky.ghostImg['file'] in eyesFiles:

                    missPac = True

                elif Blinky.ghostImg['file'] in scaredFiles:

                    if not Blinky.die:

                        ghostKillCount += 1
                        pointsImage = PhotoImage(file = ('Points' + str(ghostKillCount) + '.png'))
                        canvas.image = pointsImage
                        redPointsDisplay = canvas.create_image(Blinky.X,Blinky.Y, image=pointsImage)
                        Blinky.die = True
                        Blinky.speed = 10
                        userScore += ((2 ** ghostKillCount) * 100)
                        RedPoints()
                        

                else:

                    IMGPAC['file'] = 'PacManTrial1.png'
                    pacDead = True
                    time.sleep(1)

                    for ghost in ghostNumList:
                    
                        canvas.tag_lower(ghost)

                    totalLives -= 1
                    PacDie()

            if item == 198:

                if Pinky.ghostImg['file'] in eyesFiles:

                    missPac = True

                elif Pinky.ghostImg['file'] in scaredFiles:

                    if not Pinky.die:

                        ghostKillCount += 1
                        pointsImage = PhotoImage(file = ('Points' + str(ghostKillCount) + '.png'))
                        canvas.image = pointsImage
                        pinkPointsDisplay = canvas.create_image(Pinky.X,Pinky.Y, image=pointsImage)
                        Pinky.die = True
                        Pinky.speed = 10
                        userScore += ((2 ** ghostKillCount) * 100)
                        PinkPoints()
                else:

                    IMGPAC['file'] = 'PacManTrial1.png'
                    pacDead = True
                    time.sleep(1)

                    for ghost in ghostNumList:
                    
                        canvas.tag_lower(ghost)

                    totalLives -= 1
                    PacDie()

            if item == 199:

                if Inky.ghostImg['file'] in eyesFiles:

                    missPac = True

                elif Inky.ghostImg['file'] in scaredFiles:

                    if not Inky.die:
                        
                        ghostKillCount += 1
                        pointsImage = PhotoImage(file = ('Points' + str(ghostKillCount) + '.png'))
                        canvas.image = pointsImage
                        bluePointsDisplay = canvas.create_image(Inky.X,Inky.Y, image=pointsImage)
                        Inky.die = True
                        Inky.speed = 10
                        userScore += ((2 ** ghostKillCount) * 100)
                        BluePoints()

                else:

                    IMGPAC['file'] = 'PacManTrial1.png'
                    pacDead = True
                    time.sleep(1)

                    for ghost in ghostNumList:
                    
                        canvas.tag_lower(ghost)

                    totalLives -= 1
                    PacDie()

            if item == 200:

                if Clyde.ghostImg['file'] in eyesFiles:

                    missPac = True

                elif Clyde.ghostImg['file'] in scaredFiles:

                    if not Clyde.die:
                        
                        ghostKillCount += 1
                        pointsImage = PhotoImage(file = ('Points' + str(ghostKillCount) + '.png'))
                        canvas.image = pointsImage
                        yellowPointsDisplay = canvas.create_image(Clyde.X,Clyde.Y, image=pointsImage)
                        Clyde.die = True
                        Clyde.speed = 10
                        userScore += ((2 ** ghostKillCount) * 100)
                        YellowPoints()

                else:

                    IMGPAC['file'] = 'PacManTrial1.png'
                    pacDead = True
                    time.sleep(1)

                    for ghost in ghostNumList:
                    
                        canvas.tag_lower(ghost)

                    totalLives -= 1
                    PacDie()

    if not pacDead:
        
        if UserDirection == 'Stop':

            pass

        elif UserDirection == 'Right':

            for item in canvas.find_overlapping(PacX2 + 1, PacY1, PacX2 + 1, PacY2):


                try:

                    if canvas.itemcget(item, 'fill') == 'blue' or canvas.itemcget(item, 'fill') == 'grey':

                        Wall = True

                    else:

                        if canvas.itemcget(item, 'fill') != 'black':

                            canvas.delete(item)
                            PelletsEaten += 1

                            if PelletsEaten == 172:

                                NewLevel()
                                dont = True

                            if item in bigPelletNumList:

                                userScore += 50
                                if bigPelletTimer == 0:

                                    BigPelletEaten()

                            else:

                                userScore += 10

                except:

                    pass


            if not Wall and not dont:

                canvas.move(PacPellet,1,0)
                CurrentDirection = 'Right'

                PacX, PacY = canvas.coords(PacPellet)
                PacX2 = PacX + 7
                PacY2 = PacY + 7
                PacX1 = PacX - 7
                PacY1 = PacY - 7

                if PacX1 == Canvas_Width:

                    canvas.move(PacPellet,-(Canvas_Width+12),0)

        elif UserDirection == 'Left ':

            for item in canvas.find_overlapping(PacX1 - 1, PacY1, PacX1 - 1, PacY2):

                try:

                    if canvas.itemcget(item, 'fill') == 'blue' or canvas.itemcget(item, 'fill') == 'grey':

                        Wall = True

                    else:

                        if canvas.itemcget(item, 'fill') != 'black':

                            canvas.delete(item)
                            PelletsEaten += 1

                            if PelletsEaten == 172:

                                NewLevel()
                                dont = True

                            if item in bigPelletNumList:

                                userScore += 50
                                if bigPelletTimer == 0:

                                    BigPelletEaten()

                            else:

                                userScore += 10

                except:

                    pass


            if not Wall and not dont:

                canvas.move(PacPellet,-1,0)
                CurrentDirection = 'Left '

                PacX, PacY = canvas.coords(PacPellet)
                PacX2 = PacX + 7
                PacY2 = PacY + 7
                PacX1 = PacX - 7
                PacY1 = PacY - 7

                if PacX2 == 0:

                    canvas.move(PacPellet,+(Canvas_Width+13),0)

        elif UserDirection == 'Down ':

            for item in canvas.find_overlapping(PacX1, PacY2 + 1, PacX2, PacY2 + 1):

                try:

                    if canvas.itemcget(item, 'fill') == 'blue' or canvas.itemcget(item, 'fill') == 'grey':

                        Wall = True

                    else:

                        if canvas.itemcget(item, 'fill') != 'black':

                            canvas.delete(item)
                            PelletsEaten += 1

                            if PelletsEaten == 172:

                                NewLevel()
                                dont = True

                            if item in bigPelletNumList:

                                userScore += 50
                                if bigPelletTimer == 0:

                                    BigPelletEaten()

                            else:

                                userScore += 10

                except:

                    pass


            if not Wall and not dont:

                canvas.move(PacPellet,0,1)
                CurrentDirection = 'Down '

        elif UserDirection == 'Up ke':

            for item in canvas.find_overlapping(PacX1, PacY1 - 1, PacX2, PacY1 - 1):

                try:

                    if canvas.itemcget(item, 'fill') == 'blue' or canvas.itemcget(item, 'fill') == 'grey':

                        Wall = True

                    else:

                        if canvas.itemcget(item, 'fill') != 'black':

                            canvas.delete(item)
                            PelletsEaten += 1

                            if PelletsEaten == 172:

                                NewLevel()
                                dont = True

                            if item in bigPelletNumList:

                                userScore += 50
                                if bigPelletTimer == 0:

                                    BigPelletEaten()

                            else:

                                userScore += 10

                except:

                    pass


            if not Wall and not dont:

                canvas.move(PacPellet,0,-1)
                CurrentDirection = 'Up ke'

        if Wall:

                if CurrentDirection == 'Right':

                    

                    for item in canvas.find_overlapping(PacX2 + 1, PacY1, PacX2 + 1, PacY2):

                        try:

                            if canvas.itemcget(item, 'fill') == 'blue' or canvas.itemcget(item, 'fill') == 'grey':

                                Wall2 = True

                            else:

                                if canvas.itemcget(item, 'fill') != 'black':

                                    canvas.delete(item)
                                    PelletsEaten += 1

                                    if PelletsEaten == 172:

                                        NewLevel()
                                        dont = True

                                    if item in bigPelletNumList:

                                        userScore += 50
                                        if bigPelletTimer == 0:

                                            BigPelletEaten()

                                    else:

                                        userScore += 10

                        except:

                            pass
                                

                    if Wall2 == False and not dont:

                        canvas.move(PacPellet,1,0)

                        PacX, PacY = canvas.coords(PacPellet)
                        PacX2 = PacX + 7
                        PacY2 = PacY + 7
                        PacX1 = PacX - 7
                        PacY1 = PacY - 7

                        if PacX1 == Canvas_Width:

                            canvas.move(PacPellet,-(Canvas_Width+12),0)
                        

                elif CurrentDirection == 'Left ':

                    for item in canvas.find_overlapping(PacX1 - 1, PacY1, PacX1 - 1, PacY2):

                        try:

                            if canvas.itemcget(item, 'fill') == 'blue' or canvas.itemcget(item, 'fill') == 'grey':

                                Wall2 = True

                            else:

                                if canvas.itemcget(item, 'fill') != 'black':

                                    canvas.delete(item)
                                    PelletsEaten += 1

                                    if PelletsEaten == 172:

                                        NewLevel()
                                        dont = True

                                    if item in bigPelletNumList:

                                        userScore += 50
                                        if bigPelletTimer == 0:

                                            BigPelletEaten()

                                    else:

                                        userScore += 10

                        except:

                            pass
                                

                    if Wall2 == False and not dont:

                        canvas.move(PacPellet,-1,0)

                        PacX, PacY = canvas.coords(PacPellet)
                        PacX2 = PacX + 7
                        PacY2 = PacY + 7
                        PacX1 = PacX - 7
                        PacY1 = PacY - 7

                        if PacX2 == 0:

                            canvas.move(PacPellet,+(Canvas_Width+12),0)
                        

                elif CurrentDirection == 'Down ':

                    for item in canvas.find_overlapping(PacX1, PacY2 + 1, PacX2, PacY2 + 1):

                        try:

                            if canvas.itemcget(item, 'fill') == 'blue' or canvas.itemcget(item, 'fill') == 'grey':

                                Wall2 = True

                            else:

                                if canvas.itemcget(item, 'fill') != 'black':

                                    canvas.delete(item)
                                    PelletsEaten += 1
                                    
                                    if PelletsEaten == 172:

                                        NewLevel()
                                        dont = True

                                    if item in bigPelletNumList:

                                        userScore += 50
                                        if bigPelletTimer == 0:

                                            BigPelletEaten()

                                    else:

                                        userScore += 10

                        except:

                            pass
                                

                    if Wall2 == False and not dont:

                        canvas.move(PacPellet,0,1)

                elif CurrentDirection == 'Up ke':

                    for item in canvas.find_overlapping(PacX1, PacY1 - 1, PacX2, PacY1 - 1):

                        try:
                            
                            if canvas.itemcget(item, 'fill') == 'blue' or canvas.itemcget(item, 'fill') == 'grey':

                                Wall2 = True

                            else:

                                if canvas.itemcget(item, 'fill') != 'black':

                                    canvas.delete(item)
                                    PelletsEaten += 1
                                    
                                    if PelletsEaten == 172:
                                        
                                        NewLevel()
                                        dont = True

                                    if item in bigPelletNumList:

                                        userScore += 50
                                        if bigPelletTimer == 0:

                                            BigPelletEaten()

                                    else:

                                        userScore += 10

                        except:

                            pass
                                

                    if Wall2 == False and not dont:

                        canvas.move(PacPellet,0,-1)

            

        scoreLabel2['text'] = userScore

        if userScore > int(highScoreLabel2['text']):

            highScoreLabel2['text'] = userScore

        
        PacX, PacY = canvas.coords(PacPellet)
        PacX2 = PacX + 7
        PacY2 = PacY + 7
        PacX1 = PacX - 7
        PacY1 = PacY - 7
        
        if freeze:

            TimeWaster()
            
        canvas.after(PAC.speed,MovePac)
        
deathSkin = 3
gameOverImg = PhotoImage(file = 'GameOver.png')

redPointsTracker = 0
pinkPointsTracker = 0
bluePointsTracker = 0
yellowPointsTracker = 0

newLevelTracker = 0

def NewLevel():

    global playerLevelNumber
    global UserDirection
    global CurrentDirection
    global PelletsEaten
    global newLevelTracker
    global newLevel
    global ghostSpeed
    global bigPelletCounter
    global bigPelletTimer
    global loadingWindow


    newLevel = True
    UserDirection = 'Stop'

    try:

        canvas.delete(loadingWindow)

    except:
        
        pass
    
    if newLevelTracker != 1:

        newLevelTracker = 1
        canvas.after(1500,NewLevel)

    elif bigPelletTimer != 0:

        loadingLabel.pack()
        loadingWindow = canvas.create_window(108,298,window=loadingLabel)
        canvas.after(50, NewLevel)

    else:

        playerLevelNumber += 1
        levelLabel2['text'] = str(playerLevelNumber)
        newLevel = False
        Blinky.Restart()
        Pinky.Restart()
        Inky.Restart()
        Clyde.Restart()
        UserDirection = 'Stop'
        canvas.move(PacPellet,(116-PacX),(224-PacY))

        if ghostSpeed != 11:

            ghostSpeed -= 1
                                            
        PelletsEaten = 0
        CreatePellets()
        newLevelTracker = 0

def RedPoints():

    global redPointsTracker
    global redPointsDisplay

    if redPointsTracker == 0:

        redPointsTracker = 1
        canvas.after(800,RedPoints)

    else:

        redPointsTracker = 0
        canvas.delete(redPointsDisplay)

def PinkPoints():

    global pinkPointsTracker
    global pinkPointsDisplay

    if pinkPointsTracker == 0:

        pinkPointsTracker = 1
        canvas.after(800,PinkPoints)

    else:

        pinkPointsTracker = 0
        canvas.delete(pinkPointsDisplay)

def BluePoints():

    global bluePointsTracker
    global bluePointsDisplay

    if bluePointsTracker == 0:

        bluePointsTracker = 1
        canvas.after(800,BluePoints)

    else:

        bluePointsTracker = 0
        canvas.delete(bluePointsDisplay)

def YellowPoints():

    global yellowPointsTracker
    global yellowPointsDisplay

    if yellowPointsTracker == 0:

        yellowPointsTracker = 1
        canvas.after(800,YellowPoints)

    else:

        yellowPointsTracker = 0
        canvas.delete(yellowPointsDisplay)



def PacDie():

    global totalLives
    global deathSkin
    global IMGPAC
    global PacPellet
    global UserDirection
    global pacDead
    global PacFrame
    global CurrentDirection
    global gameOverImg
    global bigPelletEaten
    global playerLevelNumber
        
    if deathSkin in [3,4]:

        IMGPAC['file'] = 'PacManTrial' + str(deathSkin) + 'Up ke.png'
        time.sleep(0.2)

    elif deathSkin in [5,6,7,8,9,10]:

        IMGPAC['file'] = 'PacManTrial' + str(deathSkin) + 'Death.png'
        
    elif deathSkin == 12:

        canvas.delete(PacPellet)

        if totalLives == 2:

            canvas.delete(life3)

        if totalLives == 1:

            canvas.delete(life2)

        if totalLives == 0:

            canvas.delete(life1)

    deathSkin += 1

        
    if deathSkin < 13:

        canvas.after(170,PacDie)

    elif totalLives < 0:

        GameOver()

    else:

        StartAgain()

def StartAgain():
    
    global PacPellet
    global pacDead
    global UserDirection
    global bigPelletEaten
    global deathSkin
    global IMGPAC
    
    if bigPelletEaten == False:

        IMGPAC = PhotoImage(file = 'PacManTrial1.png')
        canvas.image = IMGPAC
        PacPellet = canvas.create_image(116,224, image = IMGPAC)
        pacDead = False
        UserDirection = 'Stop'
        bigPelletEaten = False
        Blinky.Restart()
        Pinky.Restart()
        Inky.Restart()
        Clyde.Restart()
        AnimatePac()
        MovePac()
        AnimateBigPellet()
        deathSkin  = 3

    else:

        canvas.after(10,StartAgain)

def GameOver():

    global gameOverImg

    gameOverSign = canvas.create_image(115,176, image = gameOverImg)
    canvas.tag_raise(gameOverSign)

    if userScore > int(originalHighScore):

        with open('HighScore.txt', 'w') as highScoreFile:

            highScoreFile.write(format(userScore ^ int(key, 2), '#024b') + '\n' + key)

class PacMan():
    
    def __init__(self, PacSpeed, PacDirection):

        self.speed = PacSpeed 
        self.direction = PacDirection
        self.powerup = 0

        # Khởi tạo pygame
        pygame.init()
        # Phát nhạc liên tục
        pygame.mixer.music.load(
            "playing-pac-man-6783.mp3")  # Thay đổi "your_music_file.mp3" bằng đường dẫn đến file nhạc của bạn
        pygame.mixer.music.play(loops=-1)  # Số âm là phát nhạc liên tục


PAC = PacMan(15,8)

UserDirection = 'Stop'
AnimatePac()
ghostNumList = []

class Ghosts():
    
    global PacX1
    global PacY1
    global ghostNumList
    global ghostSpeed
    
    def __init__(self,colour):
        
        self.colour = colour
        self.state = 0
        self.powerup = 0
        self.direction = 'Down'
        self.frames = 0
        self.speed = ghostSpeed
        self.die = False
        self.reachedBox = False
        self.leftBox = False
        self.alreadyDied = False
        
        if self.colour == 'Red':

            self.X = 116
            self.Y = 127
            self.originalX = 116
            self.originalY = 127
            self.choices = [0,0,1,1]
            self.choicesNegative = [0,0,-1,-1]

        elif self.colour == 'Pink':

            self.X = 116
            self.Y = 152
            self.originalX = 116
            self.originalY = 152
            self.choices = [0,1,1,1]
            self.choicesNegative = [0,-1,-1,-1]

        elif self.colour == 'Blue':

            self.X = 100
            self.Y = 152
            self.originalX = 100
            self.originalY = 152
            self.choices = [0,random.choice([0,1]),random.choice([0,1]),1]
            self.choicesNegative = [0,random.choice([0,-1]),random.choice([0,-1]),-1]

        elif self.colour == 'Yellow':

            self.X = 132
            self.Y = 152
            self.originalX = 132
            self.originalY = 152
            self.choices = [0,0,0,1]
            self.choicesNegative = [0,0,0,-1]

        self.ghostImg = PhotoImage(file = (str(self.colour)+'Ghost' +str(self.direction) + '2.png'))
        self.ghostPellet = canvas.create_image(self.X,self.Y, image=self.ghostImg)
        self.ghostNum = 0
        for item in canvas.find_overlapping(self.X,self.Y,self.X + 4,self.Y + 4):

            try:
                
                if canvas.itemcget(item, 'fill') == 'banana':

                    pass
                    
            except:

                self.ghostNum = item
            
        ghostNumList.append(self.ghostNum)
        self.trapped = True
        self.timer = 0
        self.rightWall = False
        self.leftWall = False
        self.upWall = False
        self.downWall = False
        self.direction = 'Down'
        self.AnimateGhost()
        self.StartMoveGhost()

    def Tests(self):

        try:

            pass

        except:

            pass

        canvas.after(10, self.Tests)
        
    def AnimateGhost(self):

        global pacDead
        global bigPelletEaten
        global newLevel

        if not pacDead and not newLevel:

            if not bigPelletEaten or self.alreadyDied:

                if self.die:

                    self.ghostImg['file'] = 'GhostEyes' + str(self.direction) + '.png'
                
                elif self.state == 1:

                    self.ghostImg['file'] = (str(self.colour)+'Ghost' +str(self.direction) + '2.png')

                elif self.state == 2:

                    self.ghostImg['file'] = (str(self.colour)+'Ghost' +str(self.direction) + '.png')
                    self.state = 0

            elif bigPelletEaten == 1:

                if self.die:

                    self.ghostImg['file'] = 'GhostEyes' + str(self.direction) + '.png'

                elif self.state == 1:

                    self.ghostImg['file'] = 'ScaredGhost2.png'

                elif self.state == 2:

                    self.ghostImg['file'] = 'ScaredGhost1.png'
                    self.state = 0

            else:

                if self.die:

                    self.ghostImg['file'] = 'GhostEyes' + str(self.direction) + '.png'

                elif self.state == 1:

                    self.ghostImg['file'] = 'ScaredGhost4.png'

                elif self.state == 2:

                    self.ghostImg['file'] = 'ScaredGhost3.png'
                    self.state = 0

            self.state += 1

            if freeze:

                TimeWaster()

            canvas.after(130,self.AnimateGhost)


    def StartMoveGhost(self):

        global pacDead
        global newLevel

        if not pacDead and not newLevel:
            
            self.X, self.Y = canvas.coords(self.ghostPellet)


            if self.Y == 127:

                self.trapped = False
                self.direction = random.choice(['Right', 'Left'])

            elif self.colour == 'Pink':

                if self.timer != 20:

                    self.timer += 1

                else:

                    canvas.move(self.ghostPellet,0,-1)
                    self.direction = 'Up'

            elif self.colour == 'Blue':

                if not Pinky.trapped:

                    if self.timer != 20:

                        self.timer += 1

                    else:

                        if self.X != 116:

                            canvas.move(self.ghostPellet,1,0)
                            self.direction = 'Right'

                        else:

                            canvas.move(self.ghostPellet,0,-1)
                            self.direction = 'Up'

            elif self.colour == 'Yellow':

                if not Inky.trapped:


                    if self.timer != 20:

                        self.timer += 1

                    else:

                        if self.X != 116:

                            canvas.move(self.ghostPellet,-1,0)
                            self.direction = 'Left'

                        else:

                            canvas.move(self.ghostPellet,0,-1)
                            self.direction = 'Up'

              
                
                if freeze:

                    TimeWaster()
                    
            if self.trapped:

                canvas.after(50,self.StartMoveGhost)

            else:

                self.MoveGhost()
                self.timer = 0

    def MoveGhost(self):

        global pacDead
        global newLevel

        if not pacDead and not newLevel:
            
            self.rightWall = False
            self.leftWall = False
            self.upWall = False
            self.downWall = False
            self.moved = False

            self.X, self.Y = canvas.coords(self.ghostPellet)

            self.X1 = self.X - 7
            self.Y1 = self.Y - 7
            self.X2 = self.X + 7
            self.Y2 = self.Y + 7

            if self.X1 == Canvas_Width and self.direction == 'Right':

                canvas.move(self.ghostPellet,-(Canvas_Width+12),0)

            elif self.X2 == 0 and self.direction == 'Left':

                canvas.move(self.ghostPellet,(Canvas_Width+12),0)

                    
            for item in canvas.find_overlapping(self.X2 + 1, self.Y1, self.X2 + 1, self.Y2):

                try:

                    if canvas.itemcget(item, 'fill') == 'blue' or canvas.itemcget(item, 'fill') == 'grey':

                        self.rightWall = True

                except:

                    pass

            for item in canvas.find_overlapping(self.X1 - 1, self.Y1, self.X1 - 1, self.Y2):

                try:

                    if canvas.itemcget(item, 'fill') == 'blue' or canvas.itemcget(item, 'fill') == 'grey':

                        self.leftWall = True

                except:

                    pass

            for item in canvas.find_overlapping(self.X1, self.Y1 - 1, self.X2, self.Y1 - 1):

                try:

                    if canvas.itemcget(item, 'fill') == 'blue' or canvas.itemcget(item, 'fill') == 'grey':

                        self.upWall = True

                except:

                    pass

            for item in canvas.find_overlapping(self.X1, self.Y2 + 1, self.X2, self.Y2 + 1):

                try:

                    if canvas.itemcget(item, 'fill') == 'blue' or canvas.itemcget(item, 'fill') == 'grey':

                        self.downWall = True
                except:

                    pass

            if self.direction == 'Right':

                if PacY1 > self.Y1:

                    if not self.downWall:

                        self.ghostChoice = random.choice(self.choices)
                        canvas.move(self.ghostPellet,0,self.ghostChoice)
                        if self.ghostChoice == 1:

                            self.direction = 'Down'
                            self.moved = True

                    if not self.upWall and not self.moved:

                        self.ghostChoice = random.choice(self.choicesNegative)
                        canvas.move(self.ghostPellet,0,self.ghostChoice)

                        if self.ghostChoice == -1:

                            self.direction = 'Up'
                            self.moved = True

                    if not self.rightWall and not self.moved:

                        
                        canvas.move(self.ghostPellet,1,0)
                        self.moved = True

                    if not self.leftWall and not self.moved:

                        self.ghostChoice = random.choice(self.choicesNegative)
                        canvas.move(self.ghostPellet,self.ghostChoice,0)

                        if self.ghostChoice == -1:

                            self.direction = 'Left'
                            self.moved = True

                elif PacY1 < self.Y1:

                    if not self.upWall:

                        self.ghostChoice = random.choice(self.choicesNegative)
                        canvas.move(self.ghostPellet,0,self.ghostChoice)

                        if self.ghostChoice == -1:

                            self.direction = 'Up'
                            self.moved = True

                    if not self.downWall and not self.moved:

                        self.ghostChoice = random.choice(self.choices)
                        canvas.move(self.ghostPellet,0,self.ghostChoice)

                        if self.ghostChoice == 1:

                            self.direction = 'Down'
                            self.moved = True

                    if not self.rightWall and not self.moved:
                        
                        canvas.move(self.ghostPellet,1,0)
                        self.moved = True

                    if not self.leftWall and not self.moved:

                        self.ghostChoice = random.choice(self.choicesNegative)
                        canvas.move(self.ghostPellet,self.ghostChoice,0)

                        if self.ghostChoice == -1:

                            self.direction = 'Left'
                            self.moved = True

                else:

                    if not self.rightWall:

                        canvas.move(self.ghostPellet,1,0)
                        self.moved = True

                    if not self.leftWall and not self.moved:

                        self.ghostChoice = random.choice(self.choicesNegative)
                        canvas.move(self.ghostPellet,self.ghostChoice,0)

                        if self.ghostChoice == -1:

                            self.direction == 'Left'
                            self.moved = True

                    if not self.downWall and not self.moved:

                        self.ghostChoice = random.choice(self.choices)
                        canvas.move(self.ghostPellet,0,self.ghostChoice)

                        if self.ghostChoice == 1:

                            self.direction = 'Down'
                            self.moved = True

                    if not self.upWall and not self.moved:

                        self.ghostChoice = random.choice(self.choicesNegative)
                        canvas.move(self.ghostPellet,0,self.ghostChoice)

                        if self.ghostChoice == -1:

                            self.direction = 'Up'
                            self.moved = True

            elif self.direction == 'Left':

                if PacY1 > self.Y1:

                    if not self.downWall:

                        self.ghostChoice = random.choice(self.choices)
                        canvas.move(self.ghostPellet,0,self.ghostChoice)

                        if self.ghostChoice == 1:

                            self.direction = 'Down'
                            self.moved = True

                    if not self.upWall and not self.moved:

                        self.ghostChoice = random.choice(self.choicesNegative)
                        canvas.move(self.ghostPellet,0,self.ghostChoice)

                        if self.ghostChoice == -1:

                            self.direction = 'Up'
                            self.moved = True

                    if not self.leftWall and not self.moved:

                        canvas.move(self.ghostPellet,-1,0)
                        self.moved = True

                    if not self.rightWall and not self.moved:

                        self.ghostChoice = random.choice(self.choices)
                        canvas.move(self.ghostPellet,self.ghostChoice,0)

                        if self.ghostChoice == 1:

                            self.direction = 'Right'
                            self.moved = True

                elif PacY1 < self.Y1:

                    if not self.upWall:

                        self.ghostChoice = random.choice(self.choicesNegative)
                        canvas.move(self.ghostPellet,0,self.ghostChoice)

                        if self.ghostChoice == -1:

                            self.direction = 'Up'
                            self.moved = True

                    if not self.downWall and not self.moved:

                        self.ghostChoice = random.choice(self.choices)
                        canvas.move(self.ghostPellet,0,self.ghostChoice)

                        if self.ghostChoice == 1:

                            self.direction = 'Down'
                            self.moved = True

                    if not self.leftWall and not self.moved:
                        
                        canvas.move(self.ghostPellet,-1,0)
                        self.moved = True

                    if not self.rightWall and not self.moved:

                        self.ghostChoice = random.choice(self.choices)
                        canvas.move(self.ghostPellet,self.ghostChoice,0)

                        if self.ghostChoice == 1:

                            self.direction = 'Right'
                            self.moved = True

                else:

                    if not self.leftWall:

                        canvas.move(self.ghostPellet,-1,0)
                        self.moved = True

                    if not self.rightWall and not self.moved:

                        self.ghostChoice = random.choice(self.choices)
                        canvas.move(self.ghostPellet,self.ghostChoice,0)

                        if self.ghostChoice == 1:

                            self.direction == 'Right'
                            self.moved = True

                    if not self.downWall and not self.moved:

                        self.ghostChoice = random.choice(self.choices)
                        canvas.move(self.ghostPellet,0,self.ghostChoice)

                        if self.ghostChoice == 1:

                            self.direction = 'Down'
                            self.moved = True

                    if not self.upWall and not self.moved:

                        self.ghostChoice = random.choice(self.choicesNegative)
                        canvas.move(self.ghostPellet,0,self.ghostChoice)

                        if self.ghostChoice == -1:

                            self.direction = 'Up'
                            self.moved = True


            elif self.direction == 'Down':

                if PacX1 > self.X1:

                    if not self.rightWall:

                        self.ghostChoice = random.choice(self.choices)
                        canvas.move(self.ghostPellet,self.ghostChoice,0)

                        if self.ghostChoice == 1:

                            self.direction = 'Right'
                            self.moved = True

                    if not self.leftWall and not self.moved:

                        self.ghostChoice = random.choice(self.choicesNegative)
                        canvas.move(self.ghostPellet,self.ghostChoice,0)

                        if self.ghostChoice == -1:

                            self.direction = 'Left'
                            self.moved = True

                    if not self.downWall and not self.moved:

                        canvas.move(self.ghostPellet,0,1)
                        self.moved = True

                    if not self.upWall and not self.moved:

                        self.ghostChoice = random.choice(self.choicesNegative)
                        canvas.move(self.ghostPellet,0,self.ghostChoice)

                        if self.ghostChoice == -1:

                            self.direction = 'Up'
                            self.moved = True

                elif PacX1 < self.X1:

                    if not self.leftWall:

                        self.ghostChoice = random.choice(self.choicesNegative)
                        canvas.move(self.ghostPellet,self.ghostChoice,0)

                        if self.ghostChoice == -1:

                            self.direction = 'Left'
                            self.moved = True

                    if not self.rightWall and not self.moved:

                        self.ghostChoice = random.choice(self.choices)
                        canvas.move(self.ghostPellet,self.ghostChoice,0)

                        if self.ghostChoice == 1:

                            self.direction = 'Right'
                            self.moved = True

                    if not self.downWall and not self.moved:
                        
                        canvas.move(self.ghostPellet,0,1)
                        self.moved = True

                    if not self.upWall and not self.moved:

                        self.ghostChoice = random.choice(self.choicesNegative)
                        canvas.move(self.ghostPellet,0,self.ghostChoice)

                        if self.ghostChoice == -1:

                            self.direction = 'Up'
                            self.moved = True

                else:

                    if not self.downWall:

                        canvas.move(self.ghostPellet,0,1)
                        self.moved = True

                    if not self.upWall and not self.moved:

                        self.ghostChoice = random.choice(self.choicesNegative)
                        canvas.move(self.ghostPellet,0,self.ghostChoice)

                        if self.ghostChoice == -1:

                            self.direction == 'Up'
                            self.moved = True

                    if not self.leftWall and not self.moved:

                        self.ghostChoice = random.choice(self.choicesNegative)
                        canvas.move(self.ghostPellet,self.ghostChoice,0)

                        if self.ghostChoice == -1:

                            self.direction = 'Left'
                            self.moved = True

                    if not self.rightWall and not self.moved:

                        self.ghostChoice = random.choice(self.choices)
                        canvas.move(self.ghostPellet,self.ghostChoice,0)

                        if self.ghostChoice == 1:

                            self.direction = 'Right'
                            self.moved = True            


            elif self.direction == 'Up':

                if PacX1 > self.X1:

                    if not self.rightWall:

                        self.ghostChoice = random.choice(self.choices)
                        canvas.move(self.ghostPellet,self.ghostChoice,0)

                        if self.ghostChoice == 1:

                            self.direction = 'Right'
                            self.moved = True

                    if not self.leftWall and not self.moved:

                        self.ghostChoice = random.choice(self.choicesNegative)
                        canvas.move(self.ghostPellet,self.ghostChoice,0)

                        if self.ghostChoice == -1:

                            self.direction = 'Left'
                            self.moved = True

                    if not self.upWall and not self.moved:

                        canvas.move(self.ghostPellet,0,-1)
                        self.moved = True

                    if not self.downWall and not self.moved:

                        self.ghostChoice = random.choice(self.choices)
                        canvas.move(self.ghostPellet,0,self.ghostChoice)

                        if self.ghostChoice == 1:

                            self.direction = 'Down'
                            self.moved = True

                elif PacX1 < self.X1:

                    if not self.leftWall:

                        self.ghostChoice = random.choice(self.choicesNegative)
                        canvas.move(self.ghostPellet,self.ghostChoice,0)

                        if self.ghostChoice == -1:

                            self.direction = 'Left'
                            self.moved = True

                    if not self.rightWall and not self.moved:

                        self.ghostChoice = random.choice(self.choices)
                        canvas.move(self.ghostPellet,self.ghostChoice,0)

                        if self.ghostChoice == 1:

                            self.direction = 'Right'
                            self.moved = True

                    if not self.upWall and not self.moved:
                        
                        canvas.move(self.ghostPellet,0,-1)
                        self.moved = True

                    if not self.downWall and not self.moved:

                        self.ghostChoice = random.choice(self.choices)
                        canvas.move(self.ghostPellet,0,self.ghostChoice)

                        if self.ghostChoice == 1:

                            self.direction = 'Down'
                            self.moved = True

                else:

                    if not self.upWall:

                        canvas.move(self.ghostPellet,0,-1)
                        self.moved = True

                    if not self.downWall and not self.moved:

                        self.ghostChoice = random.choice(self.choices)
                        canvas.move(self.ghostPellet,0,self.ghostChoice)

                        if self.ghostChoice == 1:

                            self.direction == 'Down'
                            self.moved = True

                    if not self.leftWall and not self.moved:

                        self.ghostChoice = random.choice(self.choicesNegative)
                        canvas.move(self.ghostPellet,self.ghostChoice,0)

                        if self.ghostChoice == -1:

                            self.direction = 'Left'
                            self.moved = True

                    if not self.rightWall and not self.moved:

                        self.ghostChoice = random.choice(self.choices)
                        canvas.move(self.ghostPellet,self.ghostChoice,0)

                        if self.ghostChoice == 1:

                            self.direction = 'Right'
                            self.moved = True                

                    
            self.frames += 1

            if freeze:

                TimeWaster()
                
            if not self.die:

                canvas.after(self.speed,self.MoveGhost)

            else:

                self.DieMoveGhost()

    def DieMoveGhost(self):
        
        global pacDead
        global bigPelletTimer
        global newLevel

        if not pacDead and not self.reachedBox and not newLevel:
            
            self.rightWall = False
            self.leftWall = False
            self.upWall = False
            self.downWall = False
            self.moved = False

            self.X, self.Y = canvas.coords(self.ghostPellet)

            self.X1 = self.X - 7
            self.Y1 = self.Y - 7
            self.X2 = self.X + 7
            self.Y2 = self.Y + 7

            if self.X1 == Canvas_Width and self.direction == 'Right':

                canvas.move(self.ghostPellet,-(Canvas_Width+12),0)

            elif self.X2 == 0 and self.direction == 'Left':

                canvas.move(self.ghostPellet,(Canvas_Width+12),0)

                    
            for item in canvas.find_overlapping(self.X2 + 1, self.Y1, self.X2 + 1, self.Y2):

                try:

                    if canvas.itemcget(item, 'fill') == 'blue':

                        self.rightWall = True

                except:

                    pass

            for item in canvas.find_overlapping(self.X1 - 1, self.Y1, self.X1 - 1, self.Y2):

                try:

                    if canvas.itemcget(item, 'fill') == 'blue':

                        self.leftWall = True

                except:

                    pass

            for item in canvas.find_overlapping(self.X1, self.Y1 - 1, self.X2, self.Y1 - 1):

                try:

                    if canvas.itemcget(item, 'fill') == 'blue':

                        self.upWall = True

                except:

                    pass

            for item in canvas.find_overlapping(self.X1, self.Y2 + 1, self.X2, self.Y2 + 1):

                try:

                    if canvas.itemcget(item, 'fill') == 'blue':

                        self.downWall = True
                except:

                    pass

            if self.direction == 'Right':

                if 152 > self.Y:

                    if not self.downWall:

                        canvas.move(self.ghostPellet,0,1)
                        if 1 == 1:

                            self.direction = 'Down'
                            self.moved = True


                    if not self.rightWall and not self.moved:

                        
                        canvas.move(self.ghostPellet,1,0)
                        self.moved = True

                    if not self.upWall and not self.moved:
                        
                        canvas.move(self.ghostPellet,0,-1)

                        if -1 == -1:

                            self.direction = 'Up'
                            self.moved = True

                    if not self.leftWall and not self.moved:
                        
                        canvas.move(self.ghostPellet,-1,0)

                        if -1 == -1:

                            self.direction = 'Left'
                            self.moved = True

                elif 152 < self.Y:

                    if not self.upWall:
                        
                        canvas.move(self.ghostPellet,0,-1)

                        if -1 == -1:

                            self.direction = 'Up'
                            self.moved = True


                    if not self.rightWall and not self.moved:
                        
                        canvas.move(self.ghostPellet,1,0)
                        self.moved = True

                    if not self.downWall and not self.moved:
                        
                        canvas.move(self.ghostPellet,0,1)

                        if 1 == 1:

                            self.direction = 'Down'
                            self.moved = True

                    if not self.leftWall and not self.moved:
                        
                        canvas.move(self.ghostPellet,-1,0)

                        if -1 == -1:

                            self.direction = 'Left'
                            self.moved = True

                else:

                    if not self.rightWall:

                        canvas.move(self.ghostPellet,1,0)
                        self.moved = True

                    if not self.leftWall and not self.moved:
                        
                        canvas.move(self.ghostPellet,-1,0)

                        if -1 == -1:

                            self.direction == 'Left'
                            self.moved = True

                    if not self.downWall and not self.moved:
                        
                        canvas.move(self.ghostPellet,0,1)

                        if 1 == 1:

                            self.direction = 'Down'
                            self.moved = True

                    if not self.upWall and not self.moved:
                        
                        canvas.move(self.ghostPellet,0,-1)

                        if -1 == -1:

                            self.direction = 'Up'
                            self.moved = True

            elif self.direction == 'Left':

                if 152 > self.Y:

                    if not self.downWall:
                        
                        canvas.move(self.ghostPellet,0,1)

                        if 1 == 1:

                            self.direction = 'Down'
                            self.moved = True


                    if not self.leftWall and not self.moved:

                        canvas.move(self.ghostPellet,-1,0)
                        self.moved = True

                    if not self.upWall and not self.moved:
                        
                        canvas.move(self.ghostPellet,0,-1)

                        if -1 == -1:

                            self.direction = 'Up'
                            self.moved = True

                    if not self.rightWall and not self.moved:
                        
                        canvas.move(self.ghostPellet,1,0)

                        if 1 == 1:

                            self.direction = 'Right'
                            self.moved = True

                elif 152 < self.Y:

                    if not self.upWall:
                        
                        canvas.move(self.ghostPellet,0,-1)

                        if -1 == -1:

                            self.direction = 'Up'
                            self.moved = True


                    if not self.leftWall and not self.moved:
                        
                        canvas.move(self.ghostPellet,-1,0)
                        self.moved = True

                    if not self.downWall and not self.moved:
                        
                        canvas.move(self.ghostPellet,0,1)

                        if 1 == 1:

                            self.direction = 'Down'
                            self.moved = True

                    if not self.rightWall and not self.moved:
                        
                        canvas.move(self.ghostPellet,1,0)

                        if 1 == 1:

                            self.direction = 'Right'
                            self.moved = True

                else:

                    if not self.leftWall:

                        canvas.move(self.ghostPellet,-1,0)
                        self.moved = True

                    if not self.rightWall and not self.moved:
                        
                        canvas.move(self.ghostPellet,1,0)

                        if 1 == 1:

                            self.direction == 'Right'
                            self.moved = True

                    if not self.downWall and not self.moved:
                        
                        canvas.move(self.ghostPellet,0,1)

                        if 1 == 1:

                            self.direction = 'Down'
                            self.moved = True

                    if not self.upWall and not self.moved:
                        
                        canvas.move(self.ghostPellet,0,-1)

                        if -1 == -1:

                            self.direction = 'Up'
                            self.moved = True


            elif self.direction == 'Down':

                if 116 > self.X:

                    if not self.rightWall:
                        
                        canvas.move(self.ghostPellet,1,0)

                        if 1 == 1:

                            self.direction = 'Right'
                            self.moved = True


                    if not self.downWall and not self.moved:

                        canvas.move(self.ghostPellet,0,1)
                        self.moved = True

                    if not self.leftWall and not self.moved:
                        
                        canvas.move(self.ghostPellet,-1,0)

                        if -1 == -1:

                            self.direction = 'Left'
                            self.moved = True

                    if not self.upWall and not self.moved:
                        
                        canvas.move(self.ghostPellet,0,-1)

                        if -1 == -1:

                            self.direction = 'Up'
                            self.moved = True

                elif 116 < self.X:

                    if not self.leftWall:
                        
                        canvas.move(self.ghostPellet,-1,0)

                        if -1 == -1:

                            self.direction = 'Left'
                            self.moved = True
                            


                    if not self.downWall and not self.moved:
                        
                        canvas.move(self.ghostPellet,0,1)
                        self.moved = True

                    if not self.rightWall and not self.moved:
                        
                        canvas.move(self.ghostPellet,1,0)

                        if 1 == 1:

                            self.direction = 'Right'
                            self.moved = True

                    if not self.upWall and not self.moved:
                        
                        canvas.move(self.ghostPellet,0,-1)

                        if -1 == -1:

                            self.direction = 'Up'
                            self.moved = True

                else:

                    if not self.downWall:

                        canvas.move(self.ghostPellet,0,1)
                        self.moved = True

                    if not self.upWall and not self.moved:
                        
                        canvas.move(self.ghostPellet,0,-1)

                        if -1 == -1:

                            self.direction == 'Up'
                            self.moved = True

                    if not self.leftWall and not self.moved:
                        
                        canvas.move(self.ghostPellet,-1,0)

                        if -1 == -1:

                            self.direction = 'Left'
                            self.moved = True

                    if not self.rightWall and not self.moved:
                        
                        canvas.move(self.ghostPellet,1,0)

                        if 1 == 1:

                            self.direction = 'Right'
                            self.moved = True            


            elif self.direction == 'Up':

                if 116 > self.X:

                    if not self.rightWall:
                        
                        canvas.move(self.ghostPellet,1,0)

                        if 1 == 1:

                            self.direction = 'Right'
                            self.moved = True


                    if not self.upWall and not self.moved:

                        canvas.move(self.ghostPellet,0,-1)
                        self.moved = True


                    if not self.leftWall and not self.moved:
                        
                        canvas.move(self.ghostPellet,-1,0)

                        if -1 == -1:

                            self.direction = 'Left'
                            self.moved = True


                    if not self.downWall and not self.moved:
                        
                        canvas.move(self.ghostPellet,0,1)

                        if 1 == 1:

                            self.direction = 'Down'
                            self.moved = True


                elif 116 < self.X:

                    if not self.leftWall:

                        self.ghostChoice = random.choice(self.choicesNegative)
                        canvas.move(self.ghostPellet,-1,0)

                        if -1 == -1:

                            self.direction = 'Left'
                            self.moved = True

                    if not self.upWall and not self.moved:
                        
                        canvas.move(self.ghostPellet,0,-1)
                        self.moved = True

                    if not self.rightWall and not self.moved:
                        
                        canvas.move(self.ghostPellet,1,0)

                        if 1 == 1:

                            self.direction = 'Right'
                            self.moved = True

                    if not self.downWall and not self.moved:
                        
                        canvas.move(self.ghostPellet,0,1)

                        if 1 == 1:

                            self.direction = 'Down'
                            self.moved = True

                else:

                    if not self.upWall:

                        canvas.move(self.ghostPellet,0,-1)
                        self.moved = True

                    if not self.downWall and not self.moved:
                        
                        canvas.move(self.ghostPellet,0,1)

                        if 1 == 1:

                            self.direction == 'Down'
                            self.moved = True

                    if not self.leftWall and not self.moved:
                        
                        canvas.move(self.ghostPellet,-1,0)

                        if -1 == -1:

                            self.direction = 'Left'
                            self.moved = True

                    if not self.rightWall and not self.moved:
                        
                        canvas.move(self.ghostPellet,1,0)

                        if 1 == 1:

                            self.direction = 'Right'
                            self.moved = True

            if self.X == 116 and self.Y == 152:

                self.reachedBox = True
                self.die = False
                self.state = 1
                
                if bigPelletTimer != 0:

                    self.alreadyDied = True
                    
                self.speed = ghostSpeed

        elif not pacDead and not self.leftBox and not newLevel:

            self.X, self.Y = canvas.coords(self.ghostPellet)

            if self.Y != 127:

                canvas.move(self.ghostPellet,0,-1)
                self.direction = 'Up'

            else:

                self.leftBox = True

        if not pacDead and not self.leftBox and not newLevel:

            canvas.after(self.speed,self.DieMoveGhost)

        else:

            self.MoveGhost()
            self.reachedBox = False
            self.leftBox = False

        
    def Restart(self):

        self.X, self.Y = canvas.coords(self.ghostPellet)
        self.state = 1
        self.die = False
        self.alreadyDied = False
        canvas.move(self.ghostPellet,(self.originalX - self.X),(self.originalY - self.Y))
        self.direction = 'Down'
        self.trapped = True
        self.AnimateGhost()
        self.StartMoveGhost()
        canvas.tag_raise(self.ghostPellet)

Blinky = Ghosts('Red')
Pinky = Ghosts('Pink')
Inky = Ghosts('Blue')
Clyde = Ghosts('Yellow')



def PelletMaker(size, space, direction, num, pelletX, pelletY):

    for pellet in range(num):

        Pellet1 = canvas.create_oval(pelletX,pelletY + 10,(pelletX+size-2),(pelletY+size-2) + 10, fill='white')
        Pellet2 = canvas.create_oval(Canvas_Width-pelletX,pelletY + 10,Canvas_Width-(pelletX+size-2),(pelletY+size-2) + 10, fill='white')

        canvas.tag_lower(Pellet1)
        canvas.tag_lower(Pellet2)
                
        overlap1 = list(canvas.find_overlapping(pelletX,pelletY + 10,(pelletX+size-2),(pelletY+size-2) + 10))
        overlap2 = list(canvas.find_overlapping(Canvas_Width-pelletX,pelletY + 10,Canvas_Width-(pelletX+size-2),(pelletY+size-2) + 10))

        if direction == 1:
            
            pelletX += size + space
            
        if direction == 0:
            
            pelletY += size + space


        for item in range(len(overlap1)):

            if item != 0:

                canvas.delete(overlap1[item])

        for item in range(len(overlap2)):

            if item != 0:

                canvas.delete(overlap2[item])

TotalPellets = 172

def CreatePellets():

    global bigPellet1
    global bigPellet2
    global bigPellet3
    global bigPellet4
    global bigPelletNumList
    global playerLevelNumber
    
    PelletMaker(5,6,0,6,11,34)
    PelletMaker(5,5,1,10,11,34)
    PelletMaker(5,5,1,5,11,67)
    PelletMaker(5,8,1,4,61,67)
    PelletMaker(5,6,0,16,51,34)
    PelletMaker(5,7,0,2,51,210)
    PelletMaker(5,7,0,1,51,235)
    PelletMaker(5,6,0,3,74,67)
    PelletMaker(5,8,1,3,74,89)
    PelletMaker(5,5,1,4,11,89)
    PelletMaker(5,6,0,4,101,34)
    PelletMaker(5,5,1,1,113,67)
    PelletMaker(5,5,1,4,11,188)
    PelletMaker(5,6,0,3,11,188)
    PelletMaker(5,9,1,3,11,235)
    PelletMaker(5,9,1,2,11,210)
    PelletMaker(5,7,0,2,25,210)
    PelletMaker(5,7,1,5,51,188)
    PelletMaker(5,6,0,2,100,188)
    PelletMaker(5,7,1,5,51,210)
    PelletMaker(5,7,0,3,11,235)
    PelletMaker(5,5,1,10,11,259)
    PelletMaker(5,5,1,1,113,259)
    PelletMaker(5,7,0,2,75,210)
    PelletMaker(5,7,1,3,75,235)
    PelletMaker(5,7,0,2,100,235)

    for pelletItem in canvas.find_overlapping(222,42,212,52):

        if pelletItem != 417:

            canvas.delete(pelletItem)

    for pelletItem in canvas.find_overlapping(18,42,8,52):

        if pelletItem != 417:

            canvas.delete(pelletItem)

    for pelletItem in canvas.find_overlapping(18,227,8,217):

        if pelletItem != 417:

            canvas.delete(pelletItem)

    for pelletItem in canvas.find_overlapping(222,227,212,217):

        if pelletItem != 417:

            canvas.delete(pelletItem)

    bigPellet1 = canvas.create_oval(18,42,8,52, fill='white')
    bigPellet2 = canvas.create_oval(222,42,212,52, fill='white')
    bigPellet3 = canvas.create_oval(18,227,8,217, fill='white')
    bigPellet4 = canvas.create_oval(222,227,212,217, fill='white')

    bigPelletNumList = []

    for x in canvas.find_overlapping(18,42,8,52):

        if x != 417:

            bigPelletNumList.append(x)
        
    for x in canvas.find_overlapping(222,42,212,52):

        if x != 417:

            bigPelletNumList.append(x)

    for x in canvas.find_overlapping(18,227,8,217):

        if x != 417:

            bigPelletNumList.append(x)

    for x in canvas.find_overlapping(222,227,212,217):

        if x != 417:

            bigPelletNumList.append(x)

    cover = canvas.create_rectangle(-1,0,Canvas_Width+1, Canvas_height, fill='black')
    canvas.tag_lower(cover)

CreatePellets()
MovePac()
AnimateBigPellet()

root.mainloop()
