from cmu_graphics import *
import cv2
import mediapipe

video = cv2.VideoCapture(0)
hands = mediapipe.solutions.hands.Hands()


def onAppStart(app):
    app.cx = 0
    app.cy = 0

def redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill='gray')
    drawCircle(app.cx, app.cy, 15, fill = "blue")

def onStep(app):
    getHandPosition(app)

def getHandPosition(app):
    __, image = video.read()
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = hands.process(imageRGB)

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            for id, landmark in enumerate(hand.landmark):
                h, w = 400, 400
                cx, cy = w -  int(landmark.x * w), int(landmark.y * h)

                if id == 8:
                    app.cx, app.cy = (cx, cy)

def main():
    runApp(400, 400)

if __name__ == '__main__':
    main()  
