PyCmd='/home/saauser/.venv/bin/python'

from time import sleep
import os

while True:
    try:
        os.system(PyCmd+' ./detect3-tapo1.py')
    except:
        sleep(30)
        pass
# Uncomment the following lines to allow interruption of the program
#    else:
#        break
