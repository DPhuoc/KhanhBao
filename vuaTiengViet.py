import cv2
import mediapipe as mp
import time
import math
import numpy as np
import csv
import random
import cv2

xPointMouse, yPointMouse = 0, 0


def mouse_click(event, x, y, flags, param):
    global xPointMouse, yPointMouse
    if event == cv2.EVENT_LBUTTONDOWN:
        print('Click')
        xPointMouse, yPointMouse = x, y

def VuaTiengViet(lang):
    frameWidth = 1280
    frameHeight = 720
    cap = cv2.VideoCapture(0)
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)
    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils

    pTime = 0
    cTime = 0

    #set color
    black = (0, 0, 0)
    orange = (232, 149, 9)
    green = (50, 194, 26)
    penSize = 20

    constHd = 35
    wScr, hScr = 1920, 1080

    sm = 3
    plocX, plocY = 0, 0
    clocX, clocY = 0, 0

    xPosButton = 124
    yPosButton = 661
    hButton = 85
    wButton = 85
    disButton = 66

    class Button():
        def __init__(self, pos, text, size = [85, 85]):
            self.pos = pos
            self.text = text
            self.size = size
            self.enabled = 1

    with open('./art/question.csv') as f:
        reader = csv.reader(f)
        tempQuestion = [row for row in reader]
    questions = []
    for idx in tempQuestion:
        questions.append(idx[0])
    print(questions)

    def getPoint(hand, index):
        x = hand.landmark[index].x
        y = hand.landmark[index].y
        x = int(x * 1280)
        y = int(y * 720)
        cv2.circle(recognize, (x, y), radius=10, color=black, thickness=-1)
        h, w, c = img.shape
        wCam = 16 * constHd
        hCam = 9 * constHd
        lx = int(np.interp(x - (1280 - wCam) // 2, (0, wCam), (0, wScr)))
        ly = int(np.interp(y - (720 - hCam) // 2, (0, hCam), (0, hScr)))
        return lx, ly


    def paintPoint(lx, ly, color, radius):
        cv2.circle(img, (lx, ly), radius=radius, color=color, thickness=1)

    def distance_cal(x1, y1, x2, y2):
        return int(math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)))

    def swap_random(seq):
        idx = range(len(seq))
        i1, i2 = random.sample(idx, 2)
        seq[i1], seq[i2] = seq[i2], seq[i1]

    def clearSpace(s):
        pass

    def renderQuest(idx):
        question = []
        randomQuestion = []
        cQr = 0
        cQc = 1
        for i in questions[idx]:
            if i == ' ':
                continue
            randomQuestion.append(i)
        for i in range(0, len(questions[idx])):
            swap_random(randomQuestion)
        # randomQuestion = randomQuestion.join("")
        for idx in randomQuestion:
            if idx == ' ':
                continue
            cQr += 1
            if cQr > 10:
                cQr = 1
                cQc = 2
            question.append(Button([xPosButton + (cQr - 1) * (disButton + 85), yPosButton + (cQc - 1) * (49 + 85)], idx))
        return  question

    for i in questions:
        swap_random(questions)
    showWindow = True
    resString = ''
    questNumber = 0
    questNumberNow = 0
    score = 0
    pointOverlay = False
    popUpFalse = False
    popUpTrue = False
    background = cv2.imread(f'./art/vuaTiengVietPage{lang}.png')
    global xPointMouse, yPointMouse
    with mpHands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.8) as hands:
        while cap.isOpened():
            img = background
            if showWindow == False:
                cv2.destroyAllWindow()
                showWindow = True
                time.sleep(2)
            success, recognize = cap.read()
            if not success:
                continue
            recognize = cv2.flip(recognize, 1)
            imgRGB = cv2.cvtColor(recognize, cv2.COLOR_BGR2RGB)
            if questNumber == questNumberNow:
                questNumber += 1
                question = renderQuest(questNumberNow)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            for idx in question:
                if idx.enabled == 1:
                    cv2.rectangle(img, idx.pos, [idx.pos[0] + wButton, idx.pos[1] + hButton], orange, 4)
                else:
                    cv2.rectangle(img, idx.pos, [idx.pos[0] + wButton, idx.pos[1] + hButton], (50, 50, 50), -1)
                image = cv2.putText(img, idx.text, [idx.pos[0] + (wButton - 40) // 2, idx.pos[1] + (hButton + 30) // 2], cv2.FONT_HERSHEY_SIMPLEX, 2, black, 2, cv2.LINE_AA)

            image = cv2.putText(img, resString, [233, 204], cv2.FONT_HERSHEY_SIMPLEX, 2, black, 2, cv2.LINE_AA)
            image = cv2.putText(img, str(score), [1655, 743], cv2.FONT_HERSHEY_SIMPLEX, 5, green, 7, cv2.LINE_AA)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            if popUpTrue == True:
                img[259:445, 1375:1920] = cv2.imread(f'./art/TrueAnswer{lang}.png')
            if popUpFalse == True:
                img[259:445, 1375:1920] = cv2.imread(f'./art/WrongAnswer{lang}.png')
            if pointOverlay == True:
                img = cv2.imread(f'./art/pointTiengViet{lang}.png')
                textsize = cv2.getTextSize(str(score), cv2.FONT_HERSHEY_SIMPLEX, 3, 5)[0]
                print(textsize[0])
                image = cv2.putText(img, str(score), [918 - textsize[0], 746], cv2.FONT_HERSHEY_SIMPLEX, 3, green, 5, cv2.LINE_AA)
            results = hands.process(imgRGB)
            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    x8, y8 = getPoint(handLms, 8)
                    x4, y4 = getPoint(handLms, 4)
                    xPoint = (x8 + x4) // 2
                    yPoint = (y8 + y4) // 2
                    xPoint = clocX = plocX + (xPoint - plocX) // sm
                    yPoint = clocY = plocY + (yPoint - plocY) // sm
                    plocX, plocY = clocX, clocY
                    paintPoint(xPoint, yPoint, black, round(penSize / 2))

                    range8_4 = distance_cal(x8, y8, x4, y4)

                    x5, y5 = getPoint(handLms, 5)
                    x0, y0 = getPoint(handLms, 0)
                    range0_5 = distance_cal(x0, y0, x5, y5)

                    ratio = range0_5 * 0.32
                    status = False
                    if ratio > range8_4:
                        status = True

                    if (status == True or (xPointMouse != 0 and yPointMouse != 0)) and pointOverlay == True:
                        if (739 <= xPoint <= 1180 and 814 <= yPoint <= 957) or (739 <= xPointMouse <= 1180 and 814 <= yPointMouse <= 957):
                            pointOverlay = False
                            questNumberNow = 0
                            questNumber = 0
                            swap_random(questions)
                            score = 0
                            popUpFalse = False
                            popUpTrue = False
                            xPointMouse, yPointMouse = 0, 0

                    if (status == True or (xPointMouse != 0 and yPointMouse != 0)) and pointOverlay == False:
                        for idx in question:
                            if (idx.pos[0] <= xPoint <= idx.pos[0] + wButton and idx.pos[1] <= yPoint <= idx.pos[1] + hButton and idx.enabled == 1) or (idx.pos[0] <= xPointMouse <= idx.pos[0] + wButton and idx.pos[1] <= yPointMouse <= idx.pos[1] + hButton and idx.enabled == 1):
                                resString += idx.text
                                idx.enabled = 0
                                popUpFalse = False
                                popUpTrue = False
                                xPointMouse, yPointMouse = 0, 0
                        if (195 <= xPoint <= 481 and 301 <= yPoint <= 402) or (195 <= xPointMouse <= 481 and 301 <= yPointMouse <= 402):
                            resString = ''
                            for idx in question:
                                idx.enabled = 1
                            xPointMouse, yPointMouse = 0, 0
                        if ((580 <= xPoint <= 1032 and 301 <= yPoint <= 402) or (580 <= xPointMouse <= 1032 and 301 <= yPointMouse <= 402)) and len(resString) >= len(questions[questNumberNow]):
                            resString = resString.strip()
                            if resString == questions[questNumberNow]:
                                score += 10
                                popUpTrue = True
                                popUpFalse = False
                            else:
                                popUpFalse = True
                                popUpTrue = False
                            questNumberNow += 1
                            if questNumberNow == len(questions):
                                pointOverlay = True
                                questNumberNow = 1
                                questNumber = 2
                            resString = ''
                            xPointMouse, yPointMouse = 0, 0

                        if (729 <= xPoint <= 1181 and 489 <= yPoint <= 590) or (729 <= xPointMouse <= 1181 and 489 <= yPointMouse <= 590):
                            if resString and resString[-1] == ' ':
                                continue
                            resString += ' '
                            # resString = " ".join(resString.split())

                        if (1746 <= xPoint <= 1851 and 132 <= yPoint <= 237) or (1746 <= xPointMouse <= 1851 and 132 <= yPointMouse <= 237):
                            cv2.destroyAllWindows()
                            return

            # Write frame rate
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(img, "FPS= " + str(int(fps)), (10, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)


            # if showWindow == True:
            cv2.imshow('image', img)
            cv2.setMouseCallback('image', mouse_click)
            # if status == True:
            #     cv2.destroyallwindows()
            if cv2.waitKey(1) == 27:
                break