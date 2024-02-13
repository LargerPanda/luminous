import os
import random
#import numpy as np
import time
import sys
#from prettytable import PrettyTable
#import datetime
import math

#python3 /users/hys/env/luminous/src/os/bluestore/test.py
#该实验用于得到1-1024k的请求与大小的关系
final_bandwidth={}
print("start testing")

testcase = [8]

fd1 = open("/users/hys/volume-bandwidth.txt", "a")
#fd1.write("iosize bandwidth\n")    
#for iosize in range(3,4):
#for iosize in testcase:
for iosize in range(8,100):
    #修改配置配置文件
    #if iosize%4==0:
    if True:
        run_cmd = "/users/hys/env/fio/bin/fio -filename=/users/hys/cephrbd/test -direct=1 -iodepth 10 -thread -rw=randwrite -ioengine=psync -bs=512K -size=%dK -numjobs=10 -runtime=180 -group_reporting -name=rand_100write_4k"%(iosize*512)
        #print(run_cmd)
        avg = 0.0
        stdev = 0.0
        avg_total = 0.0
        stdev_total = 0.0
        for i in range(2):
            with os.popen(run_cmd, "r") as p:
                r = p.readlines()
                find=0
                for line in r:
                    #print(line)
                    #print(line[3:7])
                    if line[3:7] == "bw (":
                        find=1
                    if find == 1:
                        #print(line)
                        i = line.find('avg=')
                        j = line.find(',',i+4)
                        #print(line[i+1:j])
                        avg = float(line[i+4:j])
                        
                        i = line.find('stdev=')
                        j = line.find(',',i+6)
                        #print(line[i+1:j])
                        stdev = float(line[i+6:j])

                        #print(bw)
                        break
            avg_total = avg_total+avg
            stdev_total = stdev_total+stdev
            time.sleep(3)
        avg = avg_total/2
        stdev = stdev_total/2
        fd1.write(str(iosize)+" "+str(avg)+" "+str(stdev)+"\n")
        fd1.flush()
        time.sleep(5)    

fd1.close()
