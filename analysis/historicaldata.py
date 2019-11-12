import pandas as pd
import os

def longterm(my_path, region, historical_path):

    # open blank pkl from long-term/tmp
    slate = pd.read_pickle(my_path +'/analytics/long-term/tmp/blankdf.pkl')
    slate = slate.drop(columns=['server'])

    # establish path to analysis directory
    done_files = my_path + '/analytics'

    for file in os.listdir(done_files):
        # must change file[0] == 2 condition before year 3000
        if file != 'long-term' and (file[0]) == '2':
            check_path = done_files + '/' + file
            check_list = os.listdir(check_path)

            if region in check_list:
                get_path = check_path + '/' + region
                df_add = pd.read_pickle(get_path + '/' + region + file + '_df.pkl')
                df_add = df_add.drop(columns=['server'])
                slate = slate + df_add
    
    long_data = slate
    
    # identify region and open proper file to add to
    if region == 'DFW':
        filename = historical_path +'/dfw/dfw_long.pkl'
    elif region == 'GTAA':
        filename = historical_path +'/gtaa/gtaa_long.pkl'


    # find new value for on time accuracy and detection accuracy
    otval = 100 * (1 - ((long_data.false + long_data.missot + long_data.missed) / (long_data.true + long_data.missed)))
    otval = round(otval, 2)
    long_data.ot_acc = otval

    detval = 100 * (1 - ((long_data.false + long_data.missed) / (long_data.true + long_data.missed)))
    detval = round(detval, 2)
    long_data.det_acc = detval

    long_data['server'] = ['server2', 'server4', 'server6']

    plot_data = [long_data.ot_acc.tolist(), long_data.det_acc.tolist()]

    long_data.to_pickle(filename)

    # open both long term pkl files and do calculations for both to get overall server accuracy
    all_data = pd.read_pickle(my_path +'/analytics/long-term/tmp/blankdf.pkl')
    dfw_all = pd.read_pickle(my_path +'/analytics/long-term/dfw/dfw_long.pkl')
    gtaa_all = pd.read_pickle(my_path +'/analytics/long-term/gtaa/gtaa_long.pkl')

    # remove server name column
    dfw_all.drop(columns=['server'])
    gtaa_all.drop(columns = ['server'])
    
    # add dfw and gtaa data frames
    all_data = dfw_all + gtaa_all

     # calculate new on time accuracy and detection accuracy
    ot = 100 * (1 - ((all_data.false + all_data.missot + all_data.missed) / (all_data.true + all_data.missed)))
    ot = round(ot, 2)
    all_data.ot_acc = ot

    det = 100 * (1 - ((all_data.false + all_data.missed) / (all_data.true + all_data.missed)))
    det = round(det, 2)
    all_data.det_acc = det

    # add server column back in
    all_data['server'] = ['server2', 'server4', 'server6']

    # get data to plot
    all_plot = [all_data.ot_acc.tolist(), all_data.det_acc.tolist()]

    # write pkl file output
    all_data.to_pickle(my_path + '/analytics/long-term/all/all_data.pkl')


    return [plot_data, all_plot]
