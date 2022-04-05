import cv2 

im = cv2.imread('base.jpg')
im1 = cv2.imread('test.jpg')

imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,127,255,0)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


cv2.drawContours(im1, contours, -1, (0,255,0), 1)
cv2.imwrite("resulty.jpg", im1)