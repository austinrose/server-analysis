import csv
import pandas as pd

def csvsplit(filename, region):
    # init rows list
    rows = []

    # open CSV file and append each row to a list
    with open(filename, newline='') as csvfile:

        #create CSV reader object and iterate through each row - appending it to the rows list
        csv_obj = csv.reader(csvfile, delimiter=',', quotechar = '|')

        for row in csv_obj:
            rows.append(row)
    
    # find where server data ends and comparison between servers begins and shorten list to that length
    end_index = rows.index(['Differences between servers']) - 1

    # iterate through each row and create the necessary data frames for each server
    index_list = []
    counter = 0
    for row in rows:
        string_row = str(row)

        if ('orldc' in string_row) and counter <= end_index:
            index_list.append(counter)

        counter += 1
    
    index_list.append(end_index)
    
    col_names = ['flightid', 'status', 'diversion_time', 'orig_dest', 'asdi_dest', 'origin', 'on_time', 'off_time', 'rowtime']
    default_row = ['NaN', 1, '2019-01-01 00:00:00-00', 'KBOS', 'KBOS', 'KBOS', '2019-01-01 00:00:00-00', '2019-01-01 00:00:00-00', '2019-01-01 00:00:00-00']


    df_list = []
    servers = []
    names = []

    for i in (range(len(index_list) - 1)):

        temp_list = rows[index_list[i]:(index_list[i + 1] - 1)]

        if len(temp_list) == 1:
            temp_list.append(col_names)
            temp_list.append(default_row)
        else:
            temp_list.pop()
        
        name = temp_list[0][0]
        name = name[(name.index('-') + 1):name.index(':')]
        
        name_list = ['dev-fused02', 'dev-fused03', 'prod-fused04', 'prod-fused06', 'prod-fused07']
        server_list = ['server2', 'server3', 'server4', 'server6', 'server7']

        server = server_list[name_list.index(name)]

        df = pd.DataFrame(temp_list[2::], columns=col_names)

        df_list.append(df)
        servers.append(server)
        names.append(name)

    return [df_list, servers, names]

