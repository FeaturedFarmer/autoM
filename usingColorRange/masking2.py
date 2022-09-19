import cv2
import numpy as np

image = cv2.imread('C:/Users/administrator/Desktop/DX_Projects_onGit/autoM/autoM/usingColorRange/style.png')
blur = cv2.GaussianBlur(image, (5,5), 0)
blur_hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

# create NumPy arrays from the boundaries
lower = np.array([0,0,0], dtype = "uint8")
upper = np.array([180,255,40], dtype = "uint8")

# find the colors within the specified boundaries and apply
mask = cv2.inRange(blur_hsv, lower, upper)  
mask = 255 - mask
output = cv2.bitwise_and(image, image, mask = mask)

#for debugging
# show the images
# cv2.imshow("output", output)
cv2.imshow("mask", mask)


cv2.imwrite('C:/Users/administrator/Desktop/DX_Projects_onGit/autoM/autoM/usingColorRange/output.png', mask)
cv2.waitKey()
