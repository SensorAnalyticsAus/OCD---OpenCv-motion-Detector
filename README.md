# OCD2 Simple Motion Detection NVR

## About
OCD2 is a software network video recorder with powerful motion-detection, which can use any basic computer as a personal cloud for saving its motion-detected images. This cloud storage can be used for image searching, making daily video summaries, <a href="https://github.com/SensorAnalyticsAus/S-Big_Visual_Analytics"> video analytics </a> and much more. Tested with Tapo, Sricam, PiCam, and Macbook Pro cameras.

### Demos
* <a href="https://youtu.be/SsAoOSjJwRs">OCD2 night vision</a>
* <a href="https://youtu.be/sBTi22CeHho">OCD night vision</a>

## What's New (in reverse chronological order)
* Version 2 has an updated motion detection scheme [^1], which is more accurate and works better in low-light conditions.
* Option to increase motion-detection sensitivity after dark.
* Multiple cameras can be motion-detected with suitable mods to *cam??* filenames.
* `crtl` can be used to control `driver.py` with *start|stop|restart* arguments.
* `driver.py` added to make `detect.py` into a backgrounded-screen daemon, which can be started at boot through cron (e.g. `@reboot /home/saauser/bin/ctrl-cam01 start`). 
* `config.py` option for activating camera liveview window side-by-side. Requires X-win supporting terminal e.g. as the one in the PiOS Remote Desktop (where it can be kept running within a `screen`). 
* `config.py` has settings to delete old images when disk space falls below the set limit.
* `config.py` option to timestamp saved frames is added.
* `detect.py` *./images* folder gets created if not present.
* `config.py` option to specify usb cam.
* `config.py` option to scale-down motion-detected frames before saving to disk.
* `moviefrm-jpg` Creates a slideshow of the saved frames.
* `detect-cam01.py` option to record a frame before and <i>numFrames</i> after each event is added in `config.py`. White space is removed in the saved frame file names to facilitate post-processing.

## Getting Started

### Prerequisites
* raspberry pi or any debian linux/mac (windows with cygwin may be - not tested)
* python 3
* based on opencv-python
* Work-around for accessing a rtsp stream with udp transport only remotely, <a href="https://github.com/SensorAnalyticsAus/remote_rtsp">SensorAnalyticsAu/remote_rtsp</a>

Remember to pip install/upgrade numpy before installing opencv.
```
pip install opencv-python 
sudo apt update
sudo apt upgrade
sudo apt install screen
```

### config

Edit the config file according to your configuration


## Running the code

Just execute ctrl after changing its `RPATH` to your path to this repo (Remember to edit `config2.py` first).
```
./ctrl-cam01.sh start
```
To stop:
```
./ctrl-cam01.sh stop
```

### NB:
Please delete the background estimate 'img_bg.png' after changing the camera/video capture resolution (it's camera sensor size dependent).

[^1]: Credit Adrian Rosebrock (https://pyimagesearch.com/author/adrian/)                on September 2, 2019