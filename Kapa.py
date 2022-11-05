#!/bin/env python
import subprocess
import argparse
import pandas as pd
import csv
from openpyxl import Workbook
import xlsxwriter
from tabulate import tabulate
#import time
#d2= time.strftime ("%B %d, %Y %H:%M")
#print('|{}: \n'.format(d2))

def get_seconds_from_time(time):
    tominutes = [24 * 60 * 60, 60 * 60, 60, 1]
    tmp = []
    for f in time.split("-"):
        tmp += f.split(":")
    tmp = [0] * (4 - len(tmp)) + tmp
    minutes = sum([int(a)*b for a, b in zip(tmp, tominutes)])
    return minutes


def call_Kapadaten(PSP_list):
    dic = {i: [] for i in PSP_list}
    PSP_info =','.join(PSP_list)
    f = open('EXPORT_2022_10_21_ Kapadaten.XLSX')           # Mac and Linux
#    decode = f.readlines()[1:].decode('utf-8').splitlines()  # translating Excel Format
#    decode = f.encode('utf-8').strip()
#    data = pd.read_csv(r'EXPORT_2022_10_21_ Kapadaten.XLSX', encoding= 'unicode_escape')
#    data = csv.reader(data)
#    print(data)
    workbook = xlsxwriter.Workbook('EXPORT_2022_10_21_ Kapadaten.XLSX')
    print(workbook)
#    for a in decode:                                    #transformating data
#    for a in workbook:
#        anyline = a.split("|")
#        dic[a].append(anyline[4])                    # select the target variable
#return dic


# PART III   parsing Data with command line
PSP_list = [str(k) for k in range(1311873)[1006245:-1]]
# define Parser
parser = argparse.ArgumentParser(
        prog='Kapa.py',
        usage='%(prog)s [options]',
        description='Walltimes based on PSP_Elements partition(s)'
        )
# add arguments
parser.add_argument(
        '-p',
        '--psp_element',
        nargs=1,
        help="display informations for psp_element ")
parser.add_argument(
        '-part',
        '--partition',
        action='store_true',
        help="display informations for the partition ")
parser.add_argument(
        '-sc',
        '--score',
        action='store_true',
        help="display gradient score")
#  parse derivates
args = parser.parse_args()

# PART DERIVATES
#statements
if args.partition:
    parts = args.partition[0].split(',')
    for anyelement in parts:
        if anyelement not in PSP_list:
            print ('   error - please check list of Projects again .  ')
            exit(1)
    PSP_list = parts

Kapadaten = call_Kapadaten(PSP_list)
if args.psp_element:
    for elem in PSP_list:
        if elem == args.psp_element:
            print(elem)
#if args.score:
#    print
else:
    print(Kapadaten)
