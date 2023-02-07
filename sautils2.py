#!/usr/bin/python

import shutil,os,glob,time,datetime,sys
from subprocess import Popen, check_output, STDOUT, CalledProcessError,\
     STDOUT, PIPE
from pathlib import Path
import cv2
import numpy as np

def gblur(frame):
    if frame.ndim > 2: 
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.GaussianBlur(frame, (7, 7), 0)
    return frame
class saMotionDetect: # This class images requires the images are in 
                      # in greyscale (ie img.ndim=2) and slightly blurred.
    def __init__(self, Wt=0.1): # Lower Weights makes bkg less sensitive
                                   # to changes, leading to more stable bkg.
        self.Wt = Wt
        self.img_bg = None
    def updatebg(self, img):
        # Init bkg image if un-initialised so far
        if self.img_bg is None:
            img = gblur(img)
            self.img_bg = img.copy().astype("float") #float for weighted avg
            return
        # Otherwise update weighted average for the bkg image
        img = gblur(img)
        cv2.accumulateWeighted(img,self.img_bg,self.Wt)
    def savebg(self):
        cv2.imwrite('./img_bg.png',self.img_bg)
        print('background image model saved as ./img_bg.png')
    def mdetect(self, img, iPx=20):
        img = gblur(img)
        img_df = cv2.absdiff(self.img_bg.astype("uint8"),img)
        img_th = cv2.threshold(img_df,iPx,255,cv2.THRESH_BINARY)[1] #2nd val
        # Smoothout thresholded img by removing small blobs
        img_th =  cv2.erode(img_th, None, iterations=2)
        img_th = cv2.dilate(img_th, None, iterations=2)
        # Find contours in the thresholded img 
        contours,heirarchy = cv2.findContours(img_th.copy(),cv2.RETR_EXTERNAL,\
                                cv2.CHAIN_APPROX_SIMPLE)
        # sum areas of 5 biggest countour (cmax)
        cmax_area = 0
        cmax_area_perc = 0
        if len(contours) !=  0:
            cnts = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
            for contour in cnts:
                cmax_area = cv2.contourArea(contour)
                cmax_area += cmax_area
            img_ht,img_wd = img_th.shape #no channels in grayscale 
            cmax_area_perc = cmax_area/(img_ht*img_wd)*100
        # Return thresholded img,contours,cmax_area as %age of image
        return img_th,contours,cmax_area_perc

# Credit for this class most parts goes to:
# Adrian Rosebrock (https://pyimagesearch.com/author/adrian/)                  
# on September 2, 2019

def saoldestFile(path):
    dir = os.listdir(path)
    # Checking if the list is empty or not
    if len(dir) == 0:
       return 0
    else: 
       oldest_f = os.path.basename(min(glob.glob(os.path.join(path,"*")),
                 key=os.path.getmtime))
       oldest_mt = time.ctime(os.path.getmtime(path+"/"+oldest_f)) 
       today = datetime.datetime.today()
       mod_date = datetime.datetime.fromtimestamp(os.path.getmtime(
                      os.path.join(path,oldest_f)))
       duration = today - mod_date
       return duration.days # oldest file's mtime in days

def sadiskUse(path): # in %age
   total, used, free = shutil.disk_usage(path)
   return round(used/total*100,2) #disk used in %age

def sadiskManage(path,mt): # Eg. mt = +10 will rm files more than 10 days old
    try:
        cret=Popen(['find',path,'-mtime',mt,'-exec','rm','{}',';'],
        stdout=PIPE,stderr=STDOUT)
    except CalledProcessError as exc:
        print("SYNTAX ERROR:",exc.output)
        print("failed to delete old file at:",path)
        output, err = cret.communicate()
        print("output(err):",output.decode(),"err",err)

def cvread(cap):
    ret, frame = cap.read()
    if ret == False : sys.exit("Can't establish connection exiting!")
    return frame

if __name__ == '__main__':


   mt  = '+'+str(round(0.75*saoldestFile('./test_data')))
   print(mt)

   sadiskManage("./test_data",mt) 
#
   used = sadiskUse("/mnt/GR8GB")
   print(used,"%")
