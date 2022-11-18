#!/bin/env python 
import argparse
import pandas as pd
data = pd.read_excel(r'/home/mint/Documents/Pyprojekt/EXPORT_Kapatool_Vorgänge_2022_11_14.XLSX')
data = pd.DataFrame(data, columns=["Auftrag", "Kurztext Vorgang", "Systemstatus", "Vorgangsmenge (MEINH)", "Mengeneinheit Vrg. (=MEINH)", "Fr.term.St.dat.Durchf", "Fr.term.Enddat.Durchf", "Rückgemeld. Leist. 1 (ILE01)", "Vorgabewert 3 (VGE03)", "Rückgemeld. Leist. 3 (ILE03)","Bearbeitungszeit (BEAZE)"])
data = data[["Auftrag", "Kurztext Vorgang", "Systemstatus", "Vorgangsmenge (MEINH)", "Fr.term.St.dat.Durchf", "Fr.term.Enddat.Durchf", "Rückgemeld. Leist. 1 (ILE01)", "Bearbeitungszeit (BEAZE)"]]

data1 = pd.read_excel(r'/home/mint/Documents/Pyprojekt/EXPORT_Kapatool_Auftragskopf_2022_11_14.XLSX')
data1 = pd.DataFrame(data1, columns=["Auftrag", "Kunden Code PSP", "PSP-Element", "Systemstatus"])

def Kapa_with_auftrag(Input, data, p):
    if p == True:
        dic_of_auftrag = {AUFTRAG:[] for AUFTRAG in Input}
        for elment in dic_of_auftrag:
            data = data.T[[elment]].T
            data["SOLL_Bearb_zeit"] = data["Fr.term.Enddat.Durchf"] - data["Fr.term.St.dat.Durchf"]
            data.drop(["Fr.term.Enddat.Durchf", "Fr.term.St.dat.Durchf"], axis = 1, inplace=True)
            auftrag = data.loc[data.index == elment]
            dic_of_auftrag[elment].append(auftrag)
            print(dic_of_auftrag[elment][0])
            print(f'{dic_of_auftrag[elment][0][["Vorgangsmenge (MEINH)", "Rückgemeld. Leist. 1 (ILE01)", "Bearbeitungszeit (BEAZE)", "SOLL_Bearb_zeit"]].sum(axis=0)} \n \n')


def Kapa_with_status(Input, data, p):
    dic = {"ERRÖFNET":[] , "IN_BEARBEITUNG":[] , "FERTIG":[] }
    dic_of_status = {STATUS:[] for STATUS in data.index}
    if p == False:
        for elment in Input:
            status  = data.loc[data.index == elment]
            dic_of_status[elment].append(status)
        for status in Input:
            print(dic_of_status[status][0])
            print(dic_of_status[status][0].sum(axis=0, numeric_only=bool))
    if p == True:
        list_of_states = [str(STATUS) for STATUS in dic_of_status]
        LIST1 = []
        LIST2 = []
        LIST3 = []
        for state in list_of_states:
            if "nan" in state.split(' '):
                pass
            elif "RÜCK" in state.split(' '):
                LIST1.append(str(state))
            elif "EROF" in state.split(' '):
                LIST2.append(str(state))
            else:
                LIST3.append(str(state))
        dic["FERTIG"] = data.T[LIST1].T
        dic["ERRÖFNET"] = data.T[LIST2].T
        dic["IN_BEARBEITUNG"] = data.T[LIST3].T
        print(dic[Input])
        print(dic[str(Input)][["Vorgangsmenge (MEINH)", "Rückgemeld. Leist. 1 (ILE01)", "Bearbeitungszeit (BEAZE)", "SOLL_Bearb_zeit"]].sum(axis=0))



def Kapa_with_psp(Input, data1, p):
    #data = data.set_index("Auftrag")
    if p == True:
        psp_list = data1.loc[data1.index == Input]
        print(psp_list)
    if p == False:
        lst = []
        #dic = {PSP:[] for PSP in data.index and str(Input) in PSP}
        for k in data1.index:
            if str(k).split('-')[0] == Input:
                if k in lst:
                    pass
                else:
                    lst.append(k) 
        print(data1.T[lst].T)
    




parser = argparse.ArgumentParser(prog='Kapa.py', usage='%(prog)s [options]', description='Walltimes based on Auftrag number & IST/SOLL Analysis')
parser.add_argument('-a', '--auftrag', nargs=1, help="-a, or --auftrag for Walltimes based on Auftragnumber")
parser.add_argument('-s', '--status', nargs=1, help="-s, or --status for Walltimes based on status")
parser.add_argument('-p', '--psp', nargs=1, help="-s, or --status for Walltimes baed on PSP-Element")
args = parser.parse_args()
if args.auftrag:
    rows = args.auftrag[0].split(',')
    data = data.set_index("Auftrag")
    for auftrag in rows:
        Input = []
        if auftrag not in data.index:
            print(f'Error -  please check for correct Auftrag number again: {auftrag}')
        else:
            Input.append(auftrag)
            Kapa_with_auftrag(Input, data, p = True)
if args.status:
    Input = args.status[0].split(',')
    data = data.set_index("Systemstatus")
    data["SOLL_Bearb_zeit"] = data["Fr.term.Enddat.Durchf"] - data["Fr.term.St.dat.Durchf"]
    for partition in Input:
        if partition in [STATUS for STATUS in data.index]:
            Kapa_with_status(Input, data, p = False)
        elif partition in ["ERRÖFNET", "IN_BEARBEITUNG", "FERTIG"]:
            Kapa_with_status(str(partition), data, p = True)
if args.psp:
    Input = args.psp[0].split(',')
    data1 = data1.set_index("PSP-Element")
    for Elment in Input:
        if '-' in str(Elment):
            Kapa_with_psp(Elment, data1, p = True)
        else:
            Kapa_with_psp(Elment, data1, p = False)

