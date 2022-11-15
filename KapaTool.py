#!/bin/env python3.9
import argparse
import pandas as pd
import time
import numpy as np
from tabulate import tabulate
d2= time.strftime ("%B %d, %Y %H:%M")
print('|{}: \n'.format(d2))
data = pd.read_excel(r'/home/mint/Documents/Pyprojekt/EXPORT_Kapatool_Auftragskopf_2022_11_14.XLSX')
data_frame = pd.DataFrame(data, columns=["Auftrag", "Kunden Code PSP", "PSP-Element", "Systemstatus"])
data = data_frame[["Auftrag", "Kunden Code PSP", "PSP-Element", "Systemstatus"]]
def call_Kapadaten_withauftrag(Auftrag_list, dataframe, param):
    for k in Auftrag_list:
        frame = dataframe.T[[int(k)]].T
        #frame.index = frame.index.astype(int)
        if param == False:
            print(f'{frame} \n')
        elif param == True:
            data = pd.read_excel(r'/home/mint/Documents/Pyprojekt/EXPORT_Kapatool_Vorgänge_2022_11_14.XLSX')
            data_frame = pd.DataFrame(data, columns=["Auftrag", "Kurztext Vorgang", "Systemstatus", "Vorgangsmenge (MEINH)", "Mengeneinheit Vrg. (=MEINH)", "Fr.term.St.dat.Durchf", "Fr.term.Enddat.Durchf", "Rückgemeld. Leist. 1 (ILE01)",                                                       "Vorgabewert 3 (VGE03)", "Rückgemeld. Leist. 3 (ILE03)", "Bearbeitungszeit (BEAZE)"])
            data = data_frame[["Auftrag", "Kurztext Vorgang", "Systemstatus", "Vorgangsmenge (MEINH)", "Fr.term.St.dat.Durchf", "Fr.term.Enddat.Durchf", "Vorgabewert 3 (VGE03)", "Rückgemeld. Leist. 3 (ILE03)", "Bearbeitungszeit (BEAZE)"]].set_index("Auftrag")
            data = data.T[[k]].T
            data["Geplannte_Bearb_zeit"] = data["Fr.term.Enddat.Durchf"] - data["Fr.term.St.dat.Durchf"]
            data.index = data.index.astype(int)
            print(f'{data}')
            print(f'{frame} \n \n')
def plane(Input, param):
    details = pd.read_excel(r'/home/mint/Documents/Pyprojekt/EXPORT_Kapatool_Vorgänge_2022_11_14.XLSX')
    details_frame = pd.DataFrame(details, columns=["Auftrag", "Kurztext Vorgang", "Systemstatus", "Vorgangsmenge (MEINH)", "Mengeneinheit Vrg. (=MEINH)", "Fr.term.St.dat.Durchf", "Fr.term.Enddat.Durchf", "Rückgemeld. Leist. 1 (ILE01)",                                                       "Vorgabewert 3 (VGE03)", "Rückgemeld. Leist. 3 (ILE03)", "Bearbeitungszeit (BEAZE)"])
    details = details_frame[["Auftrag", "Kurztext Vorgang", "Systemstatus", "Vorgangsmenge (MEINH)", "Fr.term.St.dat.Durchf", "Fr.term.Enddat.Durchf", "Vorgabewert 3 (VGE03)", "Rückgemeld. Leist. 3 (ILE03)", "Bearbeitungszeit (BEAZE)"]].set_index("Auftrag")
    print("Example of list: for Status parameter given with --partition \n  \n  \n ")
#    new_df_FREI = details.loc[details["Systemstatus"] == "FREI"]
#    print(new_df_FREI)
    dic_of_status = {STATUS:[] for STATUS in details["Systemstatus"]}
    for k in dic_of_status:
        status  = details.loc[details["Systemstatus"] == k]
        dic_of_status[k].append(status)
    for status in Input:
        if param == True:
            print(dic_of_status[status][0])
###########################################################################Up to here it is about choosing the axis we want to sum up over
            print(dic_of_status[status][0].sum(axis=0, numeric_only=bool))
        if param == False:
            exit(1)




        



#    list_with_auftrag = [details.loc[details["Systemstatus"] == k]]
#    print(dic_of_status)
#    info_line = pd.DataFrame(dic_of_status)
#    print(info_line)
#    for status in dic_of_status:
#        for k in details.index:
#            print(k)
#            if details.T[[k]][2] == status:
#                info_line[[status]] = details.loc[k][0:]
#    print(info_line)













parser = argparse.ArgumentParser(
        prog='Kapatool.py',
        usage='%(prog)s [options]',
        description='Walltimes based on Auftrag number & IST/SOLL Analysis')
parser.add_argument(
        '-a',
        '--auftrag',
        nargs=1,
        help="-a, or --auftrag for Walltimes based on Auftragnumber")
parser.add_argument(
        '-d',
        '--details',
        action='store_true',
        help="-d, --details for printing all additional IST/SOLL informations")
parser.add_argument(
        '-p',
        '--partition',# function to plane with the state status
        nargs=1,
        help="-d, --details for printing all additional IST/SOLL informations")

args = parser.parse_args()
data = data.set_index("Auftrag")
rows = []
if args.auftrag:
    Input = args.auftrag[0].split(',')
    for k in Input:
        if int(k) not in data.index:
            print(f'Error -  please check for correct Auftrag number again: {k}')
        else:
            rows.append(k)
if args.details:
    call_Kapadaten_withauftrag(rows, data, param=True)
    exit(1)
elif args.auftrag:
    call_Kapadaten_withauftrag(rows, data, param=False)
if args.partition:
    Input = args.partition[0].split(',')
    plane(Input, param=True)
