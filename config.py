import os

#urlx = 0 # device index 0 is for the 1st usb cam or PiCam
#urlx='rtsp://192.168.1.21/onvif1' # sricam
urlx='rtsp://usrname:passwd@router_ip:port/whatever_vendor_string'
threshold1 = 30000      # Lower/raise it for higher/lower sensitivity
threshold2 = 10000      # For night time, lower value to heighten sensitivity
st_time = 21            # Night time threshold starts from e.g. 9pm 
en_time =  5            # Night time threshold end at e.g. 5am 
numFrames = 0           # 0 disables this option
perc = 90               # percent by which to scale saved frames
tsok = 1                # 0 no timestamp | 1 saved frames are timestamped
dlim = 25               # %age disk use after which old file removal starts
dfreq = 3600            # file rm run every dfreq seconds
dpath = './images'      # Do not change!
dday = 30               # files older than dday will be rm when disk gets low
showvid = 0             # 0 don't open | 1 open camera liveview in an X-window
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

