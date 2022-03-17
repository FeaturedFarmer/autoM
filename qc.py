
from calendar import Calendar
from cgitb import text
from collections import UserDict
from datetime import datetime
from http.client import FORBIDDEN
from tkinter import *
import os
from tkinter import font as tkFont
from turtle import color
from xmlrpc.server import list_public_methods
from django.shortcuts import render
from matplotlib.pyplot import show
from oauth2client.client import Error
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from pandas import date_range
from ttkwidgets.autocomplete import AutocompleteEntry
from tkcalendar import Calendar, DateEntry
from  tkinter import ttk
import numpy as np
import pandastable
from pandastable import Table
import pandas as pd
import cv2 as cv
import math
import time
from PIL import Image, ImageTk
import shutil

scope = ["https://spreadsheets.google.com/feeds",
        'https://www.googleapis.com/auth/spreadsheets',
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"]


#CREDENTIALS FROM GOOGLE SERVICE ACCOUNT
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("11Fc1o0U_mFUx0iNNcYQLdAt-w8d9-TUrAo9G1Ay79PA")  
accts = sheet.worksheet("MEASURER")
rd = sheet.worksheet("RAWDATA")
qc_ctrl = sheet.worksheet("qc_ctrl")
print('Enter QC Line Number: ')
x = input()
print(x)
cell= qc_ctrl.find(x)
val = cell.row
checkval = qc_ctrl.cell(val,2).value
print(checkval)

if (checkval == "OK"):
    print("Line available. Please wait....")
    x = x.replace("qc","")
    qc_be = sheet.worksheet("qc"+str(x)+"_be")
    poNosh = sheet.worksheet("stylePOs")
    qc_temp = sheet.worksheet("qc"+str(x)+"_temp")
    records = sheet.worksheet("AUTOMEASURE")
    qc = sheet.worksheet("qc"+str(x)+"")

    def qc_main():
        global main_screen
        main_screen = Tk()
        main_screen.geometry("1980x1080")
        main_screen.title("qc"+str(x)+"")
        Label(text="QC"+str(x)+"", bg="#5189A5", width="1080", height="2", font=("Century Gothic", 12)).pack()
        account_login()
        qc_info()
        measure_info()
        camera_info()
        quick_resultTable()
        for child in info_frame.winfo_children():
            child.configure(state='disable')
        for child2 in measureInfo_frame.winfo_children():
            child2.configure(state='disable')
        resultTable_frame.destroy()
        main_screen.mainloop()

    def login_verify():
        global user
        username1 = UserID.get()

        password1 = Pass.get()
        # UserID_k.delete(0, END)
        # Pass_k.delete(0, END)
    
        usr = accts.col_values(4)[1:]
        psk = accts.col_values(5,value_render_option='UNFORMATTED_VALUE')
        if username1 in usr:
            usrnam = accts.find(username1)
            # psk2 = usrnam.row
            pskk = psk[usrnam.row-1]
            if password1 in str(pskk):
                login_sucess()
                user = username1
            else:
                password_not_recognised()
        else:
            user_not_found()


    def account_login():
        global login_frame
        login_frame = Frame(main_screen,bg="#B9CBE5")
        login_frame.place(x=5,y=50,width=800,height=40)
        Label(login_frame,text="Employee ID:",bg="#B9CBE5").pack(side=LEFT, anchor=S,padx=10,pady=10)
        global UserID
        global UserID_k
        UserID = StringVar()
        UserID_k = Entry(login_frame,textvariable=UserID,bg="#B9CBE5").pack(side=LEFT, anchor=S,padx=10,pady=10)
        Label(login_frame,text="Password:",bg="#B9CBE5").pack(side=LEFT, anchor=S,padx=10,pady=10)
        global Pass
        global Pass_k
        Pass = StringVar()
        Pass_k = Entry(login_frame,textvariable=Pass,bg="#B9CBE5",show="*").pack(side=LEFT, anchor=S,padx=10,pady=10)
        Button(login_frame, text="Login", width=50, height=5, command = login_verify).pack(side=LEFT, anchor=S, padx=10,pady=10) 

    def login_sucess():
        global login_success_screen
        login_success_screen = Toplevel(main_screen)
        login_success_screen.title("Success")
        login_success_screen.geometry("150x100")
        Label(login_success_screen, text="Login Success").pack()
        Button(login_success_screen, text="OK", command=continueTo).pack()
        
    def continueTo():
        login_success_screen.destroy()
        for child in info_frame.winfo_children():
            child.configure(state='normal')
        for child2 in measureInfo_frame.winfo_children():
            child2.configure(state='normal')
        for child4 in login_frame.winfo_children():
            child4.configure(state='disable')
        userrow = accts.find(user)
        getrows = accts.row_values(userrow.row)
        fname = getrows[0]
        lname = getrows[1]
        fullname = fname+" "+lname[0]+"."
        qc_ctrl.update_acell("P"+str(x),fullname)
        qc_info()
        quick_resultTable()
        showImg()

    def logout():
        for child in info_frame.winfo_children():

            
            child.configure(state='disable')
        for child2 in measureInfo_frame.winfo_children():
            child2.configure(state='disable')
        for child4 in login_frame.winfo_children():
            child4.configure(state='normal')
        resultTable_frame.destroy()
        UserID_k.delete(0,'end')
        Pass_k.delete(0,'end')
        imgRes_frame.destroy()
        

    def qc_info():
        global info_frame
        info_frame = Frame(main_screen,bg="#B9CBE5")
        info_frame.place(x=850,y=50,width=1000,height=40)
        Label(info_frame,text="Line: "+str(x)+"",bg="#B9CBE5").pack(side=LEFT, anchor=S,padx=10,pady=10)
        Label(info_frame,text="QC Name: "+qc_ctrl.acell("P"+str(x)+"").value,bg="#B9CBE5").pack(side=LEFT, anchor=S,padx=10,pady=10)
        Label(info_frame,text="Date : "+datetime.now().strftime("%A %d %B %Y"),bg="#B9CBE5").pack(side=LEFT, anchor=S,padx=10,pady=10)
        Button(info_frame, text="Logout", width=50, height=5, command = logout).pack(side=LEFT, anchor=S, padx=10,pady=10)

    def measure_info():
        global measureInfo_frame
        
        measureInfo_frame = Frame(main_screen,bg="#B9CBE5")
        measureInfo_frame.place(x=5,y=100,width=1900,height=40)
        Button(measureInfo_frame, text="START", width=20, height=10, command = start_button,font=("Century Gothic", 20)).pack(side=LEFT, anchor=S, padx=5,pady=5)
        Label(measureInfo_frame,text="Factory:",bg="#B9CBE5").pack(side=LEFT, anchor=S,padx=10,pady=10)
        global Factory
        Factory = StringVar(measureInfo_frame)
        Factory.set(qc_ctrl.acell("V"+str(x)+"").value)
        OptionMenu (measureInfo_frame,Factory,*qc_be.col_values(28),command=Factory.trace_add('write',lambda *args: qc_ctrl.update_acell("V"+str(x)+"",Factory.get()))).pack(side=LEFT, anchor=NW,pady=10)
        Label(measureInfo_frame,text="Style:",bg="#B9CBE5").pack(side=LEFT, anchor=S,padx=10,pady=10)
        global Style
        Style = StringVar(measureInfo_frame)
        Style.set(qc_ctrl.acell("D"+str(x)+"").value)
        OptionMenu (measureInfo_frame,Style,*qc_be.col_values(25),command = Style.trace_add('write',lambda *args: qc_ctrl.update_acell("D"+str(x)+"",Style.get()))).pack(side=LEFT, anchor=NW,pady=10)
        Label(measureInfo_frame,text="Size:",bg="#B9CBE5").pack(side=LEFT, anchor=S,padx=10,pady=10)

        global Size
        Size = StringVar(measureInfo_frame)
        Size.set(qc_ctrl.acell("F"+str(x)+"").value)
        OptionMenu (measureInfo_frame,Size,"XXS","XS","S","M","L","XL","XXL","1X","2X","3X",command = Size.trace_add('write',lambda *args: qc_ctrl.update_acell("F"+str(x)+"",Size.get()))).pack(side=LEFT, anchor=NW,pady=10)
        Label(measureInfo_frame,text="Front/Back:",bg="#B9CBE5").pack(side=LEFT, anchor=S,padx=10,pady=10)
        global FB
        FB = StringVar(measureInfo_frame)
        FB.set(qc_ctrl.acell("H"+str(x)+"").value)
        OptionMenu (measureInfo_frame,FB,*qc_be.col_values(29),command = FB.trace_add('write',lambda *args: qc_ctrl.update_acell("H"+str(x)+"",FB.get()))).pack(side=LEFT, anchor=NW,pady=10)
        Label(measureInfo_frame,text="Color:",bg="#B9CBE5").pack(side=LEFT, anchor=S,padx=10,pady=10)
        global Color
        Color = StringVar(measureInfo_frame)
        Color.set(qc_ctrl.acell("N"+str(x)+"").value)
        OptionMenu(measureInfo_frame,Color,*qc_be.col_values(27),command = Color.trace_add('write',lambda *args: qc_ctrl.update_acell("N"+str(x)+"",Color.get()))).pack(side=LEFT, anchor=NW,pady=10)
        samples = []
        for i in range(1,1000):
            samples.append(str("S"+str(i)))
        Label(measureInfo_frame,text="Sample:",bg="#B9CBE5").pack(side=LEFT, anchor=S,padx=10,pady=10)
        global Sample
        Sample = StringVar(measureInfo_frame)
        Sample.set(qc_ctrl.acell("R"+str(x)+"").value)
        OptionMenu (measureInfo_frame,Sample,*samples, command = Sample.trace_add('write',lambda *args: qc_ctrl.update_acell("R"+str(x)+"",Sample.get()))).pack(side=LEFT, anchor=NW,pady=10)
        Label(measureInfo_frame,text="Order#:",bg="#B9CBE5").pack(side=LEFT, anchor=S,padx=10,pady=10)
        global PO
        PO = StringVar(measureInfo_frame)
        PO.set(qc_ctrl.acell("T"+str(x)+"").value)
        getPONOs = qc_ctrl.acell("D"+str(x)+"").value
        poNoFrow = poNosh.find(getPONOs)
        OptionMenu (measureInfo_frame,PO,*poNosh.row_values(poNoFrow.row)[1:],command = PO.trace_add('write',lambda *args: qc_ctrl.update_acell("T"+str(x)+"",PO.get()))).pack(side=LEFT, anchor=NW,pady=10)


    def quick_resultTable():
        
        global resultTable_frame
        resultTable_frame = Frame(main_screen,bg="#B9CBE5")
        resultTable_frame.place(x=5,y=150,width=1200,height=800)
        
        df = pd.DataFrame(qc.get_all_records())
        global pt
        pt = Table(resultTable_frame, dataframe=df)
        
        pt.show()
        print("Ready")

    def camera_info():
        
        global cap
        cap = cv.VideoCapture(0,cv.CAP_DSHOW)
        cap.set(cv.CAP_PROP_FRAME_WIDTH, 1000)
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1000)

    def showImg():
        global imgRes_frame
        imgRes_frame = Canvas(main_screen,bg="#B9CBE5")
        imgRes_frame.place(x=1250,y=150,width=1200,height=800)
        

    def loadFrontImg():
        imgViewres = qc_reclist[3]+qc_reclist[5]+"Front"+qc_reclist[13]+qc_reclist[15]+qc_reclist[17]+qc_reclist[19]
        imgViewres = imgViewres.replace("-","").replace(" ","").replace("/","").replace(".","").upper()
        load = Image.open("C:\\Result\\"+imgViewres+".jpg")
        resized = load.resize((600,400),Image.ANTIALIAS)
        render = ImageTk.PhotoImage(resized)
        global img
        img = Label(imgRes_frame,image=render)
        img.image = render
        img.place(x=0,y=0)

    def loadBackImg():
        imgViewres2 = qc_reclist[3]+qc_reclist[5]+"Back"+qc_reclist[13]+qc_reclist[15]+qc_reclist[17]+qc_reclist[19]
        imgViewres2 = imgViewres2.replace("-","").replace(" ","").replace("/","").replace(".","").upper()
        load2 = Image.open("C:\Result\\"+imgViewres2+".jpg")
        resized2 = load2.resize((600,400),Image.ANTIALIAS)
        render = ImageTk.PhotoImage(resized2)
        global img2
        img2 = Label(imgRes_frame,image=render)
        img2.image = render
        img2.place(x=0,y=400)
        
        
    def start_button():
        imgRes_frame.destroy()
        shutil.copyfile('1.jpg','1_.jpg')
        ret, frame = cap.read()
        img_name = 'Result.jpg'
        img_name2 = 'all_Result.jpg'
        cv.imwrite(img_name,frame)
        cv.imwrite(img_name2,frame)
        pomIDs = []
        pomIDlist = (qc_be.col_values(1))
        pomIDs.extend(pomIDlist)
        imageToInspect = '1.jpg'
        imageToInspect2 = '1_.jpg'
        pxlToInchVal = qc_ctrl.acell("AB"+str(x)+"").value
        global qc_reclist
        qc_reclist = qc_ctrl.row_values(x)

        #google sheet output i/o
        styleNums = []
        StyleSizes = []
        styleSurfaces = []
        styleCriticals = []
        stylePoints = []
        styleColors = []
        styleMeasurers = []
        styleSampleNos = []
        stylePoNos = []
        styleOutputs = []
        styleRecordsID = []
        styleTS = []
        styleFactory = []

        for i in pomIDs[1:]:
        
            recID = i+qc_reclist[17]+qc_reclist[19]
            sampleNum = qc_reclist[17]
            measurer= qc_reclist[15]
            poNo = qc_reclist[19]
            factory = qc_reclist[21]
            dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            recID_repl = recID.replace(".","").replace(" ","").upper().replace("/","").replace(":","")
            output_i = 'C:\subImages\\subImage1\\'+str(i)+'.jpg'    #subImg1
            output_ii = 'C:\subImages\\subImage2\\'+str(i)+'.jpg'   #subImg2
            pomIndex_i = 0  #x,y offset indexes
            result_i = [] #pom measure output list storagepppppg
            img_i = cv.imread(imageToInspect,0) #image inspection read
            img2_i = img_i.copy()
            templ_i = cv.imread(output_i,0)     #subImg1 read
            templ_ii = cv.imread(output_ii,0)      #subImg2 read

            w, h = templ_i.shape[::-1]  #subImg1 shape height and width np arrays
            w2, h2 = templ_ii.shape[::-1]   #subImg2 shape height and width np arrays
            # All the 6 methods for comparison in a list
            methods_i = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
                    'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
            meth_i = methods_i[1] # Method selection
            img_i = img2_i.copy()   #image copy return
            method_i = eval(meth_i) #method eval for images 
            # Apply template Matchingpip i
            res_i = cv.matchTemplate(img_i,templ_i,method_i)    #result values1 from match template
            res2_i = cv.matchTemplate(img_i,templ_ii,method_i)  #result values2 from match template
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res_i)    #get 4 specific types of values after getting result
            min_val2, max_val2, min_loc2, max_loc2 = cv.minMaxLoc(res2_i)   #get 4 specific types of values after getting result
            
            # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
            if method_i in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
                top_left_i = min_loc
                top_left_ii = min_loc2

            else:
                top_left_i = max_loc
                bottom_right_i = (top_left_i[0]+w,top_left_i[1]+h)
                top_left_ii = max_loc2
                bottom_right_ii = (top_left_ii[0]+w2,top_left_ii[1]+h2)

            x1 = int((top_left_i[0]+bottom_right_i[0])/2)
            y1 = int((top_left_i[1]+bottom_right_i[1])/2)
            x2 = int((top_left_ii[0]+bottom_right_ii[0])/2)
            y2 = int((top_left_ii[1]+bottom_right_ii[1])/2)

            #python subImages topleft location image 1 and 2 on inspected image
            subImgpom_i = (x1,y1)
            print(subImgpom_i)
            subImgpom_ii = (x2,y2)
            print(subImgpom_ii)

            #result calculation from distances of 2 subImages according from height of camera
            result_i.append((math.sqrt((x2 - x1)**2 + (y2 - y1)**2))/float(pxlToInchVal))
            print(str(i)+":",round(result_i[pomIndex_i],2),"inches") # print results every pom
            #push to temp sTORAGE
            
            styleNums.append(i)
            styleOutputs.append(round(result_i[pomIndex_i],2))
            styleRecordsID.append(recID_repl)
            stylePoNos.append(poNo)
            styleSampleNos.append(sampleNum)
            styleMeasurers.append(measurer)
            styleTS.append(dt_string)
            styleFactory.append(factory)
            
            #image output line and text result draw
            imgout = cv.imread(imageToInspect)
            imgout2 = cv.imread(imageToInspect2)
            cv.line(imgout,subImgpom_i, subImgpom_ii, (253, 249, 21), 2)
            cv.line(imgout2,subImgpom_i, subImgpom_ii, (253, 249, 21), 1)      
            cv.putText(imgout, str(round(result_i[pomIndex_i],2)), (np.add(subImgpom_ii,[0,0])), cv.FONT_HERSHEY_SIMPLEX, 1.5, (51, 255, 255), 2)
            cv.putText(imgout2, str(round(result_i[pomIndex_i],2)), (np.add(subImgpom_ii,[0,0])), cv.FONT_HERSHEY_SIMPLEX, 1, (51, 255, 255), 1)
            cv.imwrite('C:\Output\\'+str(recID_repl)+'.jpg', imgout)#rgb(0,128,0)   #rgb(34,139,34)
            cv.imwrite('1_.jpg', imgout2)#rgb(0,128,0)   #rgb(34,139,34)
            # cv.imshow('ImgOutput',imgout)
            cv.waitKey(1)

        # cv.destroyWindow('ImgOutput')
        getResultImg = cv.imread('1_.jpg')
        
        resname = qc_reclist[3]+qc_reclist[5]+qc_reclist[7]+qc_reclist[13]+qc_reclist[15]+qc_reclist[17]+qc_reclist[19]
        resname = resname.replace("-","").replace(" ","").replace("/","").replace(".","").upper()
        cv.imwrite('C:\Result\\'+resname+'.jpg',getResultImg)
        os.remove("1_.jpg")

        #Clear temp result
        sheet.values_clear("qc"+str(x)+"_be!E2:E31")
        sheet.values_clear("qc"+str(x)+"_be!O2:O31")
        sheet.values_clear("qc"+str(x)+"_be!P2:P31")
        sheet.values_clear("qc"+str(x)+"_be!Q2:Q31")
        sheet.values_clear("qc"+str(x)+"_be!W2:W31")
        sheet.values_clear("qc"+str(x)+"_be!X2:X31")
        
        time.sleep(1)

        #Batch Update results
        cell_list = qc_be.range("C2:C31"+ str(len(styleNums)+1))
        for xx, val2 in enumerate(styleNums):
            cell_list[xx].value = val2
        qc_be.update_cells(cell_list)

        #Batch Update results
        cell_list = qc_be.range("D2:D31"+ str(len(styleNums)+1))
        for xx, val2 in enumerate(styleOutputs):
            cell_list[xx].value = val2
        qc_be.update_cells(cell_list)

        #Batch RecordsID results
        cell_list = qc_be.range("E2:E31"+ str(len(styleNums)+1))
        for xx, val2 in enumerate(styleRecordsID):
            cell_list[xx].value = val2
        qc_be.update_cells(cell_list)

        #Batch samplenos results
        cell_list = qc_be.range("O2:O31"+ str(len(styleNums)+1))
        for xx, val2 in enumerate(styleSampleNos):
            cell_list[xx].value = val2
        qc_be.update_cells(cell_list)

        #Batch PO Nos results
        cell_list = qc_be.range("P2:P31"+ str(len(styleNums)+1))
        for xx, val2 in enumerate(stylePoNos):
            cell_list[xx].value = val2
        qc_be.update_cells(cell_list)

        #Batch Measurers results
        cell_list = qc_be.range("Q2:Q31"+ str(len(styleNums)+1))
        for xx, val2 in enumerate(styleMeasurers):
            cell_list[xx].value = val2
        qc_be.update_cells(cell_list)

            #Batch Timedates results
        cell_list = qc_be.range("W2:W31"+ str(len(styleNums)+1))
        for xx, val2 in enumerate(styleTS):
            cell_list[xx].value = val2
        qc_be.update_cells(cell_list)

            #Batch Factory results
        cell_list = qc_be.range("X2:X31"+ str(len(styleNums)+1))
        for xx, val2 in enumerate(styleFactory):
            cell_list[xx].value = val2
        qc_be.update_cells(cell_list)

        time.sleep(2)

        lastrecNum = qc_ctrl.acell("AD"+str(x)+"").value
        lastrecNum = int(lastrecNum)

        #range results
        ab = np.array(qc_temp.get_all_values())
        records.update('A'+str(lastrecNum),ab.tolist())
        showtable()
        print('done')

    def showtable():
        dfupdate = pd.DataFrame(qc.get_all_records())
        pt.model.df = dfupdate
        # #pt.show()
        pt.redraw()
        showImg()
        loadFrontImg()
        loadBackImg()

    def password_not_recognised():
        global password_not_recog_screen
        password_not_recog_screen = Toplevel(main_screen)
        password_not_recog_screen.title("Success")
        password_not_recog_screen.geometry("150x100")
        Label(password_not_recog_screen, text="Invalid Password ").pack()
        Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised).pack()


    def user_not_found():
        global user_not_found_screen
        user_not_found_screen = Toplevel(main_screen)
        user_not_found_screen.title("Success")
        user_not_found_screen.geometry("150x100")
        Label(user_not_found_screen, text="User Not Found").pack()
        Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()

    def delete_password_not_recognised():
        password_not_recog_screen.destroy()

    def delete_user_not_found_screen():
        user_not_found_screen.destroy()
        
    qc_main()
else:
    print("Line not available")