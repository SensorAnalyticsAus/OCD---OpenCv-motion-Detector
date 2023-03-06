#!/usr/bin/python

import shutil,os,glob,time,datetime,sys
from subprocess import Popen, check_output, STDOUT, CalledProcessError,\
     STDOUT, PIPE
from pathlib import Path
import cv2
import numpy as np
import skimage.measure

#########################################################################

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
    def mdetect(self, img, iPx=20, cWd=1):
        img_cn = img.copy() # save color copy for contouring
        img_cn_bw = img.copy() # save color copy for bw contouring
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
            cv2.drawContours(img_cn,contours,-1,(0,255,0),cWd)
        # create contours only bw image for ml
        img_cn_bw.fill(0) # 3 channel image still
        cv2.drawContours(img_cn_bw, contours, -1, (255, 255, 255), 2)
        img_cn_bw = cv2.cvtColor(img_cn_bw,cv2.COLOR_BGR2GRAY)
        # Return contoured img,contours,cmax_area as %age img,contoured img bw
        return img_cn,contours,cmax_area_perc,img_cn_bw

# Credit for this class most parts goes to:
# Adrian Rosebrock (https://pyimagesearch.com/author/adrian/)                  
# on September 2, 2019

#########################################################################

class adsleep:
    def __init__(self,init=1,inc=1,count=5,delay=0):
        self.init = init
        self.init_s = init # save it
        self.k = 0
        self.k_s = self.k # save it
        self.inc = inc
        if delay > 0:
            self.delay = delay
        else:
            self.delay = inc*(pow(count,2)+count)/2
        self.count = count
        self.t1 = time()
    def adwait(self):
        if self.k >= self.count: 
            self.t1 = time() # reset timer to time = 'now'
            self.k = self.k_s
        if self.timer() > self.delay:
            self.t1 = time()
            self.k = self.k_s
            self.init = self.init_s
            #if self.init >= self.count: self.init = self.count
            print('timer exceeded >',self.delay)
            time.sleep(self.init)
            return self.k,self.init,self.delay,self.timer() 
        elif self.k < self.count//2:
            self.k = self.k+1
        elif self.k < self.count:
            self.init = self.init+self.inc    
            self.k = self.k+1
        if self.init >= self.count: self.init = self.count
        time.sleep(self.init)
        return self.k,self.init,self.delay,self.timer() 
    def timer(self):
        self.t2 = time()
        return self.t2 - self.t1 

#########################################################################

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
    msg, err = cret.communicate()
    return msg, err
def cvread(cap):
    ret, frame = cap.read()
    if ret == False : sys.exit("Can't establish connection exiting!")
    return frame
def imgResize(img,perc):
    scale_percent = perc # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    return resized
def makeDir(dirpath):
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
        print(dirpath," created")
    else:
        print(dirpath," exists all good")
def addts(frame,ts): # ocd version updated here
    cv2.putText(frame, '[ocd3]'+ts.strftime( "%d-%b-%Y %H:%M:%S"),\
        (10, frame.shape[0] - 10),\
        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
    return frame
def handleChange(frame,frame2,imgpath,imgpath2,tok):
    ts = datetime.datetime.now() 
    if tok == 1: addts(frame,ts) # only ts frame (not frame2)
    output_path = os.path.join(imgpath,"img_%s.jpg" % (ts\
                             .strftime("%Y%m%d-%H%M%S_%f")))
    output_path2 = os.path.join(imgpath2,"img_%s.jpg" % (ts\
                             .strftime("%Y%m%d-%H%M%S_%f")))
    cv2.imwrite(output_path, frame)
    cv2.imwrite(output_path2, frame2)
    return output_path,output_path2
def setthresh(start_time,end_time,nightval,dayval):
    timenow = int(datetime.datetime.now().strftime("%H"))
    if timenow >= start_time or timenow <= end_time:
        threshx = nightval
    else:
        threshx = dayval
    return threshx
def calcEntropy(imgpath):
    img = cv2.imread(imgpath)
    if len(img.shape) == 3: img1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else: img1 = img.copy()
    entropy = skimage.measure.shannon_entropy(img1)
    return entropy
def genRows(filePath,dt_st,dt_en): # path to MD.log,frm: YYYYMMDD,to: YYYYMMDD
    prefix = './images/img_'
    ct = len(prefix) #slice st
    ct2 = len(prefix)+8 #slice end
    with open(filePath) as f:
        for line in f:
            dt = line[ct:ct2]
            tm = line[ct2+1:ct2+7]
            dtm = int(dt + tm) 
            if dtm >= dt_st and dtm <= dt_en:
                yield line

if __name__ == '__main__':


   mt  = '+'+str(round(0.75*saoldestFile('./test_data')))
   print(mt)

   sadiskManage("./test_data",mt) 
#
   used = sadiskUse("/mnt/GR8GB")
   print(used,"%")
