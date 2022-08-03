#!/usr/bin/env python
##############################################
#  PART I : Configs and automation-functions #
##############################################
import time
#  print Time/Day/Hour
d2= time.strftime ("%B %d, %Y %H:%M")
print('|{}: \n'.format(d2))
from tabulate import tabulate
import pandas as pd
import subprocess

#  Define partition list
partition_list =['fat+', 'medium', 'fat', 'int', 'gpu']


#  Define automation-functions
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
    sacct = subprocess.run([
            "sacct", "-a", "-X", "-T", "-p",
            "-r", partitions, "-o",
            "reserved, partition, ReqMem, ReqCPUS, Timelimit",
            "-sCD,R", "-Snow-7days", "-Enow"],
            stdout=subprocess.PIPE, shell=False)
#    f = open('slurm_outputs/slurm_output0')           # Mac and Linux
#    decode = f.readlines()[1:]
    decode = sacct.stdout.decode('utf-8').splitlines()[2:]
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


#  to display waitingtimes for any single partition, where
def get_waiting_averages(partition, param, dic):
    averages = [partition]
    if param == 'cpu':
        interval = interval_cpu
    elif param == 'mem':
        interval = interval_mem
#  'dic' is a dictionary including waitingtimes for all partition
#  lst records the waiting time for every single job
#  lt records the number of jobs
    lst = [0]*(len(interval))
    lt = [0]*(len(interval))
    for i, j, k in dic[partition]:
        if param == 'cpu':
            m = k
        elif param == 'mem':
            m = j
        for s in range(len(interval)-1):
            if interval[s] < m <= interval[s+1]:
                lst[s] = lst[s] + i
                lt[s] = lt[s] + 1
        if m > interval[-1]:
            lst[-1] = lst[-1] + i
            lt[-1] = lt[-1] + 1
#  b or 1 ensures non-zero division
    for a, b in zip(lst, lt):
        averages.append([round(a/(b or 1), 2), b])
    return averages


#  to automate the value of the output-waitingtimes
#  secondes, minutes, hours, days or weeks
def get_walltimes(averages):
    datings = [averages[0]]
    times = [0, 60, 3600, 86400, 604800]
    dates = ['s', 'm', 'h', 'd', 'w']
    var = [1, 60, 3600, 3600/24, 3600/24/7]
    for t in averages[1:]:
        if t[0] == 0:
#            datings.append(0)
            datings.append('NA')
        for s in range(len(times)-1):
            if times[s] < t[0] <= times[s+1]:
                date = dates[s]
                value = [round(t[0]/var[s], 1), t[1]]
                datings.append(f'{value[0]} {date} ({value[1]})')
        if t[0] > times[-1]:
            datings.append(f'{round(t[0]/var[-1], 1)} {dates[-1]} ({t[1]})')
    return datings


##############################################
#  PART II : DATA STANDARDIZING & MODELLING  #
##############################################


#  Give number of accounted jobs for each partition
sacct = call_sacct(partition_list)        
for i in sacct:
    print("For partition {}, there was {} jobs on the queue".format(i, len(sacct[i])))

#  reduce number of raws to minimum available for all partitions and check 
nb_jobs_per_partition = []
for i in sacct:
    j = len(sacct[i])
    nb_jobs_per_partition.append(j)
Param = min(nb_jobs_per_partition)

#  check
Limited_dic = {j: sacct[j][:1000] for j in sacct}
print("\n Trained data: \n Partition | Number of jobs")
for i in Limited_dic:
    print("       {}    {}".format(i, len(Limited_dic[i])))

#  standardize Designmatrix, to model output-Data
ping = {'fat+': [], 'medium': [], 'fat': [], 'int': [],
                        'gpu': []}
ring = {i: [] for i in partition_list}
interval_mem = [0]
interval_cpu = [0]
minGB_head = [
    "Partition", "< 4 GBh", " 4 GBh -  256 GBh", "256 GBh - 1024 GBh",
    "1024 GBh - 51200 GBh", "51200 GBh - 102400 GBh", "> 102400 GBh"]
minCPU_head = [
    "Partition", "< 3 CPUh", "3 CPUh - 15 CPUh",
    "15 CPUh - 30 CPUh", "30 CPUh - 150 CPUh",
    "150 CPUh - 300 CPUh", "> 300 CPUh"]
for a, b in zip(minGB_head[1:-1], minCPU_head[1:-1]):
    interval_cpu.append(3600*int(b.split(' ')[-2]))
    interval_mem.append(3600*1024*int(a.split(' ')[-2]))
output = [minGB_head]
for i in partition_list:
    mem = get_walltimes(get_waiting_averages(i, 'mem', sacct))
    output.append(mem)
    ping[i] = mem[1:]
print("\nWalltime partitionning with complete data \n {}\n".format(tabulate(output, headers='firstrow')))

##############################################
#  PART III : DISPLAY TRAINED WALLTIMES      #
##############################################
import matplotlib.pyplot as plt
#  Display transformed Designmatrix
#  with adequated columns and rows
for i in partition_list:
    mem = get_walltimes(get_waiting_averages(i, 'mem', Limited_dic))
    ring[i] = mem[1:]
act1 = pd.DataFrame(ring).T
act1.columns = minGB_head[1:]
print("Walltime partitioning with trained data \n {} ".format(act1))
for i in minGB_head[1:]:
    for j in partition_list:
        if act1[i][j] == 'NA':
            act1[i][j] = act1[i][j].replace('NA', '0')
        else:
            continue

times = [1/60, 1, 60, 1440, 10080]
dates = ['s', 'm', 'h', 'd', 'w']
for i in minGB_head[1:]:
    for j in partition_list:
        if act1[i][j] == '0':
            continue
        else:
            a = act1[i][j].split(' ')[0]
            b = act1[i][j].split(' ')[1]
            k = dates.index(b)
            act1[i][j] = act1[i][j].replace(act1[i][j], str(float(a)*times[k]))
print("Walltime partitioning in minutes with trained data \n{}\n".format(act1))
#act0 = act1.to_dict()
#print(act0)
##############################################
#                   END                      #
##############################################
