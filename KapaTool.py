#!/bin/env python
import subprocess
import argparse
import pandas as pd
import openpyxl
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


def import_xlsx(filename):
    """Import Excel 2007 workbook (.xlsx) as a list-of-lists."""
    data = []
    wb = openpyxl.load_workbook(filename)           # use openpyxl to import and read excel data
    for sheetname in wb.sheetnames:
        sh = wb[sheetname]
        for row in sh.values:
            data += [list(row)]
    return data


def call_Kapadaten_withauftrag(Auftrag_list):
    dic = {a: [] for a in Auftrag_list}
#    f = open('EXPORT_2022_10_21_ Kapadaten.XLSX')           # Mac and Linux
#    decode = f.readlines()[1:].decode('utf-8').splitlines()  # translating Excel Format
    for anyline in import_xlsx('EXPORT_2022_10_21_ Kapadaten.XLSX')[1:]:                   # here it begins at 1 because 0 just contains inscriptions and labels
        for Auftragnumber in Auftrag_list:
            if anyline[4] == Auftragnumber:
                dic[Auftragnumber].append(anyline)                    # select the target variable
    return dic


def call_Kapadaten(PSP_list):
    dic = {i: [] for i in PSP_list}
    for anyline in import_xlsx('EXPORT_2022_10_21_ Kapadaten.XLSX')[1:]:
#        print(line[4])
        for PSP_project in PSP_list:                # means the first 6 entries in PSP_Element
            if anyline[0].split('-')[0] == PSP_project:
                dic[PSP_project].append(anyline)                    # select the target variable
    return dic


# PART III   parsing Data with command line
# using Python's exception handling
Auftrag_list = [str(k) for k in range(1311873)[1006240:-1]]

G1 =['G'+str(k) for k in [int("00058"), int('00296'), int('00313'), int('00001'), int('00002'), int('00003'), int('00309')]]
G2 = ['G'+str(k) for k in range(10090)[ 10002: ]]
#B = ['B'+str(k) for k in [p for p in range(int('00001'))[int('00020')]] ]  #    min : 10038      max : 1311873
#D = ['D'+str(k) for k in [p for p in range(int('00001'))[int('00020')]] ]  #    min : 10038      max : 1311873
PSP_list = G1 + G2 # + B + D      #   Direkte SUmme
#print(f'Choices:in G1 ~ {G1} and G2 ~ [G10001 -bis G10089]')


# define Parser
parser = argparse.ArgumentParser(
        prog='Kapa.py',
        usage='%(prog)s [options]',
        description='Walltimes based on PSP_Elements partition(s)'
        )
# add arguments
parser.add_argument(
        '-a',
        '--auftrag',
        nargs=1,
        help="display informations for the Auftragnumber ")
parser.add_argument(
        '-p',
        '--psp_element',
        nargs=1,
        help="display informations for psp_element ")
#parser.add_argument(
#        '-part',
#        '--partition',
#        action='store_true',
#        help="display informations for the partition ")
#parser.add_argument(
#        '-sc',
#        '--score',
#        action='store_true',
#        help="display gradient score")
#  parse derivates
args = parser.parse_args()

# PART DERIVATES
#statements
if args.auftrag:
    Input = args.auftrag[0].split(',')
    for anyauftrag in Input:
        if anyauftrag not in Auftrag_list:
            print('   error - please check list of project Auftrag again .  ')
            exit(1)
    Auftrag_list = Input
    print(call_Kapadaten_withauftrag(Auftrag_list))
    exit(1)
Kapadaten = call_Kapadaten(PSP_list)        # call Kapadaten just one time for reducing waitingtime of the programm
if args.psp_element:
    print(f'Choices:in G1 ~ {G1} and G2 ~ [G10001 -bis G10089]')
    Input = args.psp_element[0].split(',')
    for anyelement in Input:
        if anyelement not in PSP_list:
            print('   error - please check list of PSP_Element again .  ')
            exit(1)
        else:
            Kapadaten = call_Kapadaten(PSP_list)        # call Kapadaten just one time for reducing waitingtime of the programm
    print(Kapadaten[anyelement])
#else:
#    for PSP_element in Kapadaten:
#        if Kapadaten[PSP_element][]:
#        print(Kapadaten[k])
