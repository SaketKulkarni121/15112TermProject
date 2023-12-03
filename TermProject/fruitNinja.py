from cmu_graphics import *
import cv2
import mediapipe
from PIL import Image
import math
import random

#High Score list

def getHandPosition(app):
    __, image = app.video.read()
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = app.hands.process(imageRGB)

    if result.multi_hand_landmarks:
        for handNum, hand in enumerate(result.multi_hand_landmarks):
            for id, landmark in enumerate(hand.landmark):
                if id == 8:
                    cx, cy = app.width -  int(landmark.x * app.width), int(landmark.y * app.height)
                    if handNum == 0:
                        app.mouseX, app.mouseY = (cx, cy)
                    else:
                        app.mouseX2, app.mouseY2 = (cx, cy)


class Button:
    def __init__(self, centerX, centerY, width, height, fillColor, textColor, text, textSize):
        self.centerX = centerX
        self.centerY = centerY
        self.width = width
        self.height = height
        self.fillColor = fillColor
        self.textColor = textColor
        self.text = text
        self.textSize = textSize

    def getButton(self):
        drawCircle(self.centerX + self.width//2, self.centerY, self.height//2, fill = self.fillColor)
        drawCircle(self.centerX - self.width//2, self.centerY, self.height//2, fill = self.fillColor)
        drawRect(self.centerX - self.width//2, self.centerY- self.height//2, self.width, self.height, fill = self.fillColor)
        drawLabel(self.text, self.centerX, self.centerY, fill = self.textColor, font = "montserrat", align = "center", size = self.textSize)

    def isClicked(self, app):
        if (app.mouseX < self.centerX + self.width//2 + self.height//2) and (app.mouseX > self.centerX - self.width//2 and self.height//2) \
            and (app.mouseY < self.centerY + self.height//2 + self.height//2) and (app.mouseY > self.centerY - self.height//2 and self.height//2): 
                return True
        

class Game:
    def __init__(self, app, lives, showTime, timeLimit, difficultyLevel):
        app.score = 0
        app.lives = lives
        app.seconds = timeLimit
        app.showTimer = showTime
        app.difficultyLevel = difficultyLevel
        app.paused = False

    def spawnFruit(app):
        fruits = ["apple", "banana", "coconut", "kiwi", "mango", "pineapple", "strawberry", "watermelon", "bomb"]
        fruit = fruits[random.randint(0, len(fruits) - 1)]
        startX = random.randint(0, app.width-100)
        if startX < 400:
            app.fruits.append(Fruit(app, fruit, startX, random.randint(20, 24), random.randint(50, 80)))
        elif startX > app.width - 400:
            app.fruits.append(Fruit(app, fruit, startX, random.randint(20, 24), random.randint(100, 130)))
        else: app.fruits.append(Fruit(app, fruit, startX, random.randint(20, 24), random.randint(60, 120)))

    def moveFruit(app):
        for fruit in app.fruits:
            px, py = fruit.getPos()
            drawImage(CMUImage(fruit.getFruit()), px, py)

    def checkCollision(app):
        for fruit in app.fruits:
            if fruit.yPosition > app.height:
                app.fruits.remove(fruit)
                if fruit.fruit != "bomb":
                    app.lives -= 1
            elif fruit.xPosition < 0 or fruit.xPosition > app.width:
                app.fruits.remove(fruit)
                if fruit.fruit != "bomb":
                    app.lives -= 1
            elif app.mouseX < fruit.xPosition + 100 and app.mouseX > fruit.xPosition\
                and app.mouseY < fruit.yPosition + 100 and app.mouseY > fruit.yPosition:
                if fruit.fruit == "bomb":
                    app.lives -= 1
                else:
                    if app.mouseX < fruit.xPosition + 60 and app.mouseX > fruit.xPosition + 40\
                        or app.mouseY < fruit.yPosition + 40  and app.mouseY > fruit.yPosition + 60:
                            app.score += app.additionalPoints + 15
                    elif app.mouseX < fruit.xPosition + 80 and app.mouseX > fruit.xPosition + 20\
                        or app.mouseY < fruit.yPosition + 40  and app.mouseY > fruit.yPosition + 60:
                            app.score += app.additionalPoints + 10
                    else:
                        app.score += app.additionalPoints
                    if app.arcadeGameMode:
                        app.seconds += 1
                app.fruits.remove(fruit)
            
class Fruit:
    def __init__(self, app, fruit, startXPos, speed, angle):
        self.fruit = fruit
        self.weight = 1.8

        self.speed = speed
        self.xSpeed = speed
        self.angle = angle
        self.xPosition = startXPos
        self.yPosition = app.height

    def getPos(self):
        self.xPosition = self.xSpeed * math.cos(math.radians(self.angle)) + self.xPosition
        self.yPosition = self.yPosition - ((self.speed * math.sin(math.radians(self.angle))) * self.weight)
        self.speed -= 0.5 * self.weight
        return self.xPosition, self.yPosition

    def getFruit(self):
        if self.fruit == "apple":
            return Image.open("/Users/saket/Documents/CMU/15112/15112TermProject/TermProject/images/fruitImages/apple.png").resize((75, 75))
        elif self.fruit == "banana":
            return Image.open("/Users/saket/Documents/CMU/15112/15112TermProject/TermProject/images/fruitImages/banana.png").resize((100, 100))
        elif self.fruit == "coconut":
            return Image.open("/Users/saket/Documents/CMU/15112/15112TermProject/TermProject/images/fruitImages/coconut.png").resize((100, 100))
        elif self.fruit == "kiwi":
            return Image.open("/Users/saket/Documents/CMU/15112/15112TermProject/TermProject/images/fruitImages/kiwi.png").resize((60, 60))
        elif self.fruit == "mango":
            return Image.open("/Users/saket/Documents/CMU/15112/15112TermProject/TermProject/images/fruitImages/mango.png").resize((75, 75))
        elif self.fruit == "pineapple":
            return Image.open("/Users/saket/Documents/CMU/15112/15112TermProject/TermProject/images/fruitImages/pineapple.png").resize((100, 100))
        elif self.fruit == "strawberry":
            return Image.open("/Users/saket/Documents/CMU/15112/15112TermProject/TermProject/images/fruitImages/strawberry.png").resize((50, 50))
        elif self.fruit == "watermelon":
            return Image.open("/Users/saket/Documents/CMU/15112/15112TermProject/TermProject/images/fruitImages/watermelon.png").resize((100, 100))
        elif self.fruit == "bomb":
            return Image.open("/Users/saket/Documents/CMU/15112/15112TermProject/TermProject/images/bomb.png").resize((100, 100))
        
    
class screen:
    def getBackground():
        return Image.open("/Users/saket/Documents/CMU/15112/15112TermProject/TermProject//images/background.png")
    
    def getLogo():
        img = Image.open("/Users/saket/Documents/CMU/15112/15112TermProject/TermProject/images/logo.png")
        return img.resize((700, 120), Image.BICUBIC)
    
    def getScore():
        return Image.open("/Users/saket/Documents/CMU/15112/15112TermProject/TermProject/images/score.png").resize((100, 50), Image.BICUBIC)
    
    def getEmptyCross():
        return Image.open("/Users/saket/Documents/CMU/15112/15112TermProject/TermProject/images/emptyCross.png").resize((65, 50), Image.BICUBIC)

    def getFullCross():
        return Image.open("/Users/saket/Documents/CMU/15112/15112TermProject/TermProject/images/fullCross.png").resize((65, 50), Image.BICUBIC)

    def drawSplashScreen(app, board):
        drawImage(CMUImage(board.getBackground()), 0, 0, width = app.width, height = app.height)
        drawImage(CMUImage(board.getLogo()), app.width//2 - 350, app.height//2 -150)
        app.startButton.getButton()
    
    def drawGameSelectScreen(app, board):
        drawImage(CMUImage(board.getBackground()), 0, 0, width = app.width, height = app.height)
        drawImage(CMUImage(board.getLogo()), app.width//2 - 350, app.height//2 -150)
        app.classicButton.getButton()
        app.arcadeButton.getButton()
        app.zenButton.getButton()
        app.multiplayerButton.getButton()
        app.useHandsButton.fillColor = app.usingHandsFill
        app.useHandsButton.getButton()
        app.showHighScores.getButton()

    def drawClassicModeScreen(app, board):
        drawImage(CMUImage(board.getBackground()), 0, 0, width = app.width, height = app.height)
        drawImage(CMUImage(board.getScore()), 0, 0)
        drawLabel(app.difficultyLevel, app.width//3, 25, fill = "white", font = "montserrat", size = 50)
        drawRect(0, 0, app.width, app.height, fill = "black", opacity = app.pausedOpacity)

        if app.pausedOpacity == 50:
            app.quitGameButton.getButton()
        

        app.pauseGameButton.fillColor = app.pausedFill
        app.pauseGameButton.getButton()
        drawCircle(app.mouseX, app.mouseY, 15, fill = "blue")
        if app.multiplayerGameMode:
            drawCircle(app.mouseX2, app.mouseY2, 15, fill = "red")

        drawLabel(app.score, 200, 25, fill = "white", font = "montserrat", size = 70)
        if app.lives == 0:
            drawImage(CMUImage(board.getFullCross()), app.width - 50, 0)
            drawImage(CMUImage(board.getFullCross()), app.width - 100, 0)
            drawImage(CMUImage(board.getFullCross()), app.width - 150, 0)
        elif app.lives == 1:
            drawImage(CMUImage(board.getFullCross()), app.width - 50, 0)
            drawImage(CMUImage(board.getFullCross()), app.width - 100, 0)
            drawImage(CMUImage(board.getEmptyCross()), app.width - 150, 0)
        elif app.lives == 2:
            drawImage(CMUImage(board.getFullCross()), app.width - 50, 0)
            drawImage(CMUImage(board.getEmptyCross()), app.width - 100, 0)
            drawImage(CMUImage(board.getEmptyCross()), app.width - 150, 0)
        elif app.lives == 3:
            drawImage(CMUImage(board.getEmptyCross()), app.width - 50, 0)
            drawImage(CMUImage(board.getEmptyCross()), app.width - 100, 0)
            drawImage(CMUImage(board.getEmptyCross()), app.width - 150, 0)

        if not app.paused:
            Game.moveFruit(app)     

        if app.showTimer:
            drawLabel(app.timer, app.width//2, 25, fill = "white", font = "montserrat", size = 70)

    def drawAppEndScreen(app, board):
        drawImage(CMUImage(board.getBackground()), 0, 0, width = app.width, height = app.height)
        drawImage(CMUImage(board.getLogo()), app.width//2 - 350, app.height//2 -150)
        drawLabel("Game Over", app.width//2, app.height//2, fill = "white", font = "montserrat", size = 70)
        drawLabel("Score: " + str(app.score), app.width//2, app.height//2 + 100, fill = "white", font = "montserrat", size = 70)
        app.resetButton.getButton()

    def drawHighScore(app, board):
        drawImage(CMUImage(board.getBackground()), 0, 0, width = app.width, height = app.height)
        drawImage(CMUImage(board.getLogo()), app.width//2 - 350, app.height//3 -150)
        app.goBackToSelectScreen.getButton()



def onAppStart(app):
    app.mouseX = 0
    app.mouseY = 0
    app.mouseX2 = 0
    app.mouseY2 = 0
    app.showSplashScreen = True
    app.showSelectScreen = False

    app.classicGameMode = False
    app.arcadeGameMode = False
    app.zenGameMode = False
    app.multiplayerGameMode = False

    app.endGameScreen = False
    app.showHighScoreScreen = False
    app.gamePaused = False
    
    app.pausedFill = "gray"
    app.pausedOpacity = 0
    app.usingHandsFill = "gray"

    app.startButton = Button(app.width//2, app.height//2, app.width//2 - 100, 50, "gray","white", "Start Game", 30)
    
    app.classicButton = Button(app.width//5, app.height//2, app.width//5 - 100, 50, "gray","white", "Classic Mode", 30)
    app.arcadeButton = Button(2 * app.width//5, app.height//2, app.width//5 - 100, 50, "gray","white", "Arcade Mode", 30)
    app.zenButton = Button(3 * app.width//5, app.height//2, app.width//5 - 100, 50, "gray","white", "Zen Mode", 30)
    app.multiplayerButton = Button(4 * app.width//5, app.height//2 , app.width//5 - 100, 50, "gray","white", "Multiplayer", 30)
    app.useHandsButton = Button(app.width//2, app.height//2 + 100, app.width//2 - 100, 50, app.usingHandsFill, "white", "Use Hands", 30)
    app.showHighScores = Button(app.width//2, app.height//2 + 175, app.width//2 - 100, 50, "gray","white", "High Scores", 30)


    app.resetButton = Button(app.width//2, app.height//2 + 200, app.width//2 - 100, 50, "gray","white", "Reset Game", 30)
    app.goBackToSelectScreen = Button(85, 50, 85, 50, "gray","white", "Go Back", 30)

    app.pauseGameButton = Button(app.width//2 + 150, 30, 50, 50, "gray","white", "Pause", 30)
    app.quitGameButton = Button(app.width//2, app.height//2, 50, 50, "gray","white", "Quit", 30)

    app.score = 0
    app.lives = 3
    app.difficultyLevel = "Easy"

    app.showTimer = True
    app.timer = "0:00"

    app.steps = 0
    app.seconds = 90

    app.fruits = []
    app.stepsPerSecond = 30

    app.spawnsPerTick = 40
    app.numOfSpawns = 1
    app.additionalPoints = 10

    app.useHands = False
    app.video = None
    app.hands = None

    app.paused = False
    app.clearedBoard = 0


def onStep(app):
    app.steps += 1
    if app.fruits == []:
        app.clearedBoard += 1
    if app.clearedBoard == 300:
        app.clearedBoard = 0
        app.additionalPoints += 3
        app.spawnsPerTick -= 3
    if app.paused:
        return
    if app.useHands:
        if app.video == None and app.hands == None:
            app.video = cv2.VideoCapture(0)
            app.hands = mediapipe.solutions.hands.Hands()
        if app.steps % 1 == 0:
            getHandPosition(app)
    else:
        if app.video != None and app.hands != None:
            cv2.VideoCapture.release(app.video)
            app.video = None
            app.hands = None

    if app.classicGameMode and not app.paused:
        if app.steps % 30 == 0:
            mins, secs = divmod(app.seconds, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            app.seconds -= 1
            app.timer = timeformat
        if app.seconds == 0:
            app.paused = True
            app.endGameScreen = True
            app.classicGameMode = False
        if app.steps % app.spawnsPerTick == 0:
            for _ in range(app.numOfSpawns):
                Game.spawnFruit(app)
        Game.checkCollision(app) 

        if app.lives == 0:
            app.paused = True
            app.endGameScreen = True
            app.classicGameMode = False

        if app.score < 100:
            app.spawnsPerTick = 40
            app.difficultyLevel = "Easy"
            app.numOfSpawns = 1
            app.additonalPoints = 5
        elif app.score < 300:
            app.spawnsPerTick = 40
            app.difficultyLevel = "Medium"
            app.numOfSpawns = 2
            app.additonalPoints = 10
        elif app.score < 700:
            app.spawnsPerTick = 30
            app.difficultyLevel = "Hard"
            app.numOfSpawns = 3
            app.additionalPoints = 12
        elif app.score < 1200:
            app.spawnsPerTick = 30
            app.difficultyLevel = "Insane"
            app.numOfSpawns = 4
            app.additionalPoints = 18
        elif app.score < 1800:
            app.spawnsPerTick = 20
            app.difficultyLevel = "Impossible"
            app.numOfSpawns = 5
            app.additionalPoints = 22
        elif app.score < 3000:
            app.spawnsPerTick = 10
            app.difficultyLevel = "God Mode"
            app.numOfSpawns = 6
            app.additionalPoints = 26

    if app.arcadeGameMode and not app.paused:
        if app.steps % 30 == 0:
            mins, secs = divmod(app.seconds, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            app.seconds -= 1
            app.timer = timeformat
        if app.seconds == 0:
            app.paused = True
            app.endGameScreen = True
            app.classicGameMode = False
        if app.steps % app.spawnsPerTick == 0:
            for _ in range(app.numOfSpawns):
                Game.spawnFruit(app)
        Game.checkCollision(app) 

        if app.lives == 0:
            app.paused = True
            app.endGameScreen = True
            app.arcadeGameMode = False

        
        if app.score < 100:
            app.spawnsPerTick = 40
            app.difficultyLevel = "Easy"
            app.numOfSpawns = 1
            app.additonalPoints = 5
        elif app.score < 300:
            app.spawnsPerTick = 40
            app.difficultyLevel = "Medium"
            app.numOfSpawns = 2
            app.additonalPoints = 10
        elif app.score < 700:
            app.spawnsPerTick = 30
            app.difficultyLevel = "Hard"
            app.numOfSpawns = 3
            app.additionalPoints = 12
        elif app.score < 1200:
            app.spawnsPerTick = 30
            app.difficultyLevel = "Insane"
            app.numOfSpawns = 4
            app.additionalPoints = 18
        elif app.score < 1800:
            app.spawnsPerTick = 20
            app.difficultyLevel = "Impossible"
            app.numOfSpawns = 5
            app.additionalPoints = 22
        elif app.score < 3000:
            app.spawnsPerTick = 10
            app.difficultyLevel = "God Mode"
            app.numOfSpawns = 6
            app.additionalPoints = 26

    if app.zenGameMode and not app.paused:
        if app.steps % app.spawnsPerTick == 0:
            for _ in range(app.numOfSpawns):
                Game.spawnFruit(app)
        Game.checkCollision(app) 

        if app.lives == 0:
            app.paused = True
            app.endGameScreen = True
            app.zenGameMode = False
    
        app.spawnsPerTick = 40
        app.difficultyLevel = "ZEN"
        app.numOfSpawns = 2
        app.additonalPoints = 10


def onMousePress(app, mouseX, mouseY):
    (app.mouseX, app.mouseY) = (mouseX, mouseY)

    if app.startButton.isClicked(app) and app.showSplashScreen:
        app.showSplashScreen = False
        app.showSelectScreen = True

    elif app.useHandsButton.isClicked(app) and app.showSelectScreen:
        app.useHands = not app.useHands
        if app.useHands:
            app.usingHandsFill = "green"
        else:
            app.usingHandsFill = "gray"

    elif app.classicButton.isClicked(app) and app.showSelectScreen:
        app.showSelectScreen = False
        app.classicGameMode = True
        Game(app, 3, True, 90, "Easy")

    elif app.showHighScores.isClicked(app) and app.showSelectScreen:
        app.showSelectScreen = False
        app.showHighScoreScreen = True


    elif app.arcadeButton.isClicked(app) and app.showSelectScreen:
        app.showSelectScreen = False
        app.arcadeGameMode = True
        Game(app, 3, True, 30, "Easy")

    elif app.zenButton.isClicked(app) and app.showSelectScreen:
        app.showSelectScreen = False
        app.zenGameMode = True
        Game(app, 3, False, 90, "Easy")

    elif app.multiplayerButton.isClicked(app) and app.showSelectScreen:
        app.showSelectScreen = False
        app.multiplayerGameMode = True
        Game(app, 3, True, 90, "Easy")

    elif app.resetButton.isClicked(app) and app.endGameScreen:
        app.showSplashScreen = True
        app.endGameScreen = False
        app.classicGameMode = False
        app.showSelectScreen = False
        onAppStart(app)

    elif app.quitGameButton.isClicked(app) and app.classicGameMode and app.paused:
        app.showSplashScreen = True
        app.classicGameMode = False
        app.showSelectScreen = False
        onAppStart(app)

    elif app.pauseGameButton.isClicked(app) and app.classicGameMode:
        app.paused = not app.paused
        if app.paused:
            app.pausedFill = "green"
            app.pausedOpacity = 50
        else:
            app.pausedFill = "gray"
            app.pausedOpacity = 0

    

    elif app.goBackToSelectScreen.isClicked(app) and app.showHighScoreScreen:
        app.showHighScoreScreen = False
        app.showSelectScreen = True

def onMouseDrag(app, mouseX, mouseY):
    (app.mouseX, app.mouseY) = (mouseX, mouseY)


def redrawAll(app):
    if app.showSplashScreen:
        screen.drawSplashScreen(app, screen)
    elif app.showSelectScreen:
        screen.drawGameSelectScreen(app, screen)
    elif app.classicGameMode:
        screen.drawClassicModeScreen(app, screen)
    elif app.arcadeGameMode:
        screen.drawClassicModeScreen(app, screen)
    elif app.zenGameMode:
        screen.drawClassicModeScreen(app, screen)
    elif app.endGameScreen:
        screen.drawAppEndScreen(app, screen)
    elif app.multiplayerGameMode:
        screen.drawClassicModeScreen(app, screen)
    elif app.showHighScoreScreen:
        screen.drawHighScore(app, screen)

def main():
    runApp(1200, 600)

if __name__ == '__main__':
    main()  