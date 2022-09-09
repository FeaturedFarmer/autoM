# packages
import cv2
import numpy as np
import pyautogui as pg

# take a screenshot to store locally
#screenshot = pg.screenshot('screenshot.png')

# take a screenshot to locate objects on
screenshot = cv2.imread('C:/Users/administrator/Desktop/DX_Projects_onGit/autoM/autoM/contours/PATTERN1.jpg')

# adjust colors
#screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
#cv2.imshow("  ",screenshot)

# locate a single object in a screenshot
#board = pg.locateOnScreen('board.png')

# draw rectangle around the object
#cv2.rectangle(
#    screenshot,
#    (board.left, board.top),
#    (board.left + board.width, board.top + board.height),
#    (0, 255, 255),
#    2
#)

# pawn_img = 'C:/Users/administrator/Desktop/DX_Projects_onGit/autoM/autoM/locate-objects/pawn.png'
# pawn_imF = cv2.cvtColor(np.array(pawn_img), cv2.COLOR_RGB2BGR)

# detect several objects on screenshot
for pawn in pg.locateAllOnScreen('C:/Users/administrator/Desktop/DX_Projects_onGit/autoM/autoM/locate-objects/pawn.png', confidence = 0.3, grayscale = True):
    # draw rectangle around the object
    cv2.rectangle(
        screenshot,
        (pawn.left, pawn.top),
        (pawn.left + pawn.width, pawn.top + pawn.height),
        (0, 255, 0),
        1
    )

# display screenshot in a window

cv2.imshow('shot', screenshot)

# escape condition
cv2.waitKey(0)

# clean up windows
cv2.destroyAllWindows()


