#!/usr/bin/env python
import time
from datetime import date
d2= time.strftime ("%B %d, %Y %H:%M")
#print('|{} \n'.format(d2))

from flask import Flask, jsonify, request
import json
import subprocess
out= subprocess.run(["sacct -a -X -o jobid,Eligible,reserved,start,state,alloccpu,Elapsed,ReqCPUS,partition,TimelimitRaw -s CD,R -S $(date -d '7 day ago' +%D-%R) -E now"], stdout=subprocess.PIPE, shell=True)
outp= out.stdout.decode('utf -8').splitlines()
app= Flask(__name__)


@app.route('/')

def separe(list=outp):
	CD=[]
	R=[]
	wb={}
	mdm=[]
	fat=[]
	timecnt=0
	for line in list[2:]:
		j=line.split()
		wb[j[0]]=j[8],j[6]
		if j[8]=='medium': mdm.append(j[9])
		elif j[8]=='fat': fat.append(j[9])
		k= j[6]	 #elapsed
		l=k.split(':')
		n= l[0]   #Tage '-'/und Stunden
		m= int(l[1])	  #Minuten
		sek= int(l[2])    #Sekunden
		if 'COMPLETED' in line and '-' not in k and int(n)==0 and m<5  :
			CD.append(round((m*60+sek)/60 , 2))
#for percentage			timecnt=timecnt+round((m*60+sek)/60 , 2)
		elif 'RUNNING' in line and '-' not in k and int(n)==0 and m<5:
			R.append(round((m*60+sek)/60 , 2))
#for pencentage			timecnt=timecnt+round((m*60+sek)/60 ,2)
	return jsonify(d2,
                    'There was {} jobs completed in less than 5 minutes in the last 7 days with average runningtime {} minutes/job and {} jobs are still running with average running time {} minutes/job '.format( len(CD), round( sum(CD)/len(CD), 2) , len(R), round( sum(R)/len(R), 2)) ,
                    wb)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')

