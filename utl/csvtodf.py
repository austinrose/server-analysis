import csv
import pandas as pd

def csvsplit(filename, region):

    if region == 'DFW':
        start_ind = 4
    elif region == 'GTAA':
        start_ind = 6

    # init rows list
    rows = []

    # open CSV file and append each row to a list
    with open(filename, newline='') as csvfile:

        #create CSV reader object and iterate through each row - appending it to the rows list
        csv_obj = csv.reader(csvfile, delimiter=',', quotechar = '|')

        for row in csv_obj:
            rows.append(row)
    
    # find where server data ends and comparison between servers begins and shorten list to that length
    end_index = rows.index(['Differences between servers'])
    search_rows = rows[start_ind: end_index - 1]


    # iterate through each row and create the necessary data frames for each server
    index_list = []
    counter = 0
    for row in search_rows:

        string_row = str(row)

        if 'rows' in string_row:
            index_list.append(counter)

        counter += 1
    
    # remove header rows and section off each servers data
    list2 = search_rows[1:index_list[0]]
    list3 = search_rows[index_list[0] + 3: index_list[1]]
    list4 = search_rows[index_list[1] + 3: index_list[2]]
    list6 = search_rows[index_list[2] + 3: index_list[3]]


    # convert lists into DataFrames
    df2 = pd.DataFrame(list2[1::], columns=list2[0])
    df3 = pd.DataFrame(list3[1::], columns=list3[0])
    df4 = pd.DataFrame(list4[1::], columns=list4[0])
    df6 = pd.DataFrame(list6[1::], columns=list6[0])

    # put all 3 lists in an array and return that array
    df_list = [df2, df3, df4, df6]

    return df_list

