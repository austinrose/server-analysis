import pandas as pd

def server_check(truth_list, df_list):

    # iterate through each server and add a list of whether the value is true or false for that flight
    for server in df_list:

        #init list to add values to
        truelist = []

        # iterate through each flight id in the server
        for fid in server.flightid:
            # get the checked value from the checked data list and append that to the output list
            check = truth_list[truth_list.flightid == fid].divert
            check = check.tolist()[0]
            truelist.append(check)
        
        server['divert'] = truelist

    return df_list


