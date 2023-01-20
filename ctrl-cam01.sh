#!/bin/bash -l

RPATH=./
SCRNM=cam01
PROGNM=driver-cam01.py
TS=$(date +%Y%m%d_%H:%M:%S)

i=0
case $1 in
  start)
     while ! [ -f "$RPATH"/"$PROGNM" ] ; do
        ((i++))
        if [[ $i -eq 12 ]]; then #stop after trying for 2 mins
           break
        fi
        #echo "$RPATH/$PROGNM not available waiting"
        sleep 10
     done
     cd $RPATH
     if pgrep -f "python ./$PROGNM"  > /dev/null 2>&1; then
        echo "[$TS] $PROGNM is already running"
     else
        /usr/bin/screen -S $SCRNM -dm python ./$PROGNM
        if [ $? = 0 ] ; then 
           echo "[$TS] $PROGNM started"
        else
           echo "[$TS] $PROGNM failed to start"
        fi
     fi;;
  stop)
     kill $(pgrep -f "python ./$PROGNM")  2> /dev/null
     if [ $? = 0 ] 
     then
	echo "[$TS] $PROGNM stopped"
     else
	echo "[$TS] $PROGNM was not running"
     fi;;
   restart)
     #Stop
     kill $(pgrep -f "python ./$PROGNM")  2> /dev/null
     if [ $? = 0 ] 
     then
	echo "[$TS] $PROGNM stopped"
     else
	echo "[$TS] $PROGNM was not running"
     fi
     #then Start
     while ! [ -f "$RPATH"/"$PROGNM" ] ; do
        ((i++))
        if [[ $i -eq 12 ]]; then #stop after trying for 2 mins
           break
        fi
        #echo "$RPATH/$PROGNM not available waiting"
        sleep 10
     done
     cd $RPATH
     if pgrep -f "python ./$PROGNM"  > /dev/null 2>&1; then
        echo "[$TS] $PROGNM is already running"
     else
        /usr/bin/screen -S $SCRNM -dm python ./$PROGNM
        if [ $? = 0 ] ; then 
           echo "[$TS] $PROGNM started"
        else
           echo "[$TS] $PROGNM failed to start"
        fi
     fi;;
  *)
     echo "usage: tapo1 start|stop|restart"
     exit 1;;
esac
