# OCD Motion Detection NVR

This software NVR is based on gilelias' excellent <a href="https://github.com/gilelias/rtsp-motion">POC using opencv to detect motion in rtsp stream</a>. This implementation converts a SDCard based motion recording ip cam or a basic usb cam into a fully featured ip cam with online access to motion events and option to perform <a href="https://github.com/SensorAnalyticsAus/S-Big_Visual_Analytics"> video analytics </a>. Tested with Tapo, Sricam, PiCam, and Macbook Pro 2018's builtin camera.
### Demo
https://youtu.be/R4qauQm8y-M
## What's New (in reverse chronological order)
* Option to increase motion-detection sensitivity after dark.
* Multiple cameras can be motion-detected with suitable mods to *cam??* filenames.
* `crtl` can be used to control `driver.py` with *start|stop|restart* arguments.
* `driver.py` added to make `detect.py` into a backgrounded-screen daemon, which can be started at boot through cron (e.g. `@reboot /home/saauser/bin/ctrl1 start`). 
* `config.py` option for activating camera liveview window side-by-side. Requires X-win supporting terminal e.g. as the one in the PiOS Remote Desktop (where it can be kept running within a `screen`). 
* `config.py` has settings to delete old images when disk space falls below the set limit.
* `config.py` option to timestamp saved frames is added.
* `detect.py` *./images* folder gets created if not present.
* `config.py` option to specify usb cam.
* `config.py` option to scale-down motion-detected frames before saving to disk.
* `moviefrm-rtsp-motion` Creates a slideshow of the saved frames.
* `detect.py` option to record a frame before and <i>numFrames</i> after each event is added in `config.py`. White space is removed in the saved frame file names to facilitate post-processing.

## Getting Started

### Prerequisites
* raspberry pi 3 or there abouts
* python 3
* based on opencv-python
* Optional: For accessing rtsp stream with udp transport remotely, <a href="https://github.com/SensorAnalyticsAus/remote_rtsp">SensorAnalyticsAu/remote_rtsp</a>

```
pip install opencv-python
```

### config

Edit the config file according to your configuration


## Running the code

Just execute ctrl after changing its `RPATH` to your path to this repo (Remember to edit `config.py` first).
```
./ctrl-cam01 start
```
To stop:
```
./ctrl-cam01 stop
```