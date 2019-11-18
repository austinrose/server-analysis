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

    # import necessary directories and search folders to see which data hasnt been checked yet

    dropbox_path = '/Users/austinrose/Dropbox (PASSUR Aerospace)/A. Rose Files/Projects/diversion-analysis'
    my_path = os.getcwd()
    new_data = my_path + '/tmp'
    filelist = [f for f in os.listdir(new_data) if (os.path.isfile(os.path.join(new_data, f)) and f.endswith(".csv"))]
    historical_path = my_path +'/analytics/long-term'

    for file in filelist:
        # print file name that is currently being analyzed
        print(file)

        # get the date and region from filename
        date = file[(file.index('.') - 8):(file.index('.'))]
        region = file[0:(file.index('.') - 8)]

        # get full file path
        filename = new_data + '/' + file

        # create plot path and analysis path as well as plot title
        analysis_path = (region + date + '_Analysis.xlsx')
        plot_path = (region + date + '_Chart.png')
        pickle_path = (region + date + '_df.pkl')
        plot_title = (region + ' ' + date + ' Diversion Analysis')
        
        # read csv file and parse data into separate data frames for each server
        server_df = utl.csvtodf.csvsplit(filename, region)

        # concatenate all server data into one data frame
        df_all = server_df[0]
        df_all = df_all.append(server_df[1])
        df_all = df_all.append(server_df[2])

        # look up all unqiue flights on flightaware and return list of unique fid's concatenated to a list of whether they diverted or not
        found_data = utl.searchtml.htmlfind(df_all)

        # compare servers data to checked data
        df_checked = analysis.servercheck.server_check(found_data, server_df)

        # return analyzed output data in a data frame
        dfout = analysis.serverstats.stats(df_checked, found_data)

        # write data frame to pickle and save it 
        dfout.to_pickle(pickle_path)

        #create new list of columns for excel output
        out_col = ['Shown Diversions', 'True Diversions', 'False Diversions', 'Missed Diversions', 'Missing On-Time', 'On-Time Accuracy', 'Detection Accuracy', 'Server']

        # write output to analysis file
        writer = pd.ExcelWriter(analysis_path, engine='xlsxwriter')
        df_checked[0].to_excel(writer, sheet_name='dev-fused-02')
        df_checked[1].to_excel(writer, sheet_name='prod-fused-04')
        df_checked[2].to_excel(writer, sheet_name='prod-fused-06')
        dfout.to_excel(writer, sheet_name='Analysis', header=out_col)
        writer.save()

        # plot data from the day
        data = [dfout.ot_acc.tolist(), dfout.det_acc.tolist()]
        utl.serverplot.plot(data, plot_title, plot_path)

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
        long_plot = analysis.historicaldata.longterm(my_path, region, historical_path)
        utl.serverplot.plot(long_plot[0], (region + ' Long Term Analysis'), (historical_path + '/' + region.lower() + '/' + region + '_Chart.png'))
        utl.serverplot.plot(long_plot[1], 'Long Term Server Accuracy', historical_path + '/all/AllData_Chart.png')

if __name__ == "__main__":
    analysis_main()


