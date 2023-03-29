import os
import cv2
from cvzone.HandTrackingModule import HandDetector

# Variables
width, height = 1280, 720
folder_path = 'resource/images'

# Camera setup
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# Get the list of presentatoin images
path_images = sorted(os.listdir(folder_path))
# print(path_images)

# Variables
image_number = 0
scale = 1
hs, ws = int(120*scale), int(213*scale)
gesture_threshold = 400
pressed_button = False

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
    full_image_path = os.path.join(folder_path, path_images[image_number])
    current_image = cv2.imread(full_image_path)

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
                print('Left')
                if image_number > 0:
                    image_number -= image_number
                    pressed_button = not pressed_button

            # Gesture 2 - Right
            elif fingers == [0, 0, 0, 0, 1]:
                print('Right')
                if image_number < len(path_images) - 1:
                    image_number += image_number
                    pressed_button = not pressed_button


    # Button pressed itterations
    if pressed_button:
        button_counter += 1
        if button_counter > button_delay:
            button_counter = 0
            pressed_button = not pressed_button


    # Addin webcam image on the slides
    small_image = cv2.resize(img, (ws, hs))
    h, w, _ = current_image.shape
    current_image[0:hs, w-ws:w] = small_image

    cv2.imshow('Image', img)
    cv2.imshow('Slide', current_image)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break