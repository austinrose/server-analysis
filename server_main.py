# import necessary libraries
import pandas as pd
import os
import shutil

# import other functions from files
import utl.csvtodf
import utl.searchtml
import analysis.servercheck
import analysis.serverstats
import utl.serverplot
import analysis.historicaldata

def analysis_main():
    all_servers = ['dev-fused02', 'dev-fused03', 'prod-fused04', 'prod-fused06', 'prod-fused07']

    # import necessary directories and search folders to see which data hasnt been checked yet

    dropbox_path = '/Users/austinrose/Dropbox (PASSUR Aerospace)/A. Rose Files/Projects/diversion-analysis'
    my_path = os.getcwd()
    new_data = my_path + '/tmp'
    filelist = [f for f in os.listdir(new_data) if (os.path.isfile(os.path.join(new_data, f)) and f.endswith(".csv"))]
    historical_path = dropbox_path +'/long-term'

    for file in filelist:
        # print file name that is currently being analyzed
        print(file) #logger

        # get the date and region from filename
        date = file[(file.index('.') - 8):(file.index('.'))] #regex
        region = file[0:(file.index('.') - 8)]

        # get full file path
        filename = new_data + '/' + file

        # create plot path and analysis path as well as plot title
        analysis_path = (region + date + '_Analysis.xlsx')
        plot_path = (region + date + '_Chart.png')
        pickle_path = (region + date + '_df.pkl')
        plot_title = (region + ' ' + date + ' Diversion Analysis')
        plot_data = [plot_path, plot_title]
        
        # read csv file and parse data into separate data frames for each server
        server_raw = utl.csvtodf.csvsplit(filename, region)
        server_df = server_raw[0]
        server_list = server_raw[1]
        name_list = server_raw[2]

        # concatenate all server data into one data frame
        df_all = server_df[0]
        df_all.append(server_df[1])  #.apply
        for i in range(len(server_df)):
                df_all = df_all.append(server_df[i])
        
        # look up all unqiue flights on flightaware and return list of unique fid's concatenated to a list of whether they diverted or not
        found_data = utl.searchtml.htmlfind(df_all)

        # compare servers data to checked data
        df_checked = analysis.servercheck.server_check(found_data, server_df)

        # return analyzed output data in a data frame
        dfout = analysis.serverstats.stats(df_checked, found_data)
        dfout['server'] = server_list

        # write data frame to pickle and save it 
        dfout.to_pickle(pickle_path)

        #create new list of columns for excel output
        out_col = ['Shown Diversions', 'True Diversions', 'False Diversions', 'Missed Diversions', 'Missing On-Time', 'On-Time Accuracy', 'Detection Accuracy', 'Server']

        # write output to analysis file
        writer = pd.ExcelWriter(analysis_path, engine='xlsxwriter')
        for i in range(len(df_checked)):
            df_checked[i].to_excel(writer, sheet_name=name_list[i])
        dfout.to_excel(writer, sheet_name='Analysis', header=out_col)
        writer.save()

        # plot data from the day
        data = [dfout.ot_acc.tolist(), dfout.det_acc.tolist()]
        utl.serverplot.plot(data, plot_data, name_list)

        # check to see where to move data to
        out_dir = dropbox_path 
        #my_path + '/analytics'

        # create variable that is init at False but becomes True once the region directory is made to prevent doing same data twice
        not_done = False

        # if no data from that date has been written yet make a directory for that date
        if date not in os.listdir(out_dir):
            os.mkdir(out_dir +'/' + date)

        # if no data from that region has been written to that date yet - create a new directory for that region
        if region not in os.listdir(out_dir + '/' + date):
            os.mkdir(out_dir +'/' + date + '/' + region)
            not_done = True

        writedir = (out_dir + '/' + date + '/' + region)

        # move all output files to correct location
        if not_done == True:
            shutil.move(filename, writedir + '/' + region + date + '_Original.csv')
            shutil.move(my_path + '/' + analysis_path, writedir + '/' + analysis_path)
            shutil.move(my_path + '/' + plot_path, writedir + '/' + plot_path)
            shutil.move(my_path + '/' + pickle_path, writedir + '/' + pickle_path)
        
        # add data to historical database and plot historical data
        long_plot = analysis.historicaldata.longterm(dropbox_path, region, historical_path)
        utl.serverplot.plot(long_plot[0], [(historical_path + '/' + region.lower() + '/' + region + '_Chart.png'), (region + ' Long Term Analysis')], all_servers)
        utl.serverplot.plot(long_plot[1], [historical_path + '/all/AllData_Chart.png', 'Long Term Server Accuracy'], all_servers)

if __name__ == "__main__":
    analysis_main()


