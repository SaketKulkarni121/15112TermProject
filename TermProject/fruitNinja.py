from cmu_graphics import *
import cv2
import mediapipe
from PIL import Image
import math
import random
import os

path = os.getcwd() + "/TermProject"

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
                        if app.multiplayerGameMode:
                            app.mouseX, app.mouseY = (1.3*cx, cy)
                        else:
                            app.mouseX, app.mouseY = (cx, cy)
                    else:
                        app.mouseX2, app.mouseY2 = (1.3*cx, cy)

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
        if not app.multiplayerGameMode:
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
        else:
            for fruit in app.fruits:
                if fruit.yPosition > app.height:
                    app.fruits.remove(fruit)
                elif fruit.xPosition < 0 or fruit.xPosition > app.width:
                    app.fruits.remove(fruit)
                elif app.mouseX < fruit.xPosition + 100 and app.mouseX > fruit.xPosition\
                    and app.mouseY < fruit.yPosition + 100 and app.mouseY > fruit.yPosition:
                    if fruit.fruit == "bomb" and app.score != 0:
                        app.score -= app.additionalPoints
                    elif fruit.fruit == "bomb" and app.score == 0:
                        app.score = 0
                    elif app.mouseX < fruit.xPosition + 60 and app.mouseX > fruit.xPosition + 40\
                        or app.mouseY < fruit.yPosition + 40  and app.mouseY > fruit.yPosition + 60:
                            app.score += app.additionalPoints + 15
                    elif app.mouseX < fruit.xPosition + 80 and app.mouseX > fruit.xPosition + 20\
                        or app.mouseY < fruit.yPosition + 40  and app.mouseY > fruit.yPosition + 60:
                            app.score += app.additionalPoints + 10
                    else:
                        app.score += app.additionalPoints
                    app.fruits.remove(fruit)
                elif app.mouseX2 < fruit.xPosition + 100 and app.mouseX2 > fruit.xPosition\
                    and app.mouseY2 < fruit.yPosition + 100 and app.mouseY2 > fruit.yPosition:
                    if fruit.fruit == "bomb" and app.score2 != 0:
                        app.score2 -= app.additionalPoints
                    elif fruit.fruit == "bomb" and app.score2 == 0:
                        app.score2 = 0
                    elif app.mouseX2 < fruit.xPosition + 60 and app.mouseX2 > fruit.xPosition + 40\
                        or app.mouseY2 < fruit.yPosition + 40  and app.mouseY2 > fruit.yPosition + 60:
                            app.score2 += app.additionalPoints + 15
                    elif app.mouseX2 < fruit.xPosition + 80 and app.mouseX2 > fruit.xPosition + 20\
                        or app.mouseY2 < fruit.yPosition + 40  and app.mouseY2 > fruit.yPosition + 60:
                            app.score2 += app.additionalPoints + 10
                    else:
                        app.score2 += app.additionalPoints
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

    #To remove background: remove.bg
    def getFruit(self):
        if self.fruit == "apple":
            #Apple Image Citation: https://www.google.com/imgres?imgurl=https%3A%2F%2Fstatic-00.iconduck.com%2Fassets.00%2Fred-apple-emoji-1779x2048-aklr8hg9.png&tbnid=FNfj7qcqOKlpuM&vet=12ahUKEwj0wOCb_OqCAxU6M1kFHYpJCTcQMygEegQIARBm..i&imgrefurl=https%3A%2F%2Ficonduck.com%2Femojis%2F36145%2Fred-apple&docid=8hNCFk2muC1EjM&w=1779&h=2048&q=apple%20fruit%20emojis&ved=2ahUKEwj0wOCb_OqCAxU6M1kFHYpJCTcQMygEegQIARBm
            return Image.open(path + "/images/fruitImages/apple.png").resize((75, 75))
        elif self.fruit == "banana":
            #Banana Image Citation: https://www.google.com/imgres?imgurl=https%3A%2F%2Fcdn4.vectorstock.com%2Fi%2F1000x1000%2F34%2F63%2Fsticker-not-peeled-banana-vector-33023463.jpg&tbnid=9DbTDutcbfagkM&vet=12ahUKEwjzzq2g_uqCAxVUIWIAHU_sDIUQMygAegQIARBX..i&imgrefurl=https%3A%2F%2Fwww.vectorstock.com%2Froyalty-free-vector%2Fsticker-not-peeled-banana-vector-33023463&docid=wpwgt-A5egh5GM&w=1000&h=1080&q=single%20not%20peeled%20banana%20emoji&ved=2ahUKEwjzzq2g_uqCAxVUIWIAHU_sDIUQMygAegQIARBX
            return Image.open(path + "/images/fruitImages/banana.png").resize((100, 100))
        elif self.fruit == "coconut":
            #Coconut Image Citation: https://www.google.com/imgres?imgurl=https%3A%2F%2Fimages-wixmp-ed30a86b8c4ca887773594c2.wixmp.com%2Ff%2F502fff8b-d4da-4fe3-9ea0-c48cee978d98%2Fda0tne9-be718abe-46fd-424a-a7c5-d1ac84dbc593.jpg%3Ftoken%3DeyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzUwMmZmZjhiLWQ0ZGEtNGZlMy05ZWEwLWM0OGNlZTk3OGQ5OFwvZGEwdG5lOS1iZTcxOGFiZS00NmZkLTQyNGEtYTdjNS1kMWFjODRkYmM1OTMuanBnIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.ixTRNb9rtiPCE8TSEcH5OG9oJC25Zt6yI8igsBD1uSY&tbnid=IGRetm_UNAgkDM&vet=12ahUKEwiRm9nE_uqCAxWgAWIAHcCqC9IQMygXegUIARCJAQ..i&imgrefurl=https%3A%2F%2Fwww.deviantart.com%2Ftulacoe%2Fart%2Fcoconut-606045105&docid=i_3TxW9j-SDPeM&w=800&h=800&itg=1&q=full%20coconut%20emoji&ved=2ahUKEwiRm9nE_uqCAxWgAWIAHcCqC9IQMygXegUIARCJAQ
            return Image.open(path + "/images/fruitImages/coconut.png").resize((100, 100))
        elif self.fruit == "kiwi":
            #Kiwi Image Citation: https://www.google.com/imgres?imgurl=https%3A%2F%2Fcdn.create.vista.com%2Fapi%2Fmedia%2Fsmall%2F2664108%2Fstock-vector-kiwi&tbnid=UqTH0_4FCZZj5M&vet=10CLQBEDMosAFqFwoTCOjZkYb_6oIDFQAAAAAdAAAAABAC..i&imgrefurl=https%3A%2F%2Fcreate.vista.com%2Fvectors%2Fkiwi%2F&docid=xB9qCZ6XusaLRM&w=470&h=608&q=kiwi%20image%20emoji&ved=0CLQBEDMosAFqFwoTCOjZkYb_6oIDFQAAAAAdAAAAABAC
            return Image.open(path + "/images/fruitImages/kiwi.png").resize((60, 60))
        elif self.fruit == "mango":
            #Mango Image Citation: https://www.google.com/imgres?imgurl=https%3A%2F%2Fcreazilla-store.fra1.digitaloceanspaces.com%2Femojis%2F57396%2Fmango-emoji-clipart-md.png&tbnid=wvHuoZQrLJeV7M&vet=12ahUKEwjp-ba4_-qCAxXLMmIAHRTgCIwQMygHegQIARBg..i&imgrefurl=https%3A%2F%2Fcreazilla.com%2Fnodes%2F57396-mango-emoji-clipart&docid=1RFQ9SavEtOwmM&w=800&h=800&q=mango%20apple%20emoji&ved=2ahUKEwjp-ba4_-qCAxXLMmIAHRTgCIwQMygHegQIARBg
            return Image.open(path + "/images/fruitImages/mango.png").resize((75, 75))
        elif self.fruit == "pineapple":
            #Pineapple Image Citation: https://www.google.com/imgres?imgurl=https%3A%2F%2Fem-content.zobj.net%2Fsource%2Fgoogle%2F110%2Fpineapple_1f34d.png&tbnid=arKM-XuDqZg1UM&vet=12ahUKEwiqx-Tu_-qCAxUHFlkFHQ3nAssQMygDegQIARBW..i&imgrefurl=https%3A%2F%2Femojipedia.org%2Fgoogle%2Fandroid-8.0%2Fpineapple&docid=fgaZ1Dt7DzHSmM&w=512&h=512&itg=1&q=pineapple%20google%20phone%20emoji&ved=2ahUKEwiqx-Tu_-qCAxUHFlkFHQ3nAssQMygDegQIARBW
            return Image.open(path + "/images/fruitImages/pineapple.png").resize((100, 100))
        elif self.fruit == "strawberry":
            #Strawberry Image Citation: https://www.google.com/imgres?imgurl=https%3A%2F%2Fstatic-00.iconduck.com%2Fassets.00%2Fstrawberry-emoji-1926x2048-8u86jln8.png&tbnid=MRafJSaL8d54ZM&vet=12ahUKEwi9zeyKgOuCAxUsIWIAHUjPCnYQMygBegQIARBT..i&imgrefurl=https%3A%2F%2Ficonduck.com%2Femojis%2F36150%2Fstrawberry&docid=tKvSOOD89WtyBM&w=1926&h=2048&q=strawberry%20apple%20emoji&ved=2ahUKEwi9zeyKgOuCAxUsIWIAHUjPCnYQMygBegQIARBT
            return Image.open(path + "/images/fruitImages/strawberry.png").resize((50, 50))
        elif self.fruit == "watermelon":
            #Watermelon Image Citation: https://www.google.com/imgres?imgurl=https%3A%2F%2Fimage.emojipng.com%2F68%2F12039068.jpg&tbnid=flPR6TXt_GJnNM&vet=12ahUKEwjJsviagOuCAxXrF2IAHSTyAnwQMygmegUIARC0AQ..i&imgrefurl=https%3A%2F%2Fwww.emojipng.com%2Fpreview%2F12039068&docid=_LcbEOUmLjAtsM&w=900&h=899&q=full%20watermelon%20emoji&ved=2ahUKEwjJsviagOuCAxXrF2IAHSTyAnwQMygmegUIARC0AQ
            return Image.open(path + "/images/fruitImages/watermelon.png").resize((100, 100))
        elif self.fruit == "bomb":
            #Bomb Image Citation: https://www.google.com/imgres?imgurl=https%3A%2F%2Fimage.pngaaa.com%2F746%2F5079746-middle.png&tbnid=N_GEsi40OV2lKM&vet=12ahUKEwjErrnAgOuCAxWfFmIAHRSHDdoQMygIegQIARBi..i&imgrefurl=https%3A%2F%2Fwww.pngaaa.com%2Fdetail%2F5079746&docid=Ugg_aNTyaCnQuM&w=900&h=617&q=bomb%20fruit%20ninja%20png&ved=2ahUKEwjErrnAgOuCAxWfFmIAHRSHDdoQMygIegQIARBi
            return Image.open(path + "/images/bomb.png").resize((100, 100))       
    
class screen:
    #To remove background: remove.bg
    def getBackground():
        #Background Image Citation: https://www.google.com/url?sa=i&url=https%3A%2F%2Freplit.com%2F%40willverrinder%2FFruitNinja&psig=AOvVaw3HFkla36DRKMwYQ57kw9OG&ust=1701408946700000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCMDA9bCA64IDFQAAAAAdAAAAABAD
        return Image.open(path + "/images/background.png")
    
    def getLogo():
        #Fruit Ninja Font: https://fontmeme.com/fruit-ninja-font/#google_vignette 
        img = Image.open(path + "/images/logo.png")
        return img.resize((700, 120), Image.BICUBIC)
    
    def getScore():
        #Fruit Ninja Font: https://fontmeme.com/fruit-ninja-font/#google_vignette 
        return Image.open(path + "/images/score.png").resize((100, 50), Image.BICUBIC)
    
    def getScore2():
        #Fruit Ninja Font: https://fontmeme.com/fruit-ninja-font/#google_vignette 
        return Image.open(path + "/images/score2.png").resize((100, 50), Image.BICUBIC)

    def getEmptyCross():
        #Empty Cross and Filled Cross Image was made in Google Drawings
        return Image.open(path + "/images/emptyCross.png").resize((65, 50), Image.BICUBIC)

    def getFullCross():
        #Empty Cross and Filled Cross Image was made in Google Drawings
        return Image.open(path + "/images/fullCross.png").resize((65, 50), Image.BICUBIC)

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
    
    def drawMultiModeScreen(app, board):
        drawImage(CMUImage(board.getBackground()), 0, 0, width = app.width, height = app.height)
        drawImage(CMUImage(board.getScore()), 0, 0)
        drawImage(CMUImage(board.getScore2()), app.width - 300, 0)

        drawLabel(app.difficultyLevel, app.width//3, 25, fill = "white", font = "montserrat", size = 50)
        drawRect(0, 0, app.width, app.height, fill = "black", opacity = app.pausedOpacity)

        if app.pausedOpacity == 50:
            app.quitGameButton.getButton()
        
        app.pauseGameButton.fillColor = app.pausedFill
        app.pauseGameButton.getButton()
        drawCircle(app.mouseX, app.mouseY, 15, fill = "blue")
        drawCircle(app.mouseX2, app.mouseY2, 15, fill = "red")

        drawLabel(app.score, 200, 25, fill = "white", font = "montserrat", size = 70)
        drawLabel(app.score2, app.width - 100, 25, fill = "white", font = "montserrat", size = 70)
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

    def drawMultiAppEndScreen(app, board):
        drawImage(CMUImage(board.getBackground()), 0, 0, width = app.width, height = app.height)
        drawImage(CMUImage(board.getLogo()), app.width//2 - 350, app.height//2 -250)
        drawLabel("Game Over", app.width//2, app.height//2 -100, fill = "white", font = "montserrat", size = 70)
        drawLabel("Blue Score: " + str(app.score), app.width//2, app.height//2, fill = "white", font = "montserrat", size = 70)
        drawLabel("Red Score: " + str(app.score2), app.width//2, app.height//2 + 100, fill = "white", font = "montserrat", size = 70)
        app.resetButton.getButton()

    def drawHighScore(app, board):
        drawImage(CMUImage(board.getBackground()), 0, 0, width = app.width, height = app.height)
        drawImage(CMUImage(board.getLogo()), app.width//2 - 350, app.height//3 -150)
        app.goBackToSelectScreen.getButton()

        drawLabel("Mouse High Scores", 350, app.height//3, fill = "white", font = "montserrat", size = 50)
        for i in range(len(app.highScores[0])//2):
            drawLabel(str(i+1) + ". " + app.highScores[0][i], 200, app.height//3 + 50 + (i * 50), fill = "white", font = "montserrat", size = 50)

        drawLabel("Hand High Scores", app.width //2 + 325, app.height//3, fill = "white", font = "montserrat", size = 50)
        for i in range(len(app.highScores[0])//2, len(app.highScores[0])):
            drawLabel(str(i-4) + ". " + app.highScores[0][i], app.width // 2 + 200, app.height//3 + 50 + ((i-5) * 50), fill = "white", font = "montserrat", size = 50)

    def drawInstructions(app, board):
        drawImage(CMUImage(board.getBackground()), 0, 0, width = app.width, height = app.height)
        drawImage(CMUImage(board.getLogo()), app.width//2 - 350, app.height//3 -150)
        app.continueButton.getButton()

        drawLabel("Instructions", app.width//2, app.height//3, fill = "white", font = "montserrat", size = 50)
        drawLabel("1. Choose whether to use cursor or hand to play", app.width//2, app.height//3 + 50, fill = "white", font = "montserrat", size = 38)
        drawLabel("2. Choose a game mode", app.width//2, app.height//3 + 100, fill = "white", font = "montserrat", size = 38)
        drawLabel("3. Hold and drag / move your hand slowly to hit the fruit", app.width//2, app.height//3 + 150, fill = "white", font = "montserrat", size = 38)
        drawLabel("4. Don't let the fruit fall off the screen", app.width//2, app.height//3 + 200, fill = "white", font = "montserrat", size = 38)
        drawLabel("5. Don't slice the bomb", app.width//2, app.height//3 + 250, fill = "white", font = "montserrat", size = 38)
        drawLabel("6. Have fun!", app.width//2, app.height//3 + 300, fill = "white", font = "montserrat", size = 38)
        drawLabel("Tip: While using hands, move hands around slowly and in frame", app.width//2, app.height//3 + 350, fill = "white", font = "montserrat", size = 38)

def onAppStart(app):
    app.mouseX = 0
    app.mouseY = 0
    app.mouseX2 = 0
    app.mouseY2 = 0
    app.showSplashScreen = True
    app.showSelectScreen = False
    app.showInstructionScreen = False

    app.classicGameMode = False
    app.arcadeGameMode = False
    app.zenGameMode = False
    app.multiplayerGameMode = False

    app.endGameScreen = False
    app.showHighScoreScreen = False
    app.gamePaused = False
    app.endMultiGameMode = False
    
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
    app.continueButton = Button(app.width - 100, 100, 50, 50, "gray","white", "=>", 30)

    app.resetButton = Button(app.width//2, app.height//2 + 200, app.width//2 - 100, 50, "gray","white", "Reset Game", 30)
    app.goBackToSelectScreen = Button(85, 50, 85, 50, "gray","white", "Go Back", 30)

    app.pauseGameButton = Button(app.width//2 + 150, 30, 50, 50, "gray","white", "Pause", 30)
    app.quitGameButton = Button(app.width//2, app.height//2, 50, 50, "gray","white", "Quit", 30)

    app.score = 0
    app.score2 = 0
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

    app.highScores = []
    readHighScores(app)

def readHighScores(app):
    with open('/Users/saket/Documents/CMU/15112/15112TermProject/TermProject//highScores.txt', 'r') as file:
        highScores = file.read()
        app.highScores.append(highScores.split(","))
    return highScores

def writeHighScores(app):
    with open('/Users/saket/Documents/CMU/15112/15112TermProject/TermProject//highScores.txt', 'w') as file:
        for i in range(len(app.highScores[0])):
            if i == len(app.highScores[0]) - 1:
                file.write(app.highScores[0][i])
            else:
                file.write(app.highScores[0][i] + ",")

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
        classicGameMode(app)

    if app.arcadeGameMode and not app.paused:
        arcadeGameMode(app)

    if app.zenGameMode and not app.paused:
        zenGameMode(app)

    if app.multiplayerGameMode and not app.paused:
        multiGameMode(app)

def onMousePress(app, mouseX, mouseY):
    (app.mouseX, app.mouseY) = (mouseX, mouseY)

    if app.startButton.isClicked(app) and app.showSplashScreen:
        app.showSplashScreen = False
        app.showInstructionScreen = True

    elif app.continueButton.isClicked(app) and app.showInstructionScreen:
        app.showInstructionScreen = False
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

        app.useHands = True
        Game(app, 3, True, 90, "Easy")

    elif app.resetButton.isClicked(app) and (app.endGameScreen or app.endMultiGameMode):
        app.showSplashScreen = True
        app.endGameScreen = False
        app.classicGameMode = False
        app.showSelectScreen = False
        writeHighScores(app)
        onAppStart(app)

    elif app.quitGameButton.isClicked(app) and (app.classicGameMode or app.arcadeGameMode or app.zenGameMode or app.multiplayerGameMode) and app.paused:
        app.showSplashScreen = True
        app.classicGameMode = False
        app.showSelectScreen = False
        onAppStart(app)

    elif app.pauseGameButton.isClicked(app) and (app.classicGameMode or app.arcadeGameMode or app.zenGameMode or app.multiplayerGameMode):
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
        screen.drawMultiModeScreen(app, screen)
    elif app.showHighScoreScreen:
        screen.drawHighScore(app, screen)
    elif app.endMultiGameMode:
        screen.drawMultiAppEndScreen(app, screen)
    elif app.showInstructionScreen:
        screen.drawInstructions(app, screen)

def classicGameMode(app):
    dead = False
    if app.steps % 30 == 0:
        mins, secs = divmod(app.seconds, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        app.seconds -= 1
        app.timer = timeformat
    if app.seconds == 0:
        app.paused = True
        app.endGameScreen = True
        app.classicGameMode = False
        dead = True

    if app.steps % app.spawnsPerTick == 0:
        for _ in range(app.numOfSpawns):
            Game.spawnFruit(app)
    Game.checkCollision(app) 

    if app.lives == 0:
        app.paused = True
        app.endGameScreen = True
        app.classicGameMode = False
        dead = True

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

    if dead:
        if not app.useHands:
            for i in range(len(app.highScores[0])//2):
                if app.score > int(app.highScores[0][i]):
                    for j in range(len(app.highScores[0])//2, i+1, -1):
                        app.highScores[0][j] = str(int(app.highScores[0][j-1]))
                    app.highScores[0][i] = str(app.score)
                    break
        else:
            for i in range(len(app.highScores[0])//2, len(app.highScores[0])):
                if app.score > int(app.highScores[0][i]):
                    for j in range(len(app.highScores[0])-1, i+1, -1):
                        app.highScores[0][j] = str(int(app.highScores[0][j-1]))
                    app.highScores[0][i] = str(app.score)
                    break

def arcadeGameMode(app):
    if app.steps % 30 == 0:
        mins, secs = divmod(app.seconds, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        app.seconds -= 1
        app.timer = timeformat
    if app.seconds == 0:
        app.paused = True
        app.endGameScreen = True
        app.arcadeGameMode = False
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

def zenGameMode(app):
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

def multiGameMode(app):
    if app.steps % 30 == 0:
        mins, secs = divmod(app.seconds, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        app.seconds -= 1
        app.timer = timeformat
    if app.seconds == 0:
        app.paused = True
        app.endMultiGameMode = True
        app.multiplayerGameMode = False

    if app.steps % app.spawnsPerTick == 0:
        for _ in range(app.numOfSpawns):
            Game.spawnFruit(app)
    Game.checkCollision(app) 

    app.spawnsPerTick = 40
    app.difficultyLevel = ""
    app.numOfSpawns = 2
    app.additonalPoints = 10

def main():
    runApp(1200, 600)

if __name__ == '__main__':
    main()  