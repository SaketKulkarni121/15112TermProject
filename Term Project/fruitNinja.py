from cmu_graphics import *
import cv2
import mediapipe
from PIL import Image
import time
import math

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
    def __init__(self, score, lives, showTime, timeLimit):
        app.score = 0
        app.lives = lives
        app.timer = timeLimit
        app.showTimer = showTime

        # px, py = app.fruits[0].getPos()
        # drawImage(CMUImage(app.fruits[0].getFruit()), px, py)

    def spawnFruit():
        pass

    def moveFruit():
        pass

    def checkCollision():
        pass

    def updateScore():
        pass

    def updateLives():
        pass

    def endGame():
        pass
        
class fruit:
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

        self.speed = speed
        self.angle = angle
        self.xPosition = startXPos
        self.yPosition = app.height

    def getPos(self):
        self.xPosition = self.speed * math.cos(math.radians(self.angle)) + self.xPosition
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

    def drawClassicModeScreen(app, board):
        drawImage(CMUImage(board.getBackground()), 0, 0, width = app.width, height = app.height)
        drawImage(CMUImage(board.getScore()), 0, 0)
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

        if app.showTimer:
            drawLabel(app.timer, app.width//2, 25, fill = "white", font = "montserrat", size = 70)



def onAppStart(app):
    app.mouseX = 0
    app.mouseY = 0
    app.showSplashScreen = True
    app.showSelectScreen = False

    app.classicGameMode = False
    app.arcadeGameMode = False
    app.zenGameMode = False

    app.startButton = Button(app.width//2, app.height//2, app.width//2 - 100, 50, "gray","white", "Start Game", 30)
    
    app.classicButton = Button(app.width//4, app.height//2, app.width//4 - 100, 50, "gray","white", "Classic Mode", 30)
    app.arcadeButton = Button(2 * app.width//4, app.height//2, app.width//4 - 100, 50, "gray","white", "Arcade Mode", 30)
    app.zenButton = Button(3 * app.width//4, app.height//2, app.width//4 - 100, 50, "gray","white", "Zen Mode", 30)

    app.score = 0
    app.lives = 3
    app.difficultyLevel = "Easy"

    app.showTimer = True
    app.timer = time.strftime("%H:%M:%S", time.localtime())

    app.fruits = [fruit(app, "apple", app.width//2, 14, 90)]

def onStep(app):
    app.timer = time.strftime("%H:%M:%S", time.localtime())

def onMousePress(app, mouseX, mouseY):
    (app.mouseX, app.mouseY) = (mouseX, mouseY)

    if app.startButton.isClicked(app) and app.showSplashScreen:
        app.showSplashScreen = False
        app.showSelectScreen = True

    elif app.classicButton.isClicked(app) and app.showSelectScreen:
        app.showSelectScreen = False
        app.classicGameMode = True

    elif app.arcadeButton.isClicked(app) and app.showSelectScreen:
        app.showSelectScreen = False
        app.arcadeGameMode = True

    elif app.zenButton.isClicked(app) and app.showSelectScreen:
        app.showSelectScreen = False
        app.zenGameMode = True


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
    else:
        drawRect(0, 0, app.width, app.height, fill = "blue")

def main():
    runApp(1200, 600)

if __name__ == '__main__':
    main()  