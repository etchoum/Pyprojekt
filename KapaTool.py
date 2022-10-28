#!/usr/bin/env python
import argparse
import subprocess
from tabulate import tabulate
import time
#  print Time/Day/Hour
d2= time.strftime ("%B %d, %Y %H:%M")
print('|{}: \n'.format(d2))


#################################################################
#  Part I : General Configurations                              #
#################################################################
partition_list = [ k for k in [1006245:1311872]]
minGB_head = [
    "PSP-Element", "KapBearb.-Sollbed.", "KapBearb.-Restbed.", "KapAbrüst-Sollbed.", "KapAbrüst-Restbed."] 



#################################################################
#  Part II : Automation-Functions for PARSING                   #
#################################################################

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
#    decode = sacct.stdout.decode('utf-8').splitlines()[2:]
    f = open('slurm_outputs/slurm_output0')           # Mac and Linux
    decode = f.readlines()[1:]
    for a in decode:
        line = a.split("|")
#  in case some informations should be missing
#  calculated waitingtimes have to remind trustfull
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



#################################################################
#  Part III : PARSING waitingtimes with the commandline         #
#################################################################
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

#  call 'sacct' only one time,
#  to limit bugs occurence in the programm itself
sacct = call_sacct(partition_list)
#  and give parser conditions
if args.mem:
    output = [minGB_head]
    for i in partition_list:
        mem = get_walltimes(get_waiting_averages(i, 'mem', sacct))
        output.append(mem)
    print(tabulate(output, headers='firstrow'))
else:
    output = [minCPU_head]
    for i in partition_list:
        cpu = get_walltimes(get_waiting_averages(i, 'cpu', sacct))
        output.append(cpu)
    print(tabulate(output, headers='firstrow'))


#################################################################
#                               END                             #
#################################################################
