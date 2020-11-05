import numpy as np
#import scipy.stats
import argparse
import time
from datetime import datetime
import sys
import os
import csv
from scipy.stats import t
from scipy import sqrt
from statistics import variance, mean 
def int_ech(values,conf=0.95) :
    n = len(values) 
    m = mean(values) 
    s = variance(values)
    proba = (1-conf)*100 ; proba = (100-proba/2)/100 
    ddl = n - 1
    intervalle = sqrt(s/n) * t.ppf(proba, ddl)
    return m,intervalle
######## ARGS definition ######
parser = argparse.ArgumentParser()
parser.add_argument("--data","-d",help="absolute path of dataset.csv",required=True)
args = parser.parse_args()
##############################
Data = args.data

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, h, m-h, m+h


#dataset = pd.read_csv(Data)
i=1
now = datetime.now()
timestamp = datetime.timestamp(now)

f = open("rtt-"+str(timestamp)+".csv","w")
f.write("time,mean,error\n")
while i < 100:
    item = []
    tr = open(Data,"r")
    csv_reader = csv.reader(tr, delimiter=',')
    j=0
    for row in csv_reader:
        #print(row[0])
        if int(row[0]) == i:
            item.append(float(row[1]))
            
    if len(item) > 0:
        m,ci = int_ech(item)
        f.write("{},{},{}\n".format(i,m,ci))
        #fr.write("({},{})  +- ({},{})\n".format(i,mean,high,low))
    tr.close()
    i +=1
f.close()
