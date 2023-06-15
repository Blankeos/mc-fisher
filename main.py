
import cv2 as cv
import numpy as np
import pyautogui as pg
from windowcapture import WindowCapture
from pynput.keyboard import Key, Listener, KeyCode
import math

import win32gui, win32con
import re

# --- List Windows ---
list_of_windows = []
def winEnumHandler(hwnd, ctx):
    if win32gui.IsWindowVisible(hwnd):
        list_of_windows.append(win32gui.GetWindowText(hwnd))
win32gui.EnumWindows(winEnumHandler, None)
list_of_windows = list(filter(re.compile("Minecraft+").match, list_of_windows)) # First item should preferably be Minecraft

# --- Rest of the Program ---
wincap = WindowCapture(list_of_windows[0])
phase_idx = 0 # 0 = Setting Up, 1 = Initialization; 2 = Automation
bbox = (438, 521, 93, 62)
tracker = None
threshold = 0.20
prev_center_tracking_dist = 0

fish_caught = 0

ml_enumerator = 0 # main loop enumerator

def on_press(key):
    global phase_idx
    if (key == Key.ctrl_l):
        phase_idx = 0

def on_release(key):
    global phase_idx
    if (key == Key.ctrl_l):
        phase_idx = 1
    pass

def preprocess_img(img):
    # hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    # lwr = np.array([16, 23, 129])
    # upp = np.array([36, 43, 209])
    # img_mask = cv.inRange(hsv, lwr, upp)
    # img = cv.convertScaleAbs(img, 20, 1.8)
    return img

listener = Listener(on_release=on_release, on_press=on_press)
listener.start()


# Main Loop
while (True):
    screenshot = wincap.get_screenshot()
    screenshot = np.array(screenshot)

    if (phase_idx == 0):
        # -- Choose Bounding Box --
        screenshot = preprocess_img(screenshot)
    
        # Green Bounding Box
        screenshot = cv.rectangle(screenshot, bbox, color=(0,255,0))
        
        # Instructions 1:
        text_str = "Align your fishing bait to the green box"
        textSize = cv.getTextSize(text_str, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        screenshot = cv.putText(screenshot, text_str, (int(wincap.w/2) - int(textSize[0][0]/2), int(wincap.h/2)-20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv.LINE_AA)

        # Instructions 2:
        text_str = "Press the [Left Ctrl] when you're done"
        textSize = cv.getTextSize(text_str, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        screenshot = cv.putText(screenshot, text_str, (int(wincap.w/2) - int(textSize[0][0]/2), int(wincap.h/2)+120), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv.LINE_AA)
        
        # Instructions 3:
        text_str = "You can press [Q] anytime while focusing this window to quit."
        textSize = cv.getTextSize(text_str, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        screenshot = cv.putText(screenshot, text_str, (int(wincap.w/2) - int(textSize[0][0]/2), int(wincap.h/2)+210), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv.LINE_AA)
    elif (phase_idx == 1):
        # -- Initialize Tracker --
        text_str = "Initializing tracker..."
        textSize = cv.getTextSize(text_str, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        screenshot_clone = cv.putText(screenshot, text_str, (int(wincap.w/2) - int(textSize[0][0]/2), int(wincap.h/2)-20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv.LINE_AA)

        # Initialize/Reset Tracker
        tracker = None
        tracker = cv.TrackerMOSSE_create()
        screenshot = preprocess_img(screenshot)
        tracker.init(screenshot, bbox)

        # -save
        cv.imwrite("cache.png", screenshot)

        phase_idx = 2
    elif (phase_idx == 2 and tracker != None):
        # -- Tracking --
        screenshot = preprocess_img(screenshot)

        success, tracking_bbox = tracker.update(screenshot)
        if ml_enumerator > 30:
            if success:
                # Draw: tracking Box:
                _x, _y, _w, _h = int(tracking_bbox[0]),int(tracking_bbox[1]),int(tracking_bbox[2]),int(tracking_bbox[3]),
                screenshot = cv.rectangle(screenshot, (_x, _y, _w, _h), color=(0,255,0))

                # Important Tracking Metrics
                center_point = (int(wincap.w/2), int(wincap.h/2))
                tracking_bbox_point = (_x + int(_w/2), _y + int(_h/2))
                center_tracking_dist = math.dist(center_point, tracking_bbox_point)

                # Line
                screenshot = cv.line(screenshot, center_point, tracking_bbox_point, (0,0,255))

                # Distance
                text_str = "Distance: " + str(center_tracking_dist)
                textSize = cv.getTextSize(text_str, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                screenshot = cv.putText(screenshot, text_str, (int(wincap.w/2) - int(textSize[0][0]/2), textSize[0][1]+20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv.LINE_AA)

                # Reel Logic:
                if (ml_enumerator > 35) and (center_tracking_dist > (prev_center_tracking_dist + prev_center_tracking_dist * threshold)):
                    pg.rightClick()
                    phase_idx = 3
                    fish_caught += 1
                    ml_enumerator = 0

                prev_center_tracking_dist = center_tracking_dist
            else:
                pg.rightClick()
                phase_idx = 3
                fish_caught += 1
                ml_enumerator = 0
                # Not successful - reinitialize tracker with cached image
                # tracker = None
                # tracker = cv.TrackerMOSSE_create()
                # cache = cv.imread("cache.png")
                # tracker.init(cache, bbox)

        # Automating text:
        text_str = "Automating!"
        textSize = cv.getTextSize(text_str, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        screenshot = cv.putText(screenshot, text_str, (int(wincap.w/2) - int(textSize[0][0]/2), int(wincap.h/2)-20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv.LINE_AA)
        
        ml_enumerator += 1
    elif (phase_idx == 3):
        if (ml_enumerator == 10):
            pg.rightClick()
            # ml_enumerator = 0

        if (ml_enumerator > 40):
            phase_idx = 1
            
        ml_enumerator += 1

    # User Interface
    # Fish Caught
    text_str = "Fish Caught: " + str(fish_caught)
    textSize = cv.getTextSize(text_str, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    screenshot = cv.putText(screenshot, text_str, (int(wincap.w/2) - int(textSize[0][0]/2), textSize[0][1]*2+40), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv.LINE_AA)
    
    cv.imshow("Carlo's Autofisher", screenshot)

    # Change Windows Icon
    hwnd = win32gui.FindWindow(None, "Carlo's Autofisher")
    icon_path = "mcfisher.ico"
    win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_BIG, win32gui.LoadImage(None, icon_path, win32con.IMAGE_ICON, 0, 0, win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE))

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

listener.stop()
print('Done.')