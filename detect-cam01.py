#!/usr/bin/python

import cv2
import numpy as np
from datetime import datetime
from time import gmtime, strftime, time, sleep
from config import url,username,password,channel,threshold,urlx,numFrames,\
     perc,tsok,dlim,dfreq,dpath,dday,showvid,threshold2,st_time,en_time
from sautils import saoldestFile,sadiskUse,sadiskManage
import signal,os,sys

def diffImg(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)
def preEvent(cap,img_minus):
    global imgCnt
    ts = datetime.now()
    output_path = os.path.join(dpath,"img_%s.jpg" % (ts\
                             .strftime("%Y%m%d-%H%M%S_%f")))
    addts(tsok,img_minus,ts)
    cv2.imwrite(output_path, img_minus)
    imgCnt += 1
def handleChange(frame):
    global imgCnt,dpath 
    ts = datetime.now()
    addts(tsok,frame,ts)
    output_path = os.path.join(dpath,"img_%s.jpg" % (ts\
                             .strftime("%Y%m%d-%H%M%S_%f")))
    cv2.imwrite(output_path, frame)
    imgCnt += 1
def postEvent(cap,numFrames,perc):
    global imgCnt
    for _ in range(numFrames):
        frame = cap.read()[1]
        frame = imgResize(frame,perc)
        ts = datetime.now()
        output_path = os.path.join(dpath,"img_%s.jpg" % (ts\
                             .strftime("%Y%m%d-%H%M%S_%f")))
        addts(tsok,frame,ts)
        cv2.imwrite(output_path, frame)
        imgCnt += 1
def signal_handling(signum,recurrfunc):
    global terminate
    terminate = True
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
def addts(tsok,frame,ts):
    if tsok:
        cv2.putText(frame, ts.strftime(
        "%d-%b-%Y %H:%M:%S"), (10, frame.shape[0] - 10),
        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
    return(frame)
def setthresh(start_time,end_time):
    timenow = int(datetime.now().strftime("%H"))
    if timenow >= start_time or timenow <= end_time:
        threshx = threshold2
    else:
        threshx = threshold
    return threshx
if __name__ == '__main__':
    time_st = time()
    global terminate,imgCnt
    terminate = False 
    imgCnt = 0
    makeDir(dpath)
    duse = sadiskUse(dpath)
    signal.signal(signal.SIGINT,signal_handling) #sets terminate value on ctrl-c
    if not urlx and urlx !=0 and urlx !=1 and urlx!=2:
       rtsp_url = ("rtsp://%s/user=%s&password=%s&channel=%s&stream=0.sdp?real_stream--rtp-caching=100" % (url, username, password, channel))
    else:
       rtsp_url = urlx
    print ("motion detector in: %s" % rtsp_url)
    print ('motion threshhold: ',threshold,' night threshold: ',threshold2)
    print ('Night threshold applies between',st_time,': 00 -> ',en_time,': 00')
    print("image scale:--->",perc,"%")
    cap=cv2.VideoCapture(rtsp_url)
    sleep(2.0) # stablise camera
    if cap is None or not cap.isOpened():
       print('Unable to open video source: ',rtsp_url)
       sys.exit("Video source failed to open...exiting") 
    else:
       print("Camera is ready to capture motion \n1>\n2>\n3> Go\n")

    while(True):
        if terminate:
            print("Oh-o gotta go outer...")
            break
        # Read three images first:
        print("Re/Initialising with three images:")
        img_minus = cap.read()[1]
        img = cap.read()[1]
        img_plus = cap.read()[1]

        t_minus = cv2.cvtColor(img_minus, cv2.COLOR_RGB2GRAY)
        t = cv2.cvtColor(np.copy(img), cv2.COLOR_RGB2GRAY)
        t_plus = cv2.cvtColor(img_plus, cv2.COLOR_RGB2GRAY)
        while(True):
            if terminate:
                print("Oh-o gotta go inner...")
                break
            dif = diffImg(t_minus, t, t_plus)
            difSum = dif.sum()
            threshold = setthresh(st_time,en_time) #diff thresh in-between  
            if difSum > threshold:
                if numFrames > 0 : # save a frame before the event
                    img_minus = imgResize(img_minus,perc)
                    preEvent(cap,img_minus)
                img = imgResize(img,perc)
                handleChange(img)
                print(datetime.now().strftime("%d/%m %H:%M:%S"),\
                      "MOTION DETECTED:-> Image",imgCnt," Saved at ",\
                      threshold," threshold")
                if numFrames > 0 : # save few frames after the event
                    postEvent(cap,numFrames,perc)
                    break          #restart after these frame captures
        
            img_minus = img #outer while loop
            # Read next image
            img = cap.read()[1]
            t_minus = t
            t = t_plus
            t_plus = cv2.cvtColor(np.copy(img), cv2.COLOR_RGB2GRAY)
            time_end = time() #runs in the outer while loop
            if (time_end - time_st)/dfreq > 1: # program has run for dfreq secs 
                mt_raw = saoldestFile(dpath)
                if mt_raw < dday and duse < dlim: 
                    print('mtime:',mt_raw,'<',dday,'days retention- skipping')
                    time_st = time_end # advance start time
                    continue # skip following lines if mtime < 1 wk
                duse = sadiskUse(dpath)
                if duse > dlim: # if disk use is over %age limit set in config
                    mt  = '+'+str(round(0.9*mt_raw))
                    # mtime is set to 0.9*mtime of the oldest f 
                    print('DiskUse:',duse,'>',dlim,'file rm',dpath,',mt:',mt)
                    sadiskManage(dpath,mt) #files older than mt are deleted 
                #else:
                    #print('DiskUse:',duse,'<',dlim,'all good no file rm needed')
                time_st = time_end # advance start time
            if showvid == 1: # open X-window diplay for cam stream
                cv2.imshow('VIDEO', imgResize(img,perc))
                if cv2.waitKey(20) & 0xFF == ord('q'): 
                    showvid = 0 #close video window on 'q' press and exit
                    print("cleaning up")
                    cap.release()
                    sys.exit('Exiting Program')

    print("cleaning up")
    cap.release()
