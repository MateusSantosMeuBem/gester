import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui

from personal_parser import (
    parsers
)

args = parsers()
print(args)

# Variables
width, height = 1280, 720

# Camera setup
cap = cv2.VideoCapture(0)

# Variables
image_number = 0
scale = .3
gesture_threshold = 400
pressed_button = False
show_cam = args.show_cam

#  Hand Detector
detector = HandDetector(
    detectionCon=0.8,
    maxHands=1,
)
button_counter = 0
button_delay = 10

while True:
    # Import images
    sucess, img = cap.read()
    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img)
    cv2.line(img, (0, gesture_threshold), (width,  gesture_threshold), (0, 255, 0), 10)

    if hands and not pressed_button:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx, cy = hand['center']
        print(fingers)

        if cy <= gesture_threshold:
            # Gesture 1 - Left
            if fingers == [1, 0, 0, 0, 0]:
                print('left')
                pyautogui.press('left')
                pressed_button = True

            # Gesture 2 - Right
            if fingers == [0, 0, 0, 0, 1]:
                print('Right')
                pyautogui.press('right')
                pressed_button = True

            # Gesture 3 - Quit
            if fingers == [0, 1, 0, 0, 1]:
                print('You rock, baby!')
                break

    # Button pressed itterations
    if pressed_button:
        button_counter += 1
        if button_counter > button_delay:
            button_counter = 0
            pressed_button = False

    if show_cam:
        h, w, _ = img.shape
        image_on_screen = cv2.resize(img, (int(w*scale), int(h*scale)))
        cv2.imshow('Image', image_on_screen)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break