from bs4 import BeautifulSoup
import urllib.request
import pandas as pd

def search_fa():

        fid = input('Please enter flight ID: ')

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

        # identify when this flight was diverted as identified from test servers
        divert_date = input('Please Enter Divert Date: ')

        if len(divert_date) == 0:
            divert_date = flight_rows.rowtime.unique()[0]

        realdate = divert_date[0:divert_date.index(' ')]

        # extract month day and year from date
        realday = int(realdate[8::])
        realmonth = int(realdate[5:7])
        realyear = int(realdate[0:4])

        # iterate through each of the rows of data found to make sure that it is within one day of our listed diverion time
        # append True if found or False if not found to the output list
        for row in divert_rows:
            testdate = row
            testdate = testdate[0:len(testdate) - 1]

            testday = int(testdate[0:2])
            testmonth = testdate[3:6]
            testyear = int(testdate[7::])

            if testmonth == 'Jan':
                testmonth = 1
            elif testmonth == 'Feb':
                testmonth = 2
            elif testmonth == 'Mar':
                testmonth = 3
            elif testmonth == 'Apr':
                testmonth = 4
            elif testmonth == 'May':
                testmonth = 5
            elif testmonth == 'Jun':
                testmonth = 6
            elif testmonth == 'Jul':
                testmonth = 7
            elif testmonth == 'Aug':
                testmonth = 8
            elif testmonth == 'Sep':
                testmonth = 9
            elif testmonth == 'Oct':
                testmonth = 10
            elif testmonth == 'Nov':
                testmonth = 11
            elif testmonth == 'Dec':
                testmonth = 12


            if testyear == realyear:
                if testmonth == realmonth:
                    if testday == realday:
                        new_val = True
                    elif testday == (realday - 1):
                        new_val = True
                    elif testday == (realday + 1):
                        new_val = True