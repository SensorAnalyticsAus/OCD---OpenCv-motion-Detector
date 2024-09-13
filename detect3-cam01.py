#!/usr/bin/python
###############################################################################
#           OpenCV MOTION DETECTOR Sensor Code for RaspberryPi 
#                      Sensor Analytics Australia™ 2024
###############################################################################

import cv2
import time,signal,os
from datetime import datetime
from sautils3_5 import saMotionDetect,imgResize,makeDir,handleChange,setthresh,\
     sadiskUse,saoldestFile,sadiskManage,calcEntropy
from config3 import showvid,cmaxMinD,cmaxInc,cmaxDec,bWt,nIter,tsok,Perc,\
     night_st,day_st,iPx_night,iPx_day,cWidth,dpath,dfreq,dday,dlim,markcnt,\
     urlx,dcrit,cpath,nCnt,cmaxMinN,dday2,lpath,logg,lfreq,lCrt

def signal_handling(signum,recurrfunc):
    global terminate
    terminate = True

cPx = setthresh(night_st,day_st,iPx_night,iPx_day)
cmaxCurr = setthresh(night_st,day_st,cmaxMinN,cmaxMinD)
cmax = cmaxCurr
print('current iPx:',cPx,'current cmax:',cmax,'current bWt:',bWt)
print('night starts from:',night_st,'hr','day starts after:',day_st,'hr')
terminate = False
signal.signal(signal.SIGINT,signal_handling)

time_st = time.time()
makeDir(dpath)
makeDir(cpath)
makeDir(lpath)
duse = sadiskUse(dpath)
print('disk use:',duse,'% ')
print('Program started: ['+datetime.now().strftime("%d/%b/%Y %H:%M:%S")+']')

cap = cv2.VideoCapture(urlx)
time.sleep(2)

md = saMotionDetect(Wt=bWt)
k   = 0
kbg = 0
kmd = 0
kpr = 0
flag = 0
fR = 0

if logg == 1: # if logging is enabled
    fname='MD.log'
    ffname=os.path.join(lpath,fname)
    f = open(ffname,'a') #wrt append
    if f.closed: print(fname+'output file is not available')
    else: print(ffname+' Opened for update every: '+str(lfreq)+' sec')
    savbw = 'yes'
else: savbw = 'no'

t_st = time.time()
while(cap.isOpened()):
    if terminate:
       print("Oh-o gotta go...")
       break
    ret, frame = cap.read()
    if not ret:
       cap.release()
       cap = cv2.VideoCapture(urlx)
       print('Found error; rebuilding stream')
    img_md = frame.copy()
    md.updatebg(img_md)
    if kbg < 100:
       md.updatebg(img_md)
       kbg = kbg + 1
       continue
    if flag == 0: # run once
        print('READY: ['+datetime.now().strftime("%d/%b/%Y %H:%M:%S")+']')
        flag = 1
    cPx = setthresh(night_st,day_st,iPx_night,iPx_day)
    if cmaxCurr != setthresh(night_st,day_st,cmaxMinN,cmaxMinD):
        cmaxCurr = setthresh(night_st,day_st,cmaxMinN,cmaxMinD)
        cmax = cmaxCurr
    imgcn,contours,cmax_area,imgbw = md.mdetect(img_md,iPx=cPx,cWd=cWidth) #md
    if showvid == 1 :
       cv2.imshow('CONTOURED VIDEO', imgcn)
       if cv2.waitKey(20) & 0xFF == ord('q'):
        k = 0
        break
    lcont = len(contours)
    if (lcont > nCnt and cmax_area > cmax) or (lcont > lCrt):
       if markcnt == 1: frame = imgcn.copy()
       if Perc < 100: img = imgResize(frame,Perc)
       else: img = frame.copy()
       op,op2 = handleChange(img,imgbw,dpath,cpath,tsok,savbw)#md saves returns
       if savbw == 'yes':
           eN  = round(calcEntropy(op),3) # entropy actual image
           eN2 = round(calcEntropy(op2),3) # entropy b/w contours image
       else: eN = eN2 = -1
       print(datetime.now().strftime("%d/%m %H:%M:%S"),\
       'MD','fR:',round(fR,1),'iPx: '+str(cPx),\
       ' cnts: '+str(lcont),'a: '+str(round(cmax_area,3)),'%',\
       'aMax: '+str(round(cmax,3)),'%','eN2: '+str(eN2))
       if logg == 1: # if logging is enabled
           if f.closed: print('output file is not available')
           else:
               tfn = datetime.now() 
               decimal_time = tfn.hour+tfn.minute/60+tfn.second/3600\
                            +tfn.microsecond/1000000/3600
               f.write(op+' '+f'{round(decimal_time,6):.6f}'+' '\
               +str(lcont)+' '+str(round(cmax_area,3))+' '\
               +str(eN)+' '+str(eN2)+'\n') 
       kmd = kmd + 1 # inc on each md

    # md hueristic: run every nIter
    t_en = time.time()
    fR = kmd/(t_en - t_st)
    if (k == nIter): 
        if fR > 1 : # i.e. md rate is over 1 fps slow it down
            cmax = cmax + cmaxInc # inc cmax limit slightly
        elif round(fR,0) == 0 and cmax > cmaxCurr: 
            cmax = cmax - cmaxDec  #try increasing fR by lowering cmax a bit
            if cmax < cmaxCurr: cmax = cmaxCurr
            #print('fR:',round(fR,0),'cmax lowered to:',cmax)
        t_st = time.time() # restart timer nIter
        kmd = 0 # restart md count    
        k = 0
    #if kpr == 5*nIter:
    #    print(datetime.now().strftime("%d/%m %H:%M:%S"),\
    #    'contours:',lcont,'contour areas:',round(cmax_area,3),\
    #    'cMax',round(cmax,4),'%')
    #    kpr = 0
    #kpr = kpr + 1
    k = k + 1 
    # disk management block
    time_end = time.time() 
    if (time_end - time_st)/lfreq > 1 and logg == 1: # program ran lfreq secs
       f.flush() # output the logfile to disk
    if (time_end - time_st)/dfreq > 1: # program has run for dfreq secs 
        mt_raw = saoldestFile(dpath)
        mt_raw_cn = saoldestFile(cpath)
        if mt_raw < dday and duse < dlim:
            print('mtime:',mt_raw,'<',dday,'days retention- skipping')
            time_st = time_end # advance start time
            continue
        duse = sadiskUse(dpath) # re-check disk use to be sure
        if duse > dlim: # if disk use is over %age limit set in config
            mt = '+'+str(dday) # less aggressive deletion than the following
            mt2 = '+'+str(dday2) # less aggressive deletion than the following
            if duse > dcrit: mt  = '+'+str(round(0.9*mt_raw)) #2nd condition
                # mtime is set to 0.9*mtime of the oldest f 
            print('DiskUse:',duse,'>',dlim,'file rm',dpath,',mt:',mt)
            txt,rc=sadiskManage(dpath,mt) #files older than mt are deleted 
            print(dpath,'>',mt,'days chkd',txt.decode(),'oldest:',\
                  mt_raw,'days')
            txt,rc=sadiskManage(cpath,mt2) #files older than mt2 are deleted 
            print(cpath,'>',mt2,'days chkd',txt.decode(),'oldest:',\
                  mt_raw_cn,'days')
        time_st = time_end # advance start time    
    #time.sleep(0.1) # end while

if logg == 1: f.close()
cap.release()
cv2.destroyAllWindows()
