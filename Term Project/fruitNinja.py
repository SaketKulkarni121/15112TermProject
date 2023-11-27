from cmu_graphics import *
import cv2
import mediapipe
from PIL import Image
import math
import random


def getHandPosition(app):
    __, image = app.video.read()
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = app.hands.process(imageRGB)

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            for id, landmark in enumerate(hand.landmark):
                w, h = 1200, 600
                cx, cy = w -  int(landmark.x * w), int(landmark.y * h)

                if id == 8:
                    app.mouseX, app.mouseY = (cx, cy)


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
        app.fruits.append(Fruit(app, fruit, random.randint(0, app.width-100), random.randint(11, 18), random.randint(30, 150)))

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
                    app.score += app.additionalPoints
                    if app.arcadeGameMode:
                        app.seconds += 5
                app.fruits.remove(fruit)
            
class Fruit:
    def __init__(self, app, fruit, startXPos, speed, angle):
        self.fruit = fruit

        if self.fruit == "apple":
            self.weight = 1.1
        elif self.fruit == "banana":
            self.weight = 1.3
        elif self.fruit == "coconut":
            self.weight = 1.5
        elif self.fruit == "kiwi":
            self.weight = 1
        elif self.fruit == "mango":
            self.weight = 1.5
        elif self.fruit == "pineapple":
            self.weight = 1.7
        elif self.fruit == "strawberry":
            self.weight = 0.9
        elif self.fruit == "watermelon":
            self.weight = 2
        elif self.fruit == "bomb":
            self.weight = 1.5

        self.speed = speed
        self.xSpeed = speed
        self.angle = angle
        self.xPosition = startXPos
        self.yPosition = app.height

    def getPos(self):
        self.xPosition = self.xSpeed * math.cos(math.radians(self.angle)) + self.xPosition
        self.yPosition = self.yPosition - ((self.speed * math.sin(math.radians(self.angle))) * self.weight)
        self.speed -= 0.2 * self.weight
        return self.xPosition, self.yPosition

    def getFruit(self):
        if self.fruit == "apple":
            return Image.open("images/fruitImages/apple.png").resize((75, 75))
        elif self.fruit == "banana":
            return Image.open("images/fruitImages/banana.png").resize((100, 100))
        elif self.fruit == "coconut":
            return Image.open("images/fruitImages/coconut.png").resize((100, 100))
        elif self.fruit == "kiwi":
            return Image.open("images/fruitImages/kiwi.png").resize((60, 60))
        elif self.fruit == "mango":
            return Image.open("images/fruitImages/mango.png").resize((75, 75))
        elif self.fruit == "pineapple":
            return Image.open("images/fruitImages/pineapple.png").resize((100, 100))
        elif self.fruit == "strawberry":
            return Image.open("images/fruitImages/strawberry.png").resize((50, 50))
        elif self.fruit == "watermelon":
            return Image.open("images/fruitImages/watermelon.png").resize((100, 100))
        elif self.fruit == "bomb":
            return Image.open("images/bomb.png").resize((100, 100))
        
    
class screen:
    def getBackground():
       return Image.open("images/background.png")
    
    def getLogo():
        img = Image.open("images/logo.png")
        return img.resize((700, 120), Image.BICUBIC)
    
    def getScore():
        return Image.open("images/score.png").resize((100, 50), Image.BICUBIC)
    
    def getEmptyCross():
        return Image.open("images/emptyCross.png").resize((65, 50), Image.BICUBIC)

    def getFullCross():
        return Image.open("images/fullCross.png").resize((65, 50), Image.BICUBIC)

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
        app.useHandsButton.getButton()

    def drawClassicModeScreen(app, board):
        drawImage(CMUImage(board.getBackground()), 0, 0, width = app.width, height = app.height)
        drawImage(CMUImage(board.getScore()), 0, 0)
        drawCircle(app.mouseX, app.mouseY, 15, fill = "blue")
        drawLabel(app.score, 175, 25, fill = "white", font = "montserrat", size = 70)
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



def onAppStart(app):
    app.mouseX = 0
    app.mouseY = 0
    app.showSplashScreen = True
    app.showSelectScreen = False

    app.classicGameMode = False
    app.arcadeGameMode = False
    app.zenGameMode = False

    app.endGameScreen = False

    app.startButton = Button(app.width//2, app.height//2, app.width//2 - 100, 50, "gray","white", "Start Game", 30)
    
    app.classicButton = Button(app.width//4, app.height//2, app.width//4 - 100, 50, "gray","white", "Classic Mode", 30)
    app.arcadeButton = Button(2 * app.width//4, app.height//2, app.width//4 - 100, 50, "gray","white", "Arcade Mode", 30)
    app.zenButton = Button(3 * app.width//4, app.height//2, app.width//4 - 100, 50, "gray","white", "Zen Mode", 30)
    app.useHandsButton = Button(app.width//2, app.height//2 + 100, app.width//2 - 100, 50, "gray","white", "Use Hands", 30)

    app.resetButton = Button(app.width//2, app.height//2 + 200, app.width//2 - 100, 50, "gray","white", "Reset Game", 30)

    app.score = 0
    app.lives = 3
    app.difficultyLevel = "Easy"

    app.showTimer = True
    app.timer = "0:00"

    app.steps = 0
    app.seconds = 90

    app.fruits = []
    app.stepsPerSecond = 30

    app.spawnsPerTick = 60
    app.numOfSpawns = 1
    app.additionalPoints = 10

    app.useHands = False

    app.paused = False

def onStep(app):
    app.steps += 1

    if app.useHands:
        app.video = cv2.VideoCapture(0)
        app.hands = mediapipe.solutions.hands.Hands()
        getHandPosition(app)

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

        if app.score == 100:
            app.spawnsPerTick = 50
            app.difficultyLevel = "Medium"
            app.numOfSpawns = 2
            app.additonalPoints = 20
        elif app.score == 200:
            app.spawnsPerTick = 40
            app.difficultyLevel = "Hard"
            app.numOfSpawns = 3
            app.additionalPoints = 30
        elif app.score == 300:
            app.spawnsPerTick = 30
            app.difficultyLevel = "Insane"
            app.numOfSpawns = 4
            app.additionalPoints = 40
        elif app.score == 400:
            app.spawnsPerTick = 20
            app.difficultyLevel = "Impossible"
            app.numOfSpawns = 5
            app.additionalPoints = 50
        elif app.score == 500:
            app.spawnsPerTick = 10
            app.difficultyLevel = "God Mode"
            app.numOfSpawns = 6
            app.additionalPoints = 60

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
            app.classicGameMode = False

        if app.score == 100:
            app.spawnsPerTick = 50
            app.difficultyLevel = "Medium"
            app.numOfSpawns = 2
            app.additonalPoints = 20
        elif app.score == 200:
            app.spawnsPerTick = 40
            app.difficultyLevel = "Hard"
            app.numOfSpawns = 3
            app.additionalPoints = 30
        elif app.score == 300:
            app.spawnsPerTick = 30
            app.difficultyLevel = "Insane"
            app.numOfSpawns = 4
            app.additionalPoints = 40
        elif app.score == 400:
            app.spawnsPerTick = 20
            app.difficultyLevel = "Impossible"
            app.numOfSpawns = 5
            app.additionalPoints = 50
        elif app.score == 500:
            app.spawnsPerTick = 10
            app.difficultyLevel = "God Mode"
            app.numOfSpawns = 6
            app.additionalPoints = 60

    if app.zenGameMode and not app.paused:
        if app.steps % app.spawnsPerTick == 0:
            for _ in range(app.numOfSpawns):
                Game.spawnFruit(app)
        Game.checkCollision(app) 

        if app.lives == 0:
            app.paused = True
            app.endGameScreen = True
            app.classicGameMode = False

        
        if app.score == 100:
            app.spawnsPerTick = 50
            app.difficultyLevel = "Medium"
            app.numOfSpawns = 2
            app.additonalPoints = 20
        elif app.score == 200:
            app.spawnsPerTick = 40
            app.difficultyLevel = "Hard"
            app.numOfSpawns = 3
            app.additionalPoints = 30
        elif app.score == 300:
            app.spawnsPerTick = 30
            app.difficultyLevel = "Insane"
            app.numOfSpawns = 4
            app.additionalPoints = 40
        elif app.score == 400:
            app.spawnsPerTick = 20
            app.difficultyLevel = "Impossible"
            app.numOfSpawns = 5
            app.additionalPoints = 50
        elif app.score == 500:
            app.spawnsPerTick = 10
            app.difficultyLevel = "God Mode"
            app.numOfSpawns = 6
            app.additionalPoints = 60

def onMousePress(app, mouseX, mouseY):
    (app.mouseX, app.mouseY) = (mouseX, mouseY)

    if app.startButton.isClicked(app) and app.showSplashScreen:
        app.showSplashScreen = False
        app.showSelectScreen = True

    elif app.useHandsButton.isClicked(app) and app.showSelectScreen:
        app.useHands = True

    elif app.classicButton.isClicked(app) and app.showSelectScreen:
        app.showSelectScreen = False
        app.classicGameMode = True
        Game(app, 3, True, 90, "Easy")


    elif app.arcadeButton.isClicked(app) and app.showSelectScreen:
        app.showSelectScreen = False
        app.arcadeGameMode = True
        Game(app, 3, True, 30, "Easy")

    elif app.zenButton.isClicked(app) and app.showSelectScreen:
        app.showSelectScreen = False
        app.zenGameMode = True
        Game(app, 3, False, 90, "Easy")

    elif app.resetButton.isClicked(app) and app.endGameScreen:
        app.showSplashScreen = True
        app.endGameScreen = False
        app.classicGameMode = False
        app.showSelectScreen = False
        onAppStart(app)

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
    else:
        drawRect(0, 0, app.width, app.height, fill = "blue")

def main():
    runApp(1200, 600)

if __name__ == '__main__':
    main()  