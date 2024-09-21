###############################################################################
#                        Image Classifier Utilities 
#                      Sensor Analytics Australia™ 2024
###############################################################################
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'
import shutil,os,glob,time,datetime,sys
from subprocess import Popen, check_output, STDOUT, CalledProcessError,\
     STDOUT, PIPE, run
from pathlib import Path
import cv2
import numpy as np
import skimage.measure
import re
from PIL import Image
from numpy.linalg import norm
from sklearn.decomposition import PCA
import random
from math import copysign,log10
try:
    from config import rseed
except ImportError: # set rseed value below if config.sys has no rseed
    rseed = 10 
#########################################################################

def gblur(frame):
    if frame.ndim > 2: 
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.GaussianBlur(frame, (7, 7), 0)
    return frame
class saMotionDetect: # This class images requires the images are in 
                      # in greyscale (ie img.ndim=2) and slightly blurred.
    def __init__(self, Wt=0.1): # Lower Weights makes bkg less sensitive
                                   # to changes, leading to more stable bkg.
        self.Wt = Wt
        self.img_bg = None
    def updatebg(self, img):
        # Init bkg image if un-initialised so far
        if self.img_bg is None:
            img = gblur(img)
            self.img_bg = img.copy().astype("float") #float for weighted avg
            return
        # Otherwise update weighted average for the bkg image
        img = gblur(img)
        cv2.accumulateWeighted(img,self.img_bg,self.Wt)
    def mdetect(self, img, iPx=20, cWd=1):
        img_cn = img.copy() # save color copy for contouring
        img_cn_bw = img.copy() # save color copy for bw contouring
        img = gblur(img)
        img_df = cv2.absdiff(self.img_bg.astype("uint8"),img)
        img_th = cv2.threshold(img_df,iPx,255,cv2.THRESH_BINARY)[1] #2nd val
        # Smoothout thresholded img by removing small blobs
        img_th =  cv2.erode(img_th, None, iterations=2)
        img_th = cv2.dilate(img_th, None, iterations=2)
        # Find contours in the thresholded img 
        contours,heirarchy = cv2.findContours(img_th.copy(),cv2.RETR_EXTERNAL,\
                                cv2.CHAIN_APPROX_SIMPLE)
        # sum areas of 5 biggest countour (cmax)
        cmax_area = 0
        cmax_area_perc = 0
        if len(contours) !=  0:
            cnts = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
            for contour in cnts:
                cmax_area = cv2.contourArea(contour)
                cmax_area += cmax_area
            img_ht,img_wd = img_th.shape #no channels in grayscale 
            cmax_area_perc = cmax_area/(img_ht*img_wd)*100
            cv2.drawContours(img_cn,contours,-1,(0,255,0),cWd)
        # create contours only bw image for ml
        img_cn_bw.fill(0) # 3 channel image still
        cv2.drawContours(img_cn_bw, contours, -1, (255, 255, 255), 2)
        img_cn_bw = cv2.cvtColor(img_cn_bw,cv2.COLOR_BGR2GRAY)
        # Return contoured img,contours,cmax_area as %age img,contoured img bw
        return img_cn,contours,cmax_area_perc,img_cn_bw

# Credit for this class most parts goes to:
# Adrian Rosebrock (https://pyimagesearch.com/author/adrian/)                  
# on September 2, 2019

#########################################################################

class adsleep:
    def __init__(self,init=1,inc=1,count=5,delay=0):
        self.init = init
        self.init_s = init # save it
        self.k = 0
        self.k_s = self.k # save it
        self.inc = inc
        if delay > 0:
            self.delay = delay
        else:
            self.delay = inc*(pow(count,2)+count)/2
        self.count = count
        self.t1 = time()
    def adwait(self):
        if self.k >= self.count: 
            self.t1 = time() # reset timer to time = 'now'
            self.k = self.k_s
        if self.timer() > self.delay:
            self.t1 = time()
            self.k = self.k_s
            self.init = self.init_s
            #if self.init >= self.count: self.init = self.count
            print('timer exceeded >',self.delay)
            time.sleep(self.init)
            return self.k,self.init,self.delay,self.timer() 
        elif self.k < self.count//2:
            self.k = self.k+1
        elif self.k < self.count:
            self.init = self.init+self.inc    
            self.k = self.k+1
        if self.init >= self.count: self.init = self.count
        time.sleep(self.init)
        return self.k,self.init,self.delay,self.timer() 
    def timer(self):
        self.t2 = time()
        return self.t2 - self.t1 

#########################################################################

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
    msg, err = cret.communicate()
    return msg, err
def cvread(cap):
    ret, frame = cap.read()
    if ret == False : sys.exit("Can't establish connection exiting!")
    return frame
def imgResize(img,perc):
    scale_percent = perc # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    return resized
def makeDir(dirpath):
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
        print(dirpath," created")
    else:
        print(dirpath," exists all good")
def rmdir(dir_path):
    cret=run(['rm','-rf',dir_path])
    if cret.returncode == 0:
        print(dir_path,color.GREEN+"-> deleted :"+color.END)
    else:
        print(dir_path,color.RED+"-> failed to delete"+color.END)
def mvdir(dir_path1, dir_path2):
    cret=run(['mv',dir_path1,dir_path2])
    if cret.returncode == 0:
        print(dir_path1,color.GREEN+"-> moved :"+color.END,dir_path2)
    else:
        print(dir_path1,color.RED+"-> failed to move to:"+color.END,dir_path2)
def mkdir_cleared(dir_path):
    cret=run(['rm','-rf',dir_path])
    if cret.returncode == 0:
        print(dir_path,color.GREEN+"-> cleared :"+color.END)
    else:
        print(dir_path,color.RED+"-> failed to clear"+color.END)
    Path(dir_path).mkdir(parents=True, exist_ok=True) #make dir_path folder/ if it doesn't exist
def addts(frame,ts): # ocd version updated here
    cv2.putText(frame, '[ocd3]'+ts.strftime( "%d-%b-%Y %H:%M:%S"),\
        (10, frame.shape[0] - 10),\
        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
    return frame
def handleChange(frame,frame2,imgpath,imgpath2,tok,savbw='yes'):
    ts = datetime.datetime.now() 
    if tok == 1: addts(frame,ts) # only ts frame (not frame2)
    output_path = os.path.join(imgpath,"img_%s.jpg" % (ts\
                             .strftime("%Y%m%d-%H%M%S_%f")))
    cv2.imwrite(output_path, frame)
    if savbw == 'yes':
        output_path2 = os.path.join(imgpath2,"img_%s.jpg" % (ts\
                             .strftime("%Y%m%d-%H%M%S_%f")))
        cv2.imwrite(output_path2, frame2)
    else: output_path2 = -1
    return output_path,output_path2
def setthresh(start_time,end_time,nightval,dayval):
    timenow = int(datetime.datetime.now().strftime("%H"))
    if timenow >= start_time or timenow <= end_time:
        threshx = nightval
    else:
        threshx = dayval
    return threshx
def calcEntropy(imgpath):
    img = cv2.imread(imgpath)
    if len(img.shape) == 3: img1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else: img1 = img.copy()
    entropy = skimage.measure.shannon_entropy(img1)
    return entropy.item()
def genRows(filePath,dt_st,dt_en): # path to MD.log,frm: YYYYMMDD,to: YYYYMMDD
    with open(filePath) as f:
        for line in f:
            dtm = fileDt(line) 
            if int(dtm) >= int(dt_st) and int(dtm) <= int(dt_en):
                yield line
def fileDt(fname): # searches YYYYMMDD-HHMMSS in filename rets YYYYMMDDHHMMSS
 s=re.search("([0-9]{4}[0-9]{2}[0-9]{2}\-[0-9]{6})",fname)
 if s:
        d=s.group(0)
        d=d.replace('-','')
 else: 
        d='19000101000000' # If None then a very old date is sent
 return(d)
def fileTs(filename): # get the int timestamp for fileDt string
 fDt=datetime.datetime.strptime(fileDt(filename),'%Y%m%d%H%M%S').timestamp()
 return int(round(fDt))
def num_name(filename): # extracts all digits in a string as a number
 regex = re.compile('\d+')
 nlist=regex.findall(filename)
 numstr=''
 if not nlist:
        return -1 
 else:
        for s in nlist:
               numstr += s
 return int(numstr)
def fileSel(fpath,sdt,edt): # rets unsorted list of files in datetime range
 if isinstance(sdt,int) or isinstance(sdt,float): sdt=str(sdt) # need as string
 if isinstance(edt,int) or isinstance(edt,float): edt=str(edt) # need as string
 st_d_t=datetime.datetime.strptime(sdt,'%Y%m%d%H%M%S').timestamp()
 en_d_t=datetime.datetime.strptime(edt,'%Y%m%d%H%M%S').timestamp()
 lst = [i for i  in os.listdir(fpath)
          if fileTs(i) >= int(st_d_t) and fileTs(i) <= int(en_d_t)]
 return lst
def writeLog(msg,log_file):
 with open(log_file,'a') as logfile:
     logfile.write(msg+'\n')
 return
def imgcont(im):
 imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
 imgray = cv2.GaussianBlur(src=imgray, ksize=(3, 5), sigmaX=0.5)
 ret, thresh = cv2.threshold(imgray, 127, 255, 0)
 cnt, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,
                                        cv2.CHAIN_APPROX_SIMPLE)
 ncon=len(cnt)
 cona = sum([cv2.contourArea(k) for k in cnt ])
 return ncon,cona,cnt           
def cntcent(cnt,N,img_w,img_h,flag): # find centriods of N contours
 # calc all contour areas
 carea = [cv2.contourArea(c) for c in cnt] # calc contour areas
 # find N largest contours - area wise -  in carea list
 if flag == 'L':
  indices = np.argsort(carea)[::-1][:N] # reverse list to take last N elems
                                        # 0 is index to largest, N to smallest 
 # find N smallet contours - area wise -  in carea list
 elif flag == 'S':
  indices = np.argsort(carea)[:N] # 0 is index to smallest, N to largest 
 else:
  print('incorrect flag:{} called in cntcent()'.format(flag))
  sys.exit(1)
 # calc centriod of a selected contours
 cntX = []
 cntY = []
 for idx in range(0,N):
  M = cv2.moments(cnt[indices[idx]])
  if M['m00'] == 0.: # check for division by zero!
   x,y,w,h = cv2.boundingRect(cnt[indices[idx]]) # use alternative method
   xr = (x+w/2) # center of rect as centriod
   yr = (y+h/2)
   cntX.append(xr)
   cntY.append(yr) 
   dErr = 1
   if xr < 0 or xr > img_w or yr < 0 or yr > img_h: # sanity check rect 
    cntX.append(img_w/2)      # select center of img as centriod
    cntY.append(img_h/2)
    dErr = 2
  else:  
   cntX.append(M['m10']/M['m00'])
   cntY.append(M['m01']/M['m00'])
   dErr = 0
 return cntX,cntY,dErr # [cX1,cX2,cX3] [cY1,cY2,cY3] division by zero error 1
def inorms(img): # Calc L1 and L2 norms of grayscaled image
 img_gs = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).flatten()
 return norm(img_gs,1),norm(img_gs)  
def imgResize_n(im,new_ht): # resizes to desired img ht preserving aspect ratio
 if len(im.shape) < 3:
   height, width = im.shape
 else:
   height, width, channels = im.shape 
 if new_ht > height: return im # return as is
 new_wd = int(round(width/height*new_ht,0))
 resized_im = cv2.resize(im,(new_wd,new_ht))
 return resized_im 
def imgDimRed(img,n): #Reduces image to original rows and n cols
 if len(img.shape) == 3: # change to grayscale
   img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 return PCA(n_components=n).fit_transform(img)
def imgBg(img): # returns a black background for the size of input img
 if len(img.shape) < 3:
   h, w = img.shape
   blank_img = 0 * np.ones(shape=(h, w), dtype=np.uint8)
 else:
   h, w, c = img.shape
   blank_img = 0 * np.ones(shape=(h, w, c), dtype=np.uint8)
 return blank_img
def imgFeats(img,nfeats): # extract orb features
 if len(img.shape) >=  3:
   img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 orb = cv2.ORB_create(nfeatures=nfeats)
 kp = orb.detect(img,None) # init orb detector
 kp, des = orb.compute(img, kp) # find image keypoints and feature descriptors
 if kp is None or des is None : return None 
 pts = []
 for x in kp:
   pts.append([x.pt[0], x.pt[1], x.size, x.angle])
 return np.asarray(pts, dtype=np.float64)#return features as ndarray
class invarPR: # For descriptor distance based invariant pattern-recognition
 def __init__(self,ImgPath,nfts=50): # set an index image for this istance
   self.nfts = nfts
   imgf = os.listdir(ImgPath)
   r = random.Random()
   if rseed != 'off':
     r.seed(rseed) # to ensure reproducable sequences
   for i in range(100): # iterate this many times until index img sel
     self.imgrand = r.choice(imgf) # save for ref
     self.imgid = os.path.join(ImgPath,self.imgrand) # save img path
     imgidx = cv2.imread(self.imgid) # read save img
     if len(imgidx.shape) >=  3:
       imgidx = cv2.cvtColor(imgidx, cv2.COLOR_BGR2GRAY)
     orb = cv2.ORB_create(nfeatures=nfts)
     nfea = orb.detect(imgidx,None)
     if len(nfea) == nfts: # good img with right nfts found
       break
   if len(nfea) != nfts:
     print('no index img found in 100 iterations exiting')
     sys.exit(1)
   # imgidx has been set otherwise
   self.kp2 = orb.detect(imgidx,None) 
   self.kp2,self.des2 = orb.compute(imgidx,self.kp2) # sav indeximg kp des
 def desDists(self,img): # calc desc hamming dist between img and index img
  nfeats = self.nfts
  if len(img.shape) >=  3:
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  orb = cv2.ORB_create(nfeatures=nfeats) # init orb detector
  self.orb = orb # save orb
  kp = orb.detect(img,None)   
  kp, des = orb.compute(img, kp) # input imgkeypoints and feature descriptors
  if kp is None or des is None : return None
  hdist = []
  for i in range(self.nfts):
    hd = cv2.norm(des[i],self.des2[i],cv2.NORM_HAMMING)
    hd_tot = cv2.norm(des,self.des2,cv2.NORM_HAMMING)
    hdist.append(hd)
  return np.asarray(hdist,dtype=np.float64),np.float64(hd_tot)
  #return descriptors' hamming distances and their total 
def hu_invars(img): # Calcs all 7 Hu's moments
  if len(img.shape) >  2:
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  moments = cv2.moments(img)
  huM = cv2.HuMoments(moments)
  for i in range(0,7):
    huM[i] = -1* copysign(1.0, huM[i].item()) * log10(abs(huM[i].item()))
  return huM.flatten()
def imgDisplay(frame):
 cv2.imshow('Frame', frame)
 if cv2.waitKey(0) & 0xFF == ord('q'): 
    cv2.destroyAllWindows()
 return 0
def imgbw(im_gray):   #returns threshold,img_black_and_white
 if len(im_gray.shape) > 2: 
    im_gray = cv2.cvtColor(im_gray, cv2.COLOR_BGR2GRAY)
 return cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
def fsearch(fname,fstr): # search for a string in a text file
 with open(fname, 'r') as fp:
    lines = fp.readlines()
    for row in lines:
      x = row.find(fstr)
      if x != -1:
        return x # return index of 1st fstr occurence
 return -1 # fstr not found in file
def save_list(flist,fname):
 with open(fname, 'w') as f:
    for line in flist:
       f.write(f"{line}\n")
 return None
def chunk(lst, n): # breaks a list into equal sized n chunks
	for i in range(0, len(lst), n):
		# yields a chunk of the list 
		yield lst[i: i + n]
def workpacks(imgpath,chunks,workDir='./tmp-pkl'):
 wpcks = []
 for (i, images) in enumerate(chunks):
   outPath_fnames=os.path.join(workDir, 'proc_{}_fnames.pkl'.format(i))
   outPath_data=os.path.join(workDir, 'proc_{}_data.pkl'.format(i))
   fields={ 'id': i,
            'imgP': imgpath,
            'images': images,
            'outPath_fnames': outPath_fnames,
            'outPath_data': outPath_data
		  }
   wpcks.append(fields)
 return wpcks
def check_img(filename):
    try:
        im = Image.open(filename)
        im.verify() # IDK verify, sees other types o defects
        im.close() #reload is necessary in my case
        im = Image.open(filename) 
        im.transpose(Image.FLIP_LEFT_RIGHT)
        im.close()
        return True
    except: 
        print(filename,color.RED+"corrupted"+color.END)
        sys.stdout.flush()
        return False

if __name__ == '__main__':


   mt  = '+'+str(round(0.75*saoldestFile('./test_data')))
   print(mt)

   sadiskManage("./test_data",mt) 
#
   used = sadiskUse("/mnt/GR8GB")
   print(used,"%")
