import customtkinter as ctk
import cv2
import HandTrackingModule as htm
import time
import os
import math

# =========================
# CUSTOMTKINTER UI SETUP
# =========================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Smart Capture System")
root.geometry("430x340+800+100")
root.resizable(False, False)
running = True

def close_app(event=None):
    global running
    running = False

root.bind("<q>", close_app)
root.bind("<Escape>", close_app)

# =========================
# TITLE
# =========================
title = ctk.CTkLabel(
    root,
    text="📸 Smart Hand Capture",
    font=("Segoe UI", 26, "bold"),
    text_color="#54d4ff"
)
title.pack(pady=(20, 10))
# =========================
# INFO TEXT
# =========================
info = ctk.CTkLabel(
    root,
    text="You Are In Manual Mode",
    font=("Segoe UI", 14),
    text_color="yellow"
)
info.pack()


# =========================
# STATUS BOX
# =========================
label = ctk.CTkLabel(
    root,
    text="No Picture Captured",
    font=("Segoe UI", 18, "bold"),
    width=320,
    height=60,
    corner_radius=15,
    fg_color="#1E1E1E",
    text_color="white"
)
label.pack(pady=15)


gestureState = ctk.CTkLabel(
    root,
    text="Make Gesture Or Click By Button",
    font=("Segoe UI", 14, "bold"),
    width=280,
    height=40,
    corner_radius=15,
    text_color="#54d4ff",
    fg_color="#1E1E1E",
)
gestureState.pack()


# =========================
# BUTTON FUNCTION
# =========================
def buttonClicked():
    global imgTookByButton
    imgTookByButton = True

button = ctk.CTkButton(
    root,
    text="📷 Click Picture",
    font=("Segoe UI", 18, "bold"),
    width=240,
    height=50,
    corner_radius=15,
    text_color="black",
    fg_color="#00C896",
    hover_color="#10ff00",
    cursor="hand2",
    command=buttonClicked,
    state="normal"
)
button.pack(pady=30)


# =========================
# CAMERA SETTINGS
# =========================
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)


# =========================
# SAVE DIRECTORY
DATASAVE_DIR = r"H:\PyCharm Python\Tracking Projects\Hand Tracking\Essential Data"
SAVE_DIR = r"H:\PyCharm Python\Tracking Projects\Hand Tracking\Captured Image"
COUNTER_FILE = os.path.join(DATASAVE_DIR, "Image Number.txt")
# =========================

# =========================
# TIME CONTROL PANEL
GESTURE_TIME_LIMIT = 2
COUNTDOWN_SECONDS = 3
COOLDOWN_SECONDS = 2
TEXT_SHOW_SECONDS = 2
# =========================


tipOfFingers = [8, 12, 16, 20]

targetZoom = 1.0     # Desired zoom
currentZoom = 1.0    # Actual smooth zoom
zoomSpeed = 0.08     # Smoothness speed
zoomMode=False


detector = htm.handDetector() # call module

# =========================
# VARIABLE
stage = 0
gestureStartTime = 0
cooldownUntil = 0
countdownActive = False
countdownStartTime = 0
successTextUntil = 0
imageCounter = 0
imgTookByButton = False
capturing = False
proMode = False
# =========================


# =========================
# FILE FUNCTIONS
# =========================

def load_image_number():
    os.makedirs(DATASAVE_DIR, exist_ok=True)

    if not os.path.exists(COUNTER_FILE):
        return 0

    with open(COUNTER_FILE, "r") as file:
        value = file.read().strip()

    if value == "":
        return 0

    return int(value)

def save_image_number(number):
    with open(COUNTER_FILE, "w") as file:
        file.write(str(number))

# =========================
# HAND FUNCTIONS
# =========================
def get_fingers(lmList):
    if len(lmList) == 0:
        return []

    fingers = []
    handType = lmList[4][3]

    if handType == 1:
        fingers.append(1 if lmList[4][1] < lmList[3][1] else 0)
    else:
        fingers.append(1 if lmList[4][1] > lmList[3][1] else 0)

    for tip in tipOfFingers:
        fingers.append(1 if lmList[tip][2] < lmList[tip - 2][2] else 0)

    return fingers

def draw_text(img, text, position, scale=0.8, color=(255,255,255), thickness=2):
    cv2.putText(img, text, position, cv2.FONT_HERSHEY_SIMPLEX, scale, (0,0,0), thickness+2)
    cv2.putText(img, text, position, cv2.FONT_HERSHEY_SIMPLEX, scale, color, thickness)

def draw_center_text(img, text, y, scale=2, color=(0,0,255), thickness=4):
    font = cv2.FONT_HERSHEY_SIMPLEX
    textSize, _ = cv2.getTextSize(text, font, scale, thickness)
    x = (img.shape[1] - textSize[0]) // 2

    cv2.putText(img, text, (x,y), font, scale, (0,0,0), thickness+3)
    cv2.putText(img, text, (x,y), font, scale, color, thickness)

# =========================
# MAIN LOOP
# =========================
imgsave = load_image_number()

while running:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)

    if not success:
        break


    img = detector.findHands(frame, drawConnection=False)
    allHands = detector.findAllPosition(img)

    lmListRight = []
    lmListLeft = []

    for hand in allHands:
        if len(hand) == 0:
            continue

        handType = hand[4][3]

        if handType == 1:
            lmListRight = hand
        elif handType == 0:
            lmListLeft = hand

    rightFingers = get_fingers(lmListRight)
    leftFingers = get_fingers(lmListLeft)

    leftHandClosed = leftFingers == [0,0,0,0,0]
    rightHandClosed = rightFingers == [0,0,0,0,0]
    rightHandOpen = rightFingers == [1,1,1,1,1]
    rightHandPro = rightFingers == [0,1,1,0,0]
    leftHandPro = leftFingers == [0,1,1,0,0]
    rightHandUnPro = rightFingers == [0,1,0,0,1]
    leftHandUnPro = leftFingers == [0,1,0,0,1]

    now = time.time()




    # =========================
    # ZOOM GESTURE
    # =========================

    h, w = img.shape[:2]

    # SMOOTH ZOOM TRANSITION

    currentZoom += (targetZoom - currentZoom) * zoomSpeed

    # Prevent invalid zoom
    currentZoom = max(1.0, min(currentZoom, 5.0))


    # CROP CALCULATION

    new_w = int(w / currentZoom)
    new_h = int(h / currentZoom)

    x1 = (w - new_w) // 2
    y1 = (h - new_h) // 2

    x2 = x1 + new_w
    y2 = y1 + new_h

    cropped = img[y1:y2, x1:x2]

    # Resize back
    img = cv2.resize(cropped, (w, h))

    leftHandPose = leftFingers == [0, 1, 0, 0, 0]  # left hand's finger position (thumb, index, middle, ring, little)(1 for open, 0 for close)
    if lmListRight != []:
        indexX = lmListRight[8][1]
        indexY = lmListRight[8][2]
        thumbX = lmListRight[4][1]
        thumbY = lmListRight[4][2]
        distanceFloat = math.hypot(indexX - thumbX, indexY - thumbY)
        distance = math.ceil(distanceFloat)

        if distance < 25 and distance > 0:
            zoomMode = True

    if leftHandPose and len(lmListRight) >= 21 and zoomMode and not proMode:
        # Compress 25-150 → 1-100
        compressDistanceFloat = ((distance - 25) * 99) / 125 + 1
        compressDistance = max(1, min(100, math.ceil(compressDistanceFloat)))
        # print(compressDistance)

        # =========================
        # MAP DISTANCE TO ZOOM
        # 1 → 1x
        # 100 → 5x
        # =========================
        targetZoom = 1 + ((compressDistance - 1) * (5 - 1)) / (100 - 1)
    elif not leftHandPose:
        zoomMode = False

    if leftHandPro and rightHandPro:
        proMode = True

    if proMode and rightHandUnPro and leftHandUnPro:
        proMode = False

    if proMode:
        leftHandClosed  = True
    else:
        leftHandClosed = leftFingers == [0, 0, 0, 0, 0]


    # =========================
    # CAPTURE GESTURE
    # =========================

    if imgTookByButton:
        countdownStartTime = now
        imgTookByButton = False
        countdownActive = True
        capturing = True

    if countdownActive:
        elapsedTime = now - countdownStartTime
        remainingTime = COUNTDOWN_SECONDS - elapsedTime

        if remainingTime > 0:
            countdownNumber = math.ceil(remainingTime)
            button.configure(text=f"Capturing in {countdownNumber}s", text_color_disabled="#613ffc", state="disabled")
            draw_center_text(img, "Capturing in", 190, 1.2, (0,255,255), 3)
            draw_center_text(img, str(countdownNumber), 320, 4, (0,0,255), 6)

        else:
            imgsave += 1
            imageCounter += 1

            filename = os.path.join(SAVE_DIR, f"Captured Image_{imgsave}.jpg")
            cv2.imwrite(filename, img)
            save_image_number(imgsave)

            label.configure(text=f"{imageCounter} - Image Captured")
            countdownActive = False
            cooldownUntil = now + COOLDOWN_SECONDS
            successTextUntil = now + TEXT_SHOW_SECONDS
            capturing=False

    elif now > cooldownUntil:
        if not leftHandClosed:
            stage = 0

        elif stage == 0:
            if rightHandOpen:
                stage = 1
                gestureStartTime = now

        elif stage == 1:
            if now - gestureStartTime > GESTURE_TIME_LIMIT:
                stage = 0
            elif rightHandClosed:
                stage = 2

        elif stage == 2:
            if rightHandOpen:
                stage = 0
                countdownActive = True
                capturing = True
                countdownStartTime = now




    # =========================
    # SUGGESTION
    # =========================

    if leftHandPose and not leftHandClosed and zoomMode:
        info.configure(text=f"You Are In Zoom Mode")
        gestureState.configure(text=f"Zoom: {currentZoom:.1f}x", text_color="yellow")
    elif proMode:
        info.configure(text=f"You Are In Pro Mode")
        gestureState.configure(text=f"Now Perform The Gesture", text_color="#00ff04")
    elif leftHandClosed and not leftHandPose:
        info.configure(text=f"You Are In Capture Mode")
        gestureState.configure(text=f"Need To Close Your Left Hand First", text_color="red")
    else:
        info.configure(text=f"You Are In Manual Mode")
        gestureState.configure(text=f"Make Gesture Or Click By Button", text_color="#54d4ff")


    # =========================
    # SUGGESTION
    # =========================

    if now < successTextUntil and now < cooldownUntil:
        remaining = math.ceil(cooldownUntil - now)
        gestureState.configure(text=f"Image Captured Successfully", text_color="#54d4ff")
        button.configure(text=f"Cooldown {remaining}",text_color_disabled="red", state="disabled")
    elif capturing:
        gestureState.configure(text=f"Capturing The Picture", text_color="yellow")
        # button.configure(text=f"Capturing...", text_color_disabled="red", state="disabled")
    else:
        if button.cget("state") == "disabled":
            button.configure(state="normal")

        if button.cget("text") != "📷 Click Picture":
            button.configure(text="📷 Click Picture")
        if leftHandClosed and not proMode:
            gestureState.configure(text=f"Now Perform The Gesture", text_color="#00ff04")
    # leftHandTextColor = (0,255,0) if leftHandClosed else (0,0,255)
    # draw_text(img, "Need To Close Your Left Hand First" if not leftHandClosed else "Now Perform The Gesture", (20,450), 0.75, leftHandTextColor, 2)



    root.update()
    cv2.imshow("Camera", img)
    cv2.moveWindow("Camera", 100, 100)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
root.destroy()