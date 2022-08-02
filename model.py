#!/usr/bin/env python
#  Define partition list
partition_list =['fat+', 'medium', 'fat', 'int', 'gpu']
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
    f = open('slurm_outputs/slurm_output0')           # Mac and Linux
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

sacct = call_sacct(partition_list)
for i in sacct:
    print("For partition {}, there is {} available".format(i, len(sacct[i])))


#  reduce number of raws to minimum available for all partitions and check 
min_jobs = []
for i in sacct:
    j = len(sacct[i])
    min_jobs.append(j)

Param = min(min_jobs)
Limited_dic = {j: sacct[j][:Param] for j in sacct}
for i in Limited_dic:
    print(i, len(Limited_dic[i]))


#  to model data output
import pandas as pd
#  standardize Designmatrix
ring = {'fat+': [], 'medium': [], 'fat': [], 'int': [],
                        'gpu': []}
for i in ring:
    for j in Limited_dic[i]:
#        for k in j:
#            set_lst=[]
#            set_lst.append(str(k))
#            string="-".join(set_lst)
        string=j[]
        ring[i].append(string)
acct = pd.DataFrame(ring, columns=['fat+', 'medium', 'fat', 'int',
                        'gpu'])
print(acct)



