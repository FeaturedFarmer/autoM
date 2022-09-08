# packages
import cv2
import numpy as np

# open source image file
image = cv2.imread('C:/Users/administrator/Desktop/DX_Projects_onGit/autoM/autoM/contours/PATTERN1.png', cv2.IMREAD_UNCHANGED)

# convert image to grayscale
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# onvert image to blck and white
thresh, image_edges = cv2.threshold(image_gray, 100, 255, cv2.THRESH_BINARY)

# create canvas
canvas = np.zeros(image.shape, np.uint8)
canvas.fill(255)

# create background mask
mask = np.zeros(image.shape, np.uint8)
mask.fill(255)

# get all contours
contours_draw, hierachy = cv2.findContours(image_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

# get most significant contours
contours_mask, hierachy = cv2.findContours(image_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# draw all contours
#cv2.drawContours(canvas, contours_draw, 1, (0, 0, 0), 3)

# contours traversal
for contour in range(len(contours_draw)):
    # draw current contour
    cv2.drawContours(canvas, contours_draw, contour, (0, 0, 0), 3)

    # debug
    cv2.waitKey(0)
    cv2.imshow('original',canvas)