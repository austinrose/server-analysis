import pandas as pd
import os

def get_codes():
    path = os.getcwd()
    url_base = 'https://en.wikipedia.org/wiki/List_of_airports_by_IATA_code:_'
    letters = [ 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    col = ['IATA', 'ICAO']
    df = pd.read_html(url_base + 'A')[0]
    df = df.drop(df.columns[2::], axis=1)
    df.columns = col
    
    for letter in letters:
        print(letter)
        df_temp = pd.read_html(url_base + letter)[0]
        df_temp = df_temp.drop(df_temp.columns[2::], axis=1)
        df_temp.columns = col
        df = df.append(df_temp, ignore_index=True)
    
    df.to_pickle(path + '/ICAO_IATA_ref.pkl')

if __name__ == "__main__":
    get_codes()