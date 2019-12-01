# server-analysis

Input CSV files go in /tmp directory and are then read, analyzed, and the plots and corresponding excel spreadsheets are moved to the analysis folder sorted by date and region


Main Program Logic:
1) Put some file in the tmp directory with correct format (same as all files)

2) cd into the main folder and run "python3 server_main.py" (server_main.py)

3) Program will first split the CSV file input into 4 DataFrames for each server(/utl/csvtodf.py)

4) All data is then concatenated into a single DataFrame where a unique list of flight tags is found and those are compared against        FlightAware's Data and return a DataFrame of flight tags and Bools whether the diversion notice is true or false (/utl/searchtml.py)

5) Each servers data is then checked against that list and a list of Bools whether the diversion notice is true or false is concatenated to each server's DataFrame (/analytics/servercheck.py)

6) Using these DataFrames, each server's output data is then generated and put into another DataFrame (/analytics/serverstats.py)

7) An excel file is written with the first 3 sheets as the sheets for each server's checked data as well as a final analysis sheet

8) Data is plotted for each region/day (/utl/serverplot.py)

9) Necessary directories are created and all files are moved to appropriate destination

10) Long term average data is caluclated and plotted (/analytics/historicaldata.py & /utl/serverplot.py)