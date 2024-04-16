#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# AI Virtual Mouse Project
'''  Owais Khan 
     Btech CSE AI
     2021-350-048  '''

import mediapipe as mp
import cv2
import pyautogui
import tkinter as tk
from tkinter import ttk

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Environment variables
wCam, hCam = 640, 480
screenX, screenY = pyautogui.size()  # Dimensions of the screen
screenCenter = (screenX // 2, screenY // 2)
# Debug show resolution print(f"screen dimensions: {screenX}x{screenY}")
scrollThreshold = 0.1  # Threshold for finger scrolling gesture
scrollSpeed = 10  # Controls the speed of scrolling
prevFingerPos = None  # Initialize prevFingerPos here

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

hands = mp_hands.Hands()

stopProgram = False


def start_program():
    global stopProgram
    global prevFingerPos  # Add this line to access prevFingerPos inside the function
    stopProgram = False
    while not stopProgram:
        success, img = cap.read()

        # Display a window of the current webcam footage each frame
        img = cv2.flip(img, 1)

        rgbFrame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = hands.process(rgbFrame)

        if results.multi_hand_landmarks:
            # Grab first (only) set of hand landmarks
            lm = results.multi_hand_landmarks[0]

            # Isolate index fingertip and middle fingertip
            ttip = lm.landmark[mp_hands.HandLandmark.THUMB_TIP]
            iftip = lm.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            mftip = lm.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            rftip = lm.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            ptip = lm.landmark[mp_hands.HandLandmark.PINKY_TIP]

            # Debug show fingertip coordinates relative position print(f"X: {iftip_x} | Y: {iftip_y} | Z: {iftip_z}")
            cv2.circle(img, (int(ptip.x * img.shape[1]), int(ptip.y * img.shape[0])), 5, (0, 255, 0), -1)
            cv2.circle(img, (int(iftip.x * img.shape[1]), int(iftip.y * img.shape[0])), 5, (255, 0, 0), -1)
            cv2.circle(img, (int(mftip.x * img.shape[1]), int(mftip.y * img.shape[0])), 5, (0, 0, 255), -1)
            cv2.circle(img, (int(ttip.x * img.shape[1]), int(ttip.y * img.shape[0])), 5, (255, 255, 255), -1)
            cv2.circle(img, (int(rftip.x * img.shape[1]), int(rftip.y * img.shape[0])), 5, (255, 165, 0), -1)

            cv2.line(img, (int(iftip.x * img.shape[1]), int(iftip.y * img.shape[0])),
                     (int(ttip.x * img.shape[1]), int(ttip.y * img.shape[0])), (0, 255, 0), 5)
            cv2.line(img, (int(mftip.x * img.shape[1]), int(mftip.y * img.shape[0])),
                     (int(ttip.x * img.shape[1]), int(ttip.y * img.shape[0])), (0, 255, 0), 5)
            cv2.line(img, (int(rftip.x * img.shape[1]), int(rftip.y * img.shape[0])),
                     (int(ttip.x * img.shape[1]), int(ttip.y * img.shape[0])), (0, 0, 255), 5)

            cv2.imshow("Image", img)
            cv2.waitKey(1)

            # Move mouse cursor to current fingertip position
            fingerX = int(screenCenter[0] + screenX * (ptip.x - 0.5))
            fingerY = int(screenCenter[1] + screenY * (ptip.y - 0.5))

            # Pad mouse cursor to edges
            screenUpper = screenY * 2
            screenRight = screenX * 2
            fingerX = fingerX if fingerX > 3 else 3
            fingerY = fingerY if fingerY > 3 else 3
            fingerX = fingerX if fingerX < screenRight - 3 else screenRight - 3
            fingerY = fingerY if fingerY < screenUpper - 3 else screenUpper - 3

            # Debug show fingertip coordinates by screen resolution 
            # print(f"X: {fingerX} | Y: {fingerY}")
            if prevFingerPos is None or abs(fingerX - prevFingerPos[0]) > 5 or abs(
                    fingerY - prevFingerPos[1]) > 5:
                pyautogui.moveTo(fingerX, fingerY)
                prevFingerPos = (fingerX, fingerY)

            # Calculate distance from each finger to the thumb
            leftDistance = ((iftip.x - ttip.x) ** 2 + (iftip.y - ttip.y) ** 2) ** 0.5
            rightDistance = ((mftip.x - ttip.x) ** 2 + (mftip.y - ttip.y) ** 2) ** 0.5
            quitDistance = ((rftip.x - ttip.x) ** 2 + (rftip.y - ttip.y) ** 2) ** 0.5

            # Scroll if finger is close to thumb
            if leftDistance < scrollThreshold:
                pyautogui.scroll(scrollSpeed)
            elif rightDistance < scrollThreshold:
                pyautogui.scroll(-scrollSpeed)
            elif quitDistance < scrollThreshold:
                stopProgram = True


def stop_program():
    global stopProgram
    stopProgram = True


root = tk.Tk()
root.title("AI Virtual Mouse")

start_button = ttk.Button(root, text="Start", command=start_program)
start_button.pack(pady=10)

stop_button = ttk.Button(root, text="Stop", command=stop_program)
stop_button.pack(pady=10)

root.mainloop()


# In[ ]:




