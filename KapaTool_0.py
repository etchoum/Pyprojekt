#!/bin/env python
import argparse
import pandas as pd
import time
d2= time.strftime ("%B %d, %Y %H:%M")
print('|{}: \n'.format(d2))
data = pd.read_excel(r'/home/mint/Documents/Pyprojekt/EXPORT_2022_10_21_ Kapadaten.XLSX')
data_frame = pd.DataFrame(data, columns=["Auftrag", "PSP-Element", "Fertigungsauftrag Kurztext", "Fertigungsauftragsmaterial", "Vorgangsbeschr.1", "Spät.Start","Spät.Ende",
        "Arbeitsplatz", "Vorgangsmenge (MEINH)", "Früh.Start", "Früh.Ende", "KapBearb.-Sollbed. (KEINH)", "KapBearb.-Restbed. (KEINH)" , "KapazitätBezeichnung"])
data = data_frame[["Auftrag", "Arbeitsplatz", "PSP-Element", "Fertigungsauftrag Kurztext", "Vorgangsmenge (MEINH)",
                "Früh.Start", "Spät.Ende",
                "KapBearb.-Sollbed. (KEINH)", "KapBearb.-Restbed. (KEINH)"]]
def call_Kapadaten_withauftrag(Auftrag_list, dataframe, param):
    for k in Auftrag_list:
        frame = dataframe.T[[k]].T
        frame["Rest_Bearb_zeit"] = frame["Spät.Ende"] - frame["Früh.Start"]
        frame["Kapa__IST_Bedarf"] = frame["KapBearb.-Sollbed. (KEINH)"] - frame["KapBearb.-Restbed. (KEINH)"] 
        frame.index = frame.index.astype(int)
        frame["Arbeitsplatz"] = frame["Arbeitsplatz"].fillna(0).astype(int) 
        if param == False:
            print(f'{frame} \n')
        elif param == True:
            SOLL = frame["KapBearb.-Sollbed. (KEINH)"].sum()
            REST = frame["KapBearb.-Restbed. (KEINH)"].sum()
            IST = SOLL - REST
            sum_frame = frame
            sum_frame["SOLL"] = SOLL
            sum_frame["IST"] = IST
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
    if int(k) not in data.index:
        print(f'Error -  please check for correct Auftrag number again: {k}')
    else:
        rows.append(int(k))
Input = rows
if args.summ:
    call_Kapadaten_withauftrag(Input, data, param=True)
    exit(1)
if args.auftrag:
    call_Kapadaten_withauftrag(Input, data, param=False)
else:
    print("Check again for correct Auftrag number resp. project")
    exit(1)



