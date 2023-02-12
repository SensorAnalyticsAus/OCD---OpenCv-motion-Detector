#!/usr/bin/python

import shutil,os,glob,time,datetime
from subprocess import Popen, check_output, STDOUT, CalledProcessError,\
     STDOUT, PIPE

def saoldestFile(path):
    dir = os.listdir(path)
    # Checking if the list is empty or not
    if len(dir) == 0:
       return 0
    else: 
       oldest_f = os.path.basename(min(glob.glob(os.path.join(path,"*")),
                 key=os.path.getmtime))
       oldest_mt = time.ctime(os.path.getmtime(path+"/"+oldest_f)) 
       today = datetime.datetime.today()
       mod_date = datetime.datetime.fromtimestamp(os.path.getmtime(
                      os.path.join(path,oldest_f)))
       duration = today - mod_date
       return duration.days # oldest file's mtime in days

def sadiskUse(path): # in %age
   total, used, free = shutil.disk_usage(path)
   return round(used/total*100,2) #disk used in %age

def sadiskManage(path,mt): # Eg. mt = +10 will rm files more than 10 days old
    try:
        cret=Popen(['find',path,'-mtime',mt,'-exec','rm','{}',';'],
        stdout=PIPE,stderr=STDOUT)
    except CalledProcessError as exc:
        print("SYNTAX ERROR:",exc.output)
        print("failed to delete old file at:",path)
        output, err = cret.communicate()
        print("output(err):",output.decode(),"err",err)

if __name__ == '__main__':


   mt  = '+'+str(round(0.75*saoldestFile('./test_data')))
   print(mt)

   sadiskManage("./test_data",mt) 
#
   used = sadiskUse("/mnt/GR8GB")
   print(used,"%")
