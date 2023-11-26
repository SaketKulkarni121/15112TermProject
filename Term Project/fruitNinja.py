from cmu_graphics import *
import cv2
import mediapipe
from PIL import Image

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
        
class fruit:
    def getFruit(fruit):
        if fruit == "apple":
            return Image.open("images/fruitImages/apple.png").resize((50, 50))
        elif fruit == "watermelon":
            return Image.open("images/fruitImages/watermelon.png").resize((50, 50))
        elif fruit == "banana":
            return Image.open("images/fruitImages/banana.png").resize((50, 50))
    
class board:
    def getBackground():
       return Image.open("images/background.png")
    
    def getLogo():
        img = Image.open("images/logo.png")
        return img.resize((700, 120), Image.BICUBIC)

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

def onMousePress(app, mouseX, mouseY):
    (app.mouseX, app.mouseY) = (mouseX, mouseY)

    if app.startButton.isClicked(app):
        app.showSplashScreen = False
        app.showSelectScreen = True

    if app.classicButton.isClicked(app):
        app.showSelectScreen = False
        app.classicGameMode = True

    if app.arcadeButton.isClicked(app):
        app.showSelectScreen = False
        app.arcadeGameMode = True

    if app.zenButton.isClicked(app):
        app.showSelectScreen = False
        app.zenGameMode = True
        

def redrawAll(app):
    if app.showSplashScreen:
        board.drawSplashScreen(app, board)
    elif app.showSelectScreen:
        board.drawGameSelectScreen(app, board)
    elif app.classicGameMode or app.arcadeGameMode or app.zenGameMode:
        board.drawClassicModeScreen(app, board)
    else:
        drawRect(0, 0, app.width, app.height, fill = "blue")

def main():
    runApp(1200, 600)

if __name__ == '__main__':
    main()  