# packages
import cv2

# load image file
image = cv2.imread('C:/Users/administrator/Desktop/DX_Projects_onGit/autoM/autoM/edges/PATTERN1.jpg', cv2.IMREAD_UNCHANGED)

# convert image to grayscale
image_grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# reduce image noice
image_blur = cv2.medianBlur(image_grayscale, 9)

# extract edges
image_edges = cv2.adaptiveThreshold(
    image_blur,
    255,
    cv2.ADAPTIVE_THRESH_MEAN_C,
    cv2.THRESH_BINARY,
    blockSize=7,
    C=2
)

# convert image to grayscale cartoon style
image_cartoon = cv2.bitwise_and(image_grayscale, image_edges)

# write output images
cv2.imwrite('C:/Users/administrator/Desktop/DX_Projects_onGit/autoM/autoM/edges/image_edges.png', image_edges)         # bare edges
cv2.imwrite('C:/Users/administrator/Desktop/DX_Projects_onGit/autoM/autoM/edges/image_cartoon.png', image_cartoon)       # cartoon style

# display image in a window
cv2.imshow('Image', image_cartoon)

# break out of a program
cv2.waitKey(0)

# clean up windows
cv2.destroyAllWindows()
