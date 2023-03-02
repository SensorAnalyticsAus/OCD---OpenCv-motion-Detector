#!/usr/bin/python

from time import sleep
import os

while True:
    try:
        os.system('python ./detect2-cam01.py')
    except:
        sleep(30)
        pass
# Uncomment the following lines to allow interruption of the program
#    else:
#        break
