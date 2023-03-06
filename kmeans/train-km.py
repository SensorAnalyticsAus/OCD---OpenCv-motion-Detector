#!/usr/bin/python

import sys
if len(sys.argv) < 5:
   print('USAGE: 0|1 numClusters YYYYDDMMHHMMSS YYYYMMDDHHMMSS')
   print('0:Elbow Analyses 1:Actual KMeans YYYYDDMMHHMMSS: from -> to date-')
   print('time range (HHMMSS field in 24-hour clock format)')
   sys.exit(1)
sys.path.append('..')
import numpy as np
from sklearn.cluster import KMeans
import pickle
import matplotlib.pyplot as plt
from sautils3_1 import genRows
import matplotlib
import os

datapath='../log/MD.log'
if not os.path.exists(datapath):
    print('fix datapath in this code, it  does not exist!',datapath)
    sys.exit(1)
mname = 'km_model.pkl' # trained km model saved as

##########  Data Input and Normalization Block ##########
opt = int(sys.argv[1]) # 0 for elbow analyses 1 for actual km clustering
nC = int(sys.argv[2]) # number of clusters for elbow analyses or training 
st_d_t = int(sys.argv[3]) # start date time YYYYMMDDHHMMSS for training set
en_d_t = int(sys.argv[4]) # end date time YYYYMMDDHHMMSS for training set
if len(sys.argv[3]) !=14 or len(sys.argv[4]) !=14: 
    print('input datetime error')
    sys.exit(1)
z = genRows(datapath, st_d_t, en_d_t)
fnames = np.loadtxt(z,usecols=0,dtype='str')
# 0-fn/n,01-dec_t/y,02-cnts/y,03-cnts_a/y,04-ent/n,05-ent_bw/y
z = genRows(datapath, st_d_t, en_d_t) # rest generator for re-use
data = np.loadtxt(z,usecols=(1,2,3,5))
datamax = data.max(axis=0) #later for scaling prediction vector
dataNormed = data/datamax
np.savetxt('datamax.txt',datamax) # datamax saved for this run
np.savetxt('fnames.txt',fnames,delimiter=" ",fmt="%s") # fnames also saved 

######### Elbow Analyses and Display Block ###############
if opt == 0:
    matplotlib.use('TkAgg') # to avoid cv2 qt conflict
    inertias = []

    print('Getting ready to display')
    for i in range(1,int(sys.argv[2])):
        print('.',end='')
        km = KMeans(n_clusters=i)
        km.fit(dataNormed)
        inertias.append(km.inertia_)
    print('\n')

    print('press [q] inside the display chart to end')
    plt.plot(range(1,int(sys.argv[2])), inertias, marker='o')
    plt.title('Elbow method')
    plt.xlabel('Number of clusters')
    plt.ylabel('Inertia')
    plt.show(block=True) 
    sys.exit(0)
################### KMeans Block ################################
print('ready to train KMeans with:',nC,'clusters')
km = KMeans(n_clusters=nC)
km.fit(dataNormed)
pickle.dump(km, open(mname, 'wb')) # dump trained model
print('KMeans trained model saved as:',mname)
