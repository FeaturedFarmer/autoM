import cv2 
import numpy as np

low_color = np.array([0, 100, 20])
high_color = np.array([10, 255, 255])

#25,52,72(Lowgreen)
#102,255,255(Higreen)

# lower1red ([0, 100, 20])``
# upper1red([10, 255, 255])

cap = cv2.VideoCapture(0)
# cap = cv2.imread('C:/Users/administrator/Desktop/DX_Projects_onGit/autoM/autoM/usingColorRange/PATTERN1.JPG')

while True:
    ret, frame = cap.read()
    cv2.imshow('original frame', frame)

    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    cv2.imshow('hsv', hsv)

    mask = cv2.inRange(hsv, low_color, high_color)
    cv2.imshow('masked frame', mask)

    if cv2.waitKey(1) == ord('q'):
        break;

cap.release()
cv2.destroyAllWindows()