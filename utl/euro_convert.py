import pandas as pd

def icao2iata(df_all, code_path):
    code_list = pd.read_pickle(code_path)

    for i in range(len(df_all)):
        row = df_all.iloc[i]
        
        if len(code_list[code_list.ICAO == row.orig_dest].IATA.to_list()) > 0:
            df_all.iloc[i].orig_dest = code_list[code_list.ICAO == row.orig_dest].IATA.to_list()[0]
        if len(code_list[code_list.ICAO == row.asdi_dest].IATA.to_list()) > 0:
            df_all.iloc[i].asdi_dest = code_list[code_list.ICAO == row.asdi_dest].IATA.to_list()[0]
        if len(code_list[code_list.ICAO == row.origin].IATA.to_list()) > 0:
            df_all.iloc[i].origin = code_list[code_list.ICAO == row.origin].IATA.to_list()[0]
    
    return df_all
