#!/bin/env python3.9
import argparse
import pandas as pd
import time
d2= time.strftime ("%B %d, %Y %H:%M")
print('|{}: \n'.format(d2))
data = pd.read_excel(r'/home/mint/Documents/Pyprojekt/EXPORT_Kapatool_Vorgänge.XLSX')
data_frame = pd.DataFrame(data, columns=["Auftrag", "Kurztext Vorgang", "Vorgangsmenge (MEINH)", "Rückmeldung", "Systemstatus", "Arbeitsplatz", "Fr.term.St.dat.Durchf", "Fr.term.Enddat.Durchf", "Vorgabewert 3 (VGE03)", "Rückgemeld. Leist. 3 (ILE03)", "Bearbeitungszeit (BEAZE)", "Dauer Bearbeiten (BEAZE)"])
data = data_frame[["Auftrag", "Arbeitsplatz", "Rückmeldung", "Systemstatus", "Kurztext Vorgang", "Vorgangsmenge (MEINH)", "Fr.term.St.dat.Durchf", "Fr.term.Enddat.Durchf", "Vorgabewert 3 (VGE03)", "Rückgemeld. Leist. 3 (ILE03)"]]
def call_Kapadaten_withauftrag(Auftrag_list, dataframe, param):
    for k in Auftrag_list:
        frame = dataframe.T[[k]].T
        frame["Rest_Bearb_zeit"] = frame["Fr.term.Enddat.Durchf"] - frame["Fr.term.St.dat.Durchf"]
        frame.index = frame.index.astype(int)
        frame["Rückmeldung"] = frame["Rückmeldung"].astype(int)
        if param == False:
            print(f'{frame} \n')
        elif param == True:
            sum_frame = frame
            print(f'{sum_frame} \n')
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
        '-s',
        '--summ',
        action='store_true',
        help="-s, --summ for printing additional IST/SOLL analysis")
args = parser.parse_args()
data = data.set_index("Auftrag")
Input = args.auftrag[0].split(',')
rows = []
for k in Input:
    if k not in data.index:
        print(f'Error -  please check for correct Auftrag number again: {k}')
    else:
        rows.append(k)
Input = rows
if args.summ:
    call_Kapadaten_withauftrag(Input, data, param=True)
    exit(1)
if args.auftrag:
    call_Kapadaten_withauftrag(Input, data, param=False)
else:
    print("Check again for correct Auftrag number resp. project")


