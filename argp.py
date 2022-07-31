#!/usr/bin/env python
import argparse
import subprocess
from tabulate import tabulate
#  first call sinfo to get a list of available partitions
#  and save it in partition_list
sinfo = subprocess.run([
        "sinfo", "-o", "%R"],
        stdout=subprocess.PIPE, shell=False)
decode = sinfo.stdout.decode('utf-8').splitlines()
partition_list = [i for i in decode[1:-1]]
#  define set-lists that one would want to separate waitingtimes into;
#  to adapt time repartitions perform changes in head_lists
interval_mem = [0]
interval_cpu = [0]
#  it is important to leave a space inbetween values and units
#  in head lists; start at 4GBh & 3CPUh
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


#  to return average waitingtimes for a single partition:
#  param=mem/cpu, dic is a dictionary with the asked partition;
#  for each waitingtime -> exact one string format !
def get_waiting_averages(partition, param, dic):
    averages = [partition]
    if param == 'cpu':
        interval = interval_cpu
    elif param == 'mem':
        interval = interval_mem
#  lst records the values the different categories
#  lt records the number of occurences
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


#  to convert output in secondes, minutes, hours, days, and weeks;
#  averages should be a list of average waitingtimes in seconds,
#  with a single partition as first entry;
#  find the number of jobs recensed in brackets
def get_datings_from_average(averages):
    datings = [averages[0]]
    times = [0, 60, 3600, 86400, 604800]
    dates = ['s', 'm', 'h', 'd', 'w']
    var = [1, 60, 3600, 3600/24, 3600/24/7]
    for t in averages[1:]:
        if t[0] == 0:
            datings.append('NA')
        for s in range(len(times)-1):
            if times[s] < t[0] <= times[s+1]:
                date = dates[s]
                value = [round(t[0]/var[s], 1), t[1]]
                datings.append(f'{value[0]} {date} ({value[1]})')
        if t[0] > times[-1]:
            datings.append(f'{round(t[0]/var[-1], 1)} {dates[-1]} ({t[1]})')
    return datings


#  define parser
parser = argparse.ArgumentParser(
            prog='argp.py',
            usage='%(prog)s [options]',
            description='Walltimes based on selected partition(s)'
            ' in CPUh and GBh')
#  define parser arguments
parser.add_argument(
            '-p',
            '--partition',
            nargs=1,
            help='display walltimes based on number of CPU')
parser.add_argument('-m',
                    '--mem',
                    action='store_true',
                    help='display walltimes based on required memory')
args = parser.parse_args()
#  define parser statements
if args.partition:
    m = args.partition[0].split(',')
#  make sure sacct doesn't run if command is'nt true
    for n in m:
        if n not in partition_list:
            print('error - please call_sacct_for existing partition(s)')
            exit(1)
    partition_list = m
#  it is important to call sacct only one time,
#  to limit waitingtime of the programm itself
sacct = call_sacct(partition_list)
if args.mem:
    output = [minGB_head]
    for i in partition_list:
        mem = get_datings_from_average(get_waiting_averages(i, 'mem', sacct))
        output.append(mem)
    print(tabulate(output, headers='firstrow'))
else:
    output = [minCPU_head]
    for i in partition_list:
        cpu = get_datings_from_average(get_waiting_averages(i, 'cpu', sacct))
        output.append(cpu)
    print(tabulate(output, headers='firstrow'))
