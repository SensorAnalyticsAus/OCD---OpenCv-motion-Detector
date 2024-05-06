# OCD Simple Motion Detection NVR

## About
OCD3 is a software network video recorder. Key features: 
* low-light motion-detection, 
* false-positive motion alert reduction,
* AI summation of daily events (kmeans folder). 

It can use any basic computer as a personal cloud for saving and displaying motion-detected images, videos etc. Outputs can also be used in custom image searching programs e.g. making event summary videos, gathering event stats <a href="https://github.com/SensorAnalyticsAus/S-Big_Visual_Analytics"> video analytics </a> and much more. 

Tested with Tapo, Sricam, PiCam, Hiseeu, and Macbook Pro cameras. The program is quite stable once started - can run for months uninterrupted. Once the program starts up, program parameters e.g. motion sensitivity and disk use can be tailored to meet the site requirements. 

${\color{red}NB:}$
Image Classification codes in `kmeans/`are RaspberryPi OS specif and may require editing some paths.

### Demos
* <a href="https://youtu.be/SsAoOSjJwRs">OCD2 night vision</a>
* <a href="https://youtu.be/sBTi22CeHho">OCD night vision</a>

## What's New (in reverse chronological order)
* `sautils` updated to ver 3.2. A major bug in `kmeans` which restricted the use of image classification to Tapo camera filename format has been relaxed. Now any filename which contains timestamp as YYYYMMDD-HHMMSS will work.
* Bug fixes.
* Version 3 has an updated motion detection scheme, which is more accurate and works better in low-light conditions.
* A heuristic to minimise excessive frame capture.
* `MD.log` for KMeans clustering.
* `images_cn/` for saving contoured b/w versions of motion-detected images. Handy to know what caused motion-detection and where it occurred. 
* Option to increase motion-detection sensitivity after dark.
* Multiple cameras can be motion-detected with suitable mods to *cam??* filenames.
* `crtl3-cam01` can be used to control `driver3-cam01.py` with *start|stop|restart* arguments e.g. `crontab -e` with line, `@reboot /home/saauser/bin/ctrl-cam01 start`). 
* A rpi4b with internal SSD (<a href="https://www.amazon.com/Argon-Raspberry-Support-B-Key-Compatible/dp/B08MJ3CSW7/ref=sr_1_1_sspa?crid=16TYRP9YTSGYD&keywords=argon+one+m.2+case+for+raspberry+pi+4&qid=1677735790&sprefix=argon+one+%2Caps%2C313&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEzQVRBTE5DME1BQjc5JmVuY3J5cHRlZElkPUEwMTUzMzY1MVRGSlpHV0lVVU9PUyZlbmNyeXB0ZWRBZElkPUEwNzk1MzYzMjdRNDBLUUpSVDk4TyZ3aWRnZXROYW1lPXNwX2F0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU=argon"> argon one M2</a>. enclosure) can support three camera streams quite easily.
* Version 1 has even less resource requirements and almost as good (most of my less-critical cameras still use it).

## Getting Started

### Prerequisites
* raspberry pi 4b or a debian linux/mac PC (windows with cygwin may work - not tested)
* python 3.6 or higher
* work-around for accessing a rtsp stream with udp transport only remotely, <a href="https://github.com/SensorAnalyticsAus/remote_rtsp">SensorAnalyticsAu/remote_rtsp</a>

Remember to pip install numpy before installing opencv.

```
python -m pip install -U pip
python -m pip install -U scikit-image 
pip install opencv-python
pip install shutils
pip install -U scikit-learn (for kmeans)

sudo apt update
sudo apt upgrade
sudo apt install screen
sudo apt install ffmpeg
```

### config3

Edit `config3.py` file according to your requirements. If in doubt retain default values where appropriate.


## Running the code

Just execute ctrl3-cam01 after changing its `RPATH` to your path to this repo (Remember to edit `config3.py` first).
```
./ctrl-cam01.sh start
```
To stop:
```
./ctrl-cam01.sh stop
```
To check on program
```
screen -r cam01
ctrl-a-d (to exit)
```
## Troubleshooting
There are really only three main reasons for program not working. 
* Incorrect camera url or camera is not working. Suggest testing camera url with VLC.
* A python dependency is missing.
* A program path is not correctly specified.