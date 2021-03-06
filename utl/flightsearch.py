from bs4 import BeautifulSoup
import urllib.request
import pandas as pd

def search_fa():
 
    fid = input('Please enter flight ID: ')
    date = input('Please enter date (MM-DD-YYYY): ') 

    new_val = False

    # define target url
    url =  "https://flightaware.com/live/flight/" + fid + "/history/160"

    # extract content from webpage and open as soup
    content = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(content, features="html.parser")

    # find table wiith flight history data in it
    table = soup.findAll("table", class_="prettyTable fullWidth tablesaw tablesaw-stack")

    # extract all rows in table and init output list 
    if (len(table) != 0) and (len(table[0]) != 4):
        rows = table[0].find_all("tr")
        outlist = []
        # iterate through each row and concantenate data to output list
        for tr in rows:
            td = tr.find_all('td')
            row = [tr.text for tr in td]
            outlist.append(row)
    else:
        # populate outlist with generic data
        outlist = [['01-Jan-2000 ', 'NaN', 'Ocean Reef Club (07FA)', 'Trenton Mercer (KTTN)', '11:06AM\xa0EST', '01:30PM\xa0EST', 'Scheduled']]

    
    # convert output list to data frame and find flights that are listed as diverted
    # could add other filters to check against flight times or origin/destination pairs as well
    df_out = pd.DataFrame(outlist, columns=['date', 'aircraft', 'origin', 'destination', 'departure', 'arrival', 'duration'])
    divert_rows = df_out[df_out.duration == 'Diverted'].date


    # extract month day and year from date
    realday = int(date[3:5])
    realmonth = int(date[0:2])
    realyear = int(date[6::])

    # iterate through each of the rows of data found to make sure that it is within one day of our listed diverion time
    # append True if found or False if not found to the output list
    for row in divert_rows:
        testdate = row
        testdate = testdate[0:len(testdate) - 1]

        testday = int(testdate[0:2])
        testmonth = testdate[3:6]
        testyear = int(testdate[7::])

        monthnum = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        monthword = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        testmonth = monthnum[monthword.index(testmonth)]

        if testyear == realyear:
            if testmonth == realmonth:
                if testday == realday:
                    new_val = True
                elif testday == (realday - 1):
                    new_val = True
                elif testday == (realday + 1):
                    new_val = True

    if (new_val == True):
        print('Diversion is confirmed True')
        exit()

    if (new_val == False):
        print("No flight listed, please enter origin, original destinaton, and adjusted destination: \n (e.g. 'KBOS, KTTN, KLGA')")
        origin = input('Origin: ')
        dest_orig = input('Original Destination: ')
        dest_new = input('Adjusted Destination: ')

        rows = df_out[df_out.duration != 'Diverted']
        if len(rows) != 0:
            counter = 0

            for index in range(1,len(rows) - 1):
                row = rows.iloc[index]
                # init date check val to see if the date is correct
                dc = False
                date = row.date
                date = date[0:len(date) - 1]
                testday = int(date[0:2])
                testmonth = date[3:6]
                testyear = int(date[7::])
                monthnum = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
                monthword = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                testmonth = monthnum[monthword.index(testmonth)]

                if testyear == realyear:
                    if testmonth == realmonth:
                        if testday == realday:
                            dc = True
                        elif testday == (realday - 1):
                            dc = True
                        elif testday == (realday + 1):
                            dc = True

                if dc == True:
                    test_origin = row.origin
                    test_origin = test_origin[(test_origin.index('(') + 1):test_origin.index(')')]
                    if (origin == test_origin) or (origin == dest_orig):
                        test_dest = row.destination
                        test_dest = test_dest[(test_dest.index('(') + 1):test_dest.index(')')]
                        if (test_dest == dest_orig) or (test_dest == dest_new):
                            counter += 1


                if counter >= 2:
                    new_val = True
                    print('Diversion is confirmed True')
                    exit()
        else:
            print('No diversion confirmation could be found')
    
    if 'it made it here' == 'it made it here':
        print('No diversion confirmation could be found')
        
        

if __name__ == "__main__":
    search_fa()