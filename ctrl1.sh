#!/bin/bash -l

RPATH=./opencv-motion/

case $1 in
  start)
  cd $RPATH;/usr/bin/screen -S crtl1 -dm ./driver.py;;
  stop)
     kill $(pgrep -f 'python ./driver.py')  2> /dev/null
     if [ $? = 0 ] 
     then
	echo "./driver.py stopped screen closed"
     else
	echo "./driver.py was not running"
     fi;;
  *)
     echo "usage: crtl1 start|stop"
     exit 1;;
esac
