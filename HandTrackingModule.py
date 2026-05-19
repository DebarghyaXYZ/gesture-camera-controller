import time
import mediapipe as mp
import cv2


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            model_complexity=1,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )

        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, drawPoint=False, drawConnection=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:

                if drawPoint:
                    drawConnection = False
                    self.mpDraw.draw_landmarks(img, handLms)

                if drawConnection:
                    drawPoint = False
                    self.mpDraw.draw_landmarks(
                        img,
                        handLms,
                        self.mpHands.HAND_CONNECTIONS
                    )

        return img

    def findAllPosition(self, img, draw=False):

        allHands = []

        if self.results.multi_hand_landmarks:

            for handNo, handLms in enumerate(self.results.multi_hand_landmarks):

                lmList = []

                label = self.results.multi_handedness[handNo].classification[0].label

                if label == "Right":
                    handType = 1
                else:
                    handType = 0

                for id, lm in enumerate(handLms.landmark):

                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)

                    lmList.append([id, cx, cy, handType])

                    if draw:
                        cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)

                allHands.append(lmList)

        return allHands


def main():
    cap = cv2.VideoCapture(0)

    detector = handDetector(maxHands=2)

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)

        img = detector.findHands(img)

        # Hand 1
        lmList1 = detector.findPosition(img, handNo=0)

        # Hand 2
        lmList2 = detector.findPosition(img, handNo=1)

        if len(lmList1) != 0:
            print("Hand 1 :", lmList1[4])

        if len(lmList2) != 0:
            print("Hand 2 :", lmList2[4])

        cv2.imshow("Image", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == "__main__":
    main()