#!/usr/bin/env python
from string import Template
tp_str= 'Hi $name, welcome to $site'
tp_obj= Template(tp_str)
print(tp_obj.substitute(name= 'HOn Doe', site = 'StackStatistics.com'))

from datetime import date
import time
d2= time.strftime ("%B %d, %Y %H:%M")
today = date.today() #or import datime.date.today as today
d1 = today.strftime("%B %d, %Y %H:%M")
print('|{}: \n'.format(d2))

import subprocess
import numpy as np
output1 = subprocess.run(['squeue --format=%F'], stdout= subprocess.PIPE, shell=True)
output2 = subprocess.run(['squeue --format=%T'], stdout= subprocess.PIPE, shell=True)
list1=  output1.stdout
list2= output2.stdout.splitlines()
list= [list1, list2]

cp=0
count=0
count1=0
for arg in list[1]:
	if arg == b'PENDING':
		count=count+1
		
	elif arg == b'RUNNING':
		count1=count1+1
			
	elif arg == b'COMPLETING':
		cp=cp+1
#out = subprocess.run(["sacct -a -X -o jobid,Eligible,reserved,start,state,alloccpu,Elapsed,cpu,partition,Timelimit -s R 
#outp=  out.stdout.decode('utf -8').splitlines()

print('There are {} pending and {} running jobs on the queue'.format( count, count1) )
print('{} Jobs are completing right now'.format(cp))

def average(x, a=count, b=count1):
	c=len(x)-1
	pj=round(100*a/c , 2) ;rj=round(100*b/c, 2) ;cj=round(100*cp/c , 2)	
	return 'More Stats:\n Average: {}% completing, {}% pending and {}% running'.format(cj, pj, rj)
	       
	       
print(average(list2))  #estimated runtime=?	


output1 = subprocess.run(['squeue --format=%F'], stdout= subprocess.PIPE, shell=True)
output2 = subprocess.run(['squeue --format=%T'], stdout= subprocess.PIPE, shell=True)
list1=  output1.stdout.decode('utf-8').splitlines()
list2= output2.stdout.decode('utf-8').splitlines()
list= [list1,list2]
wb={}
myrunninglist=[]
#for i in list1:
#	ind=list1.index(i)
#	wb[i]=list2[ind]
#       if wb[i]=='RUNNING':
#               myrunninglist.append(i)
#	print(myrunninglist)

		
##Mean waiting time calculation:

out = subprocess.run(['squeue --Format=PendingTime'], stdout= subprocess.PIPE, shell=True)
outp=  out.stdout.decode('utf-8').splitlines()

#out1 = subprocess.run(['sacct --Format=EndTime'], stdout= subprocess.PIPE, shell=True)
#outp1=  out1.stdout.decode('utf-8').splitlines()

#out2 = subprocess.run(['squeue --Format=StartTime'], stdout= subprocess.PIPE, shell=True)
#outp2=  out2.stdout.decode('utf-8').splitlines()

lst=[]
for i in outp[1:]:
	j=int(i)
	lst.append(j)
print('The mean pending time is about {} hours per job'.format(round((sum(lst)/len(lst))/3600 ,2)))
