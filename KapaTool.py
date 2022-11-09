#!/bin/env python
import argparse
import pandas as pd
import openpyxl
#import matplotlib.pyplot as plt

# del frame2["volume"]
data = pd.read_excel(r'/home/mint/Documents/Pyprojekt/EXPORT_2022_10_21_ Kapadaten.XLSX')
df = pd.DataFrame(data, columns=["PSP-Element", "Fertigungsauftragsmaterial", "Vorgangsbeschr.1",
        "Arbeitsplatz", "Früh.Start", "Früh.Ende",  
        "KapBearb.-Sollbed. (KEINH)", "KapBearb.-Restbed. (KEINH)" ,
        "KapazitätBezeichnung"]).set_index("Fertigungsauftragsmaterial")
df_1 = pd.DataFrame.head(data).squeeze(axis=0)
print(df_1)

df_2 = pd.DataFrame.head(df[["PSP-Element",
        "Arbeitsplatz", "Früh.Start", "Früh.Ende",
        "KapBearb.-Sollbed. (KEINH)", "KapBearb.-Restbed. (KEINH)"]])
print(df_2)

frame_0 = df.iloc[[0,7]]
print(frame_0)
print(df.iloc[57])
print(df.loc[["F002567481"]])  ## search in the index list
frame_1 =pd.DataFrame.head(df.loc["F004057494"])
print(frame_1)
