#!/bin/bash
IMGPATH=./images
MOVPATH=./
if [ $1 ]
 then 
 FR=$1
 echo "using FR = $1 fps"
else
 FR=1
 echo "using FR = 1 fps"
fi
ffmpeg -y -framerate ${FR}  -pattern_type glob -i "$IMGPATH/*.jpg" \
  -c:v libx264 -pix_fmt yuv420p $MOVPATH/out.mp4
