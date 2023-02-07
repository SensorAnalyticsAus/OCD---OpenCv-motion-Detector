import os

urlx = 0 # device index 0 is for the 1st usb cam or PiCam
#urlx='rtsp://192.168.1.21/onvif1' # sricam
#urlx='rtsp://usrname:passwd@router_ip:port/whatever_vendor_string'
contNum = 2         # min contours to motion detect,higher->low sensitivity
maxareaPerc = 0.1   # max contour area as % image,higher->low sensitivity  
threshold1 = 20     # pixel start val iPx in day,higher->low sensitivity  
threshold2 = 5      # pixel start val iPx at night,lower->high senstivity
st_time = 21        # Night time threshold starts from e.g. 9pm 
en_time =  5        # Night time threshold end at e.g. 5am 
numFrames = 0       # 0 disables this option
perc = 90           # percent by which to scale saved frames
tsok = 1            # 0 no timestamp | 1 saved frames are timestamped
dlim = 30           # %age disk use after which old file removal starts
dfreq = 3600        # file rm run every dfreq seconds
dpath = './images'  # Do not change!
dday = 30           # files older than dday will be rm when disk gets low
showvid = 0         # 0 don't open | 1 open camera liveview in Xwin
showvidcont = 0     # 0 don't open | 1 open camera contoured view in Xwin
bgnum = 10          # num images to form background model
cWd = 1             # set width of contour line between 1-10
mrkcont = 1         # 0 no contours in images | 1 with contours marked 
# Following settings will be ignored if urlx is not "".
url = "125.21.64.13:554"
username = "myusername"
password = "pAsWoRd"
channel = 1
# rtsp_flag are set below.
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"]="rtsp_transport;tcp\
   |analyzeduration;9000\
   |reorder_queue_size;2500"
# informational message-levels are set below.
#os.environ["OPENCV_FFMPEG_DEBUG"] = "1" 
os.environ["OPENCV_LOG_LEVEL"] = "QUIET"
#os.environ["OPENCV_LOG_LEVEL"] = "VERBOSE"
#os.environ["OPENCV_LOG_LEVEL"] = "ERROR"

