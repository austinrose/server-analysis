import pandas as pd

def stats(df_checked, found_data):
    total_true = len(found_data[found_data.divert == True])

    rows = []

    # iterate through each server in the data frame
    for server in df_checked:
        shown = len(server)
        true = len(server[server.divert == True])
        false = shown - true
        unique_true = pd.DataFrame([server.flightid, server.divert]).transpose().drop_duplicates()
        unique_true = len(unique_true[unique_true.divert == True])
        missed = total_true - unique_true
        missot = len(server[server.on_time == ''])

        # include to prevent divide by 0 error
        if true == 0:
            true = 1

        ot_acc = 100 * (1 - ((false + missot + missed) / (true + missed)))
        ot_acc = round(ot_acc, 2)

        det_acc = 100 * (1 - ((false + missed) / (true + missed)))
        det_acc = round(det_acc, 2)

        row = [shown, true, false, missed, missot, ot_acc, det_acc]

        rows.append(row)
    
    dfout = pd.DataFrame(rows)
    dfout.columns = ['shown', 'true', 'false', 'missed', 'missot', 'ot_acc', 'det_acc']
    dfout['server'] = ['server2', 'server4', 'server6']
    
    return dfout

