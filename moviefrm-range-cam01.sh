#!/bin/bash

# Utility to create a timelapse video from images saved by the opencv motion
# detector within any user defined time range. 

IMGPATH=/from/cam01/images # Replace with actual path to motion-detected images
MOVPATH=/to/CAM01_MOVIE # Replace with actual path to save the output movie
TMPD=/tmp/tmpcam01 # Or anyother writeable path
MOV=cam01-range # OR anyother name for th output movie

if [ "$#" -ne 5 ] 
then
 echo "usage moviefrm-sel-jpg FR YYYYMMDD HH:MM[:SS] YYYYMMDD HH:MM[:SS]"
 exit 1
fi

if [ -d "$TMPD" ] 
then
 rm -rf $TMPD/*
else
 mkdir -p $TMPD
fi 

find $IMGPATH -newermt "$2 $3" ! -newermt "$4 $5" -type f -exec cp {} $TMPD \;
if [ $? -ne 0 ] ; then
 exit
fi

ffmpeg -y -framerate $1 -pattern_type glob -i "$TMPD/img*.jpg" \
  -c:v libx264 -pix_fmt yuv420p $MOVPATH/$MOV.mp4 
 echo "jpg --> $MOVPATH/$MOV.mp4"
