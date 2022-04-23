#This is to crop subImages (This is a prototype only to get 
# same sizes of subImages and PIXELS)

# Step 1 is to select the template image or orginal image you want to
#  get for subImage with the same area of Pixels

# Step 2 is to copy the pomID text from google sheet where you want to name the subImage as pomID also.

# Step 3 is to click where is the POM A

# Step 4 is where to save the subImage after clicking the POM A

# Step 5 to get POM B (Repeat step 3 to 4)


from tkinter import Image
import cv2
import os
from PIL import Image
import easygui
import pyperclip

# function to display the coordinates of
# of the points clicked on the image				
def click_event(event, x, y, flags, params):
	# checking for left mouse clicks
	if event == cv2.EVENT_LBUTTONDOWN:
		# print(x, ' ', y)
		font = cv2.FONT_HERSHEY_SIMPLEX
		x1 = x-50
		x2 = x+50
		y1 = y+50
		y2 = y-50
		# cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), 2)
		print(x1,y1,x2,y2)
		# cv2.putText(img, str(x) + ',' +str(y), (x,y), font, 1, (255, 0, 0), 2)
		crop_img = img[y-50:y+50, x-50:x+50]
		s = pyperclip.paste()
		pyperclip.copy(s)
		file = easygui.filesavebox(title='SAVE AS POMID', filetypes=None,default='C:\\subImages\\'+s)
		print(file)
		
		cv2.imwrite(file+'.jpg',crop_img)
		cv2.imshow('image', img)

	# checking for right mouse clicks	
	if event==cv2.EVENT_RBUTTONDOWN:

		# displaying the coordinates
		# on the Shell
		print(x, ' ', y)

		# displaying the coordinates
		# on the image window
		font = cv2.FONT_HERSHEY_SIMPLEX
		b = img[y, x, 0]
		g = img[y, x, 1]
		r = img[y, x, 2]
		cv2.putText(img, str(b) + ',' +
					str(g) + ',' + str(r),
					(x,y), font, 1,
					(255, 255, 0), 2)
		cv2.imshow('image', img)

# driver function	
if __name__=="__main__":
	
	path = easygui.fileopenbox(title='Select Image Style from Table', default='C:\\Templates\\',filetypes=['*.','*.JPG'])

	# reading the image
	img = cv2.imread(path, 1)
	cv2.namedWindow('image', cv2.WINDOW_NORMAL)

	# displaying the image
	cv2.imshow('image', img)

	# setting mouse handler for the image
	# and calling the click_event() function
	cv2.setMouseCallback('image', click_event)

	# wait for a key to be pressed to exit
	cv2.waitKey(0)

	# close the window
	cv2.destroyAllWindows()
