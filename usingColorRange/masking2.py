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

# show the images
cv2.imshow("output", output)
cv2.imshow("mask", mask)
cv2.waitKey()



# image = cv2.imread('C:/Users/administrator/Desktop/DX_Projects_onGit/autoM/autoM/usingColorRange/7WC6026S_.jpg')

# cv2.imshow("Original", image)

# result = image.copy()

# image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# # lower boundary RED color range values; Hue (0 - 10)
# lower1 = np.array([0, 100, 20])
# upper1 = np.array([10, 255, 255])

# # upper boundary RED color range values; Hue (160 - 180)
# lower2 = np.array([160,100,20])
# upper2 = np.array([179,255,255])

# lower_mask = cv2.inRange(image, lower1, upper1)
# upper_mask = cv2.inRange(image, lower2, upper2)

# #full_mask = cv2.cvtColor(lower_mask + upper_mask,cv2.COLOR_BGR2HSV)
# full_mask = lower_mask + upper_mask;


# result = cv2.bitwise_and(image, image, mask=upper_mask)
# # result = cv2.bitwise_and(image, image, mask=full_mask)

# cv2.imshow('mask', full_mask)
# cv2.imshow('result', result)

# cv2.waitKey(0)
# cv2.destroyAllWindows()

# # import numpy as np
# # import cv2


# # # RGB color boundaries
# # black = ([0, 0, 0], [50, 50, 50])
# # red = ([0, 100, 20], [179,255,255])
# # boundaries = [black, red]

# # #
# # # Load an color image in grayscale
# # img = cv2.imread('C:/Users/administrator/Desktop/DX_Projects_onGit/autoM/autoM/usingColorRange/7WC6026S_.jpg')
# # print(img.shape)

# # # breakpoint()
# # for (lower, upper) in boundaries:

# #     # create NumPy arrays from the boundaries
# #     lower = np.array(lower, dtype="uint8")
# #     upper = np.array(upper, dtype="uint8")


# #     # find the colors within the specified boundaries and apply
# #     # the mask
# #     mask = cv2.inRange(img, lower, upper)
# #     output = cv2.bitwise_and(img, img, mask=mask)

# #     # show the images
# #     cv2.imshow("images", np.hstack([img, output]))
# #     cv2.waitKey(0)