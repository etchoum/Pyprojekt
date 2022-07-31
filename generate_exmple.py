#!/usr/bin/env python
import time
d2= time.strftime ("%B %d, %Y %H:%M")
print('|{}: \n'.format(d2))
#####################################
import argparse
import subprocess
from tabulate import tabulate


#  first call sinfo to get a list of available partitions
#  and save it in partition_list
#sinfo = subprocess.run([
#        "sinfo", "-o", "%R"],
#        stdout=subprocess.PIPE, shell=False)
#decode = sinfo.stdout.decode('utf-8').splitlines()
#partition_list = [i for i in decode[1:-1]]
partition_list =['fat+', 'medium', 'fat', 'int', 'gpu']


#####################################
#  define functions
#  to convert ReqMem in MB
def get_MB_from_mem(mem):
    memory = mem[:-1]
    if 'M' in mem:
        memory = float(memory)
    elif 'G' in mem:
        memory = 1024*float(memory)
    elif 'T' in mem:
        memory = 1024**2*float(memory)
    return memory


#  to convert time format [DD-[HH:]]MM:SS in secondes
def get_seconds_from_time(time):
    tosec = [24 * 60 * 60, 60 * 60, 60, 1]
    tmp = []
    for f in time.split("-"):
        tmp += f.split(":")
    tmp = [0] * (4 - len(tmp)) + tmp
    seconds = sum([int(a)*b for a, b in zip(tmp, tosec)])
    return seconds


#  to call sacct stored data from any partition list
def call_sacct(partition_list):
    dic = {i: [] for i in partition_list}
    partitions = ','.join(partition_list)
#    sacct = subprocess.run([
#            "sacct", "-a", "-X", "-T", "-p",
#            "-r", partitions, "-o",
#            "reserved, partition, ReqMem, ReqCPUS, Timelimit",
#            "-sCD,R", "-Snow-1days", "-Enow"],
#            stdout=subprocess.PIPE, shell=False)
    f = open('slurm_outputs/slurm_output1')           # Mac and Linux
    decode = f.readlines()[1:]
    for a in decode:
        line = a.split("|")
#  in case some informations should be missing
#  waitingtimes have to remind trustfull
        if line[0] == '' or line[4] == 'UNLIMITED':
            continue
        a_1 = get_seconds_from_time(line[0])
        a_2 = str(line[1])
        a_3 = get_MB_from_mem(line[2])
        a_4 = int(line[3])
        a_5 = get_seconds_from_time(line[4])
#  save waiting/reservedtime(in seconds),
#  timelimit*memory(in memh), timelimit*CPUs(in CPUh), resp. in dic
        dic[a_2].append((a_1, a_5*a_3, a_5*a_4))
    return dic


##################################
#  check how much of data is available to display
sacct = call_sacct(partition_list)
for i in sacct:
    print("For partition {}, there is {} available".format(i, len(sacct[i])))


#  reduce number of raws and check ; hier n=7
Limited_dic = {j: sacct[j][:7] for j in sacct}
for i in Limited_dic:
    print(i, len(Limited_dic[i]))


cp=0
count=0
count1=0
for arg in sacct:
    if arg == b'PENDING':
        count=count+1
    elif arg == b'RUNNING':
        count1=count1+1
    elif arg == b'COMPLETING':
        cp=cp+1
print('There are {} pending and {} running jobs on the queue'.format( count, count1) )
print('{} Jobs are completing right now'.format(cp))


#  
def average(x, a=count, b=count1):
    c=len(x)-1
    pj=round(100*a/c , 2) ;rj=round(100*b/c, 2) ;cj=round(100*cp/c , 2) 
    return 'More Stats:\n Average: {}% completing, {}% pending and {}%running'.format(cj, pj, rj)
print(average(sacct))    
 
##  Mean waiting time calculation:

lst=[]
for i in sacct:
    j=int(sacct[i])
    lst.append(j)
print('The mean pending time is about {} hours per job'.format(round((sum(lst)/len(lst))/3600 ,2)))










#  to model data output
import pandas as pd
#  standardize Designmatrix
ring = {'fat+': [], 'medium': [], 'fat': [], 'int': [],
                        'gpu': []}
for i in ring:
    for j in Limited_dic[i]:
        for k in j:
            set_lst=[]
            set_lst.append(str(k))
            string="-".join(set_lst)
            ring[i].append(string)
acct = pd.DataFrame(ring, columns=['fat+', 'medium', 'fat', 'int',
                        'gpu'])
print(acct)
