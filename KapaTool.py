#!/bin/env python3.9
import argparse
import pandas as pd
import time
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
def plane():
    details = pd.read_excel(r'/home/mint/Documents/Pyprojekt/EXPORT_Kapatool_Vorgänge_2022_11_14.XLSX')
    details_frame = pd.DataFrame(data, columns=["Auftrag", "Kurztext Vorgang", "Systemstatus", "Vorgangsmenge (MEINH)", "Mengeneinheit Vrg. (=MEINH)", "Fr.term.St.dat.Durchf", "Fr.term.Enddat.Durchf", "Rückgemeld. Leist. 1 (ILE01)",                                                       "Vorgabewert 3 (VGE03)", "Rückgemeld. Leist. 3 (ILE03)", "Bearbeitungszeit (BEAZE)"])
    details = details_frame[["Auftrag", "Kurztext Vorgang", "Systemstatus", "Vorgangsmenge (MEINH)", "Fr.term.St.dat.Durchf", "Fr.term.Enddat.Durchf", "Vorgabewert 3 (VGE03)", "Rückgemeld. Leist. 3 (ILE03)", "Bearbeitungszeit (BEAZE)"]].set_index("Auftrag")
    ABGESCHLOSSEN = []
    IN_BEARBEITUNG = []
    ERRÖFNET = []
    summ_ABG = 0
    summ_IN_BEAR = 0
    summ_ERRÖF = 0
    for k in details:
        if 'TABG' or 'RÜCK' in k["Systemstatus"]:
            ABGESCHLOSSEN.append(k)
            summ_ABG += 1
        elif 'TRÜCK' or 'FREI' in k["Systemstatus"]:
            IN_BEARBEITUNG.append(k)
            summ_IN_BEAR += 1
        elif 'EROF' in k["Systemstatus"]:
            ERRÖFNET.append(k)
            summ_IN_BEAR += 1
#    print(ABGESCHLOSSEN.head())
    print(f'summ_ABG = {summ_ABG}')
#    print(IN_BEARBEITUNG.head())
    print(f'summ_IN_BEAR = {summ_IN_BEAR}')
#    print(ERRÖFNET.head())
    print(f'summ_ERRÖF = {summ_ERRÖF}')
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
if args.auftrag:
    call_Kapadaten_withauftrag(rows, data, param=False)
else: plane()


