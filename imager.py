#This is to create orignal image from a sample style garment
# and to support the subImages cropping with the same aspect of 
# sizes and pixels ratio
# (This is also prototype only.)

# Step 1 (On comments = Camera Settings you can adjust the width and height
# of the camera regarding on what table sizes and table to camera height
# calibration based on the standard)

# Step 2 (Click Save after running)

# Step 3 Named it as what style name is the garment OR you can named it
# if its FRONT or BACK

# Step 4 (look for the cropper.py) after capturing the based template.


import easygui
import numpy as np
import cv2 as cv
import tkinter as tk
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import sys
import gspread
from oauth2client.client import Error
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds",
        'https://www.googleapis.com/auth/spreadsheets',
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"]

#CREDENTIALS FROM GOOGLE SERVICE ACCOUNTfdrtfdrty 
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("11Fc1o0U_mFUx0iNNcYQLdAt-w8d9-TUrAo9G1Ay79PA") 
qc_ctrl = sheet.worksheet("qc_ctrl")

#Set up GUI
window = tk.Tk()  #Makes main window
window.wm_title("Ubase Imager")
window.config(background="#404040")

#Graphics window
imageFrame = tk.Frame(window)
imageFrame.pack(fill='x', expand=False)

#Capture video frames
lmain = tk.Label(imageFrame)
lmain.pack(fill='x', expand=False) 

#Camera settings
cameraNo = 0
cap = cv.VideoCapture(int(cameraNo),cv.CAP_DSHOW)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 1600)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1600)

#Camera frame
def show_frame():
    _, frame = cap.read()
    # frame = cv.rotate(frame, cv.ROTATE_180)
    cv2image = cv.cvtColor(frame, cv.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)

#Lauch detection on object
def proceed_clicked():

    # camera frame on tkinter gui
    global prevImg
    _, frame = cap.read()
    cv2image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    prevImg = Image.fromarray(cv2image)
    ImageTk.PhotoImage(image=prevImg)
    filepath = easygui.filesavebox(title='Filename = Stylename', default='C:\\Templates\\', filetypes=None)
    #save captured frame as image
    print ("Output file to: " + filepath)
    prevImg.save(filepath+'.jpg')

    """ callback when the button clicked
    """

# save button
proceed_button = ttk.Button(window, text="SAVE", command=proceed_clicked)
proceed_button.pack(fill='x', expand=False)

show_frame()  #Display 2
window.mainloop()  #Starts GUI