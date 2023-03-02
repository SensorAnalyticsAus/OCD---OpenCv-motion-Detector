import os

urlx = 0 # device index 0 is for the 1st usb cam or PiCam
#urlx='rtsp://usrname:passwd@router_ip:port/whatever_vendor_string'
#urlx='rtsp://192.168.1.21/onvif1' # sricam
showvid = 0      # 0: no vid 1: show vid
markcnt = 0      # 0: no contours on saved images 1: contours marked
nCnt    = 1      # number of contours must be > nCnt to trigger motion detect
lCrt    = 4      # min contours to trigger md on their own
cmaxMinD = 0.05  # lowest contours area for md during daytime
cmaxMinN = 0.025 # lowest contours area for md during night time
cmaxInc = 0.025  # fast backoff
cmaxDec = 0.005  # slow start 
bWt = 0.4        # background change weight 0.1-0.5 typically
nIter = 10       # iterations to estimate frame rate fR frames/s
tsok = 1         # 1 adds and 0 no timestamp
Perc = 90        # saved image %age size
night_st = 19    # from 7pm
day_st   = 7     # from 7am hour (after 7:59am)
iPx_night = 5    # lowest pixel value for night time
iPx_day   = 20   # lowest pixel value for daytime
cWidth = 1       # contour line width in pix
dpath = './images' #saving actual images
cpath = './images_cn' # saving white contours on black background
lpath = './log'  # for saving log files
lfreq = 10      # flush log file to disk every 5 mins
dfreq = 3600     # run disk space management routine every hour
dday =  60       # days old image files to delete
dday2 = 30       # days old bw contour files to delete
dlim =  30       # disk %age full for deletion to begin
dcrit = 60       # disk %age full after which 10% of oldest files get deleted
logg = 1         # 0 disable logging 1 enable logging

# rtsp_flag can be set below.

#os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"]="rtsp_transport;tcp\
#   |analyzeduration;9000\
#   |reorder_queue_size;2500"
# informational message-levels are set below.
#os.environ["OPENCV_FFMPEG_DEBUG"] = "1" 
#os.environ["OPENCV_LOG_LEVEL"] = "QUIET"
#os.environ["OPENCV_LOG_LEVEL"] = "VERBOSE"
#os.environ["OPENCV_LOG_LEVEL"] = "ERROR"
