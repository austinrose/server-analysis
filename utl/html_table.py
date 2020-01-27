from bs4 import BeautifulSoup
import urllib.request
import pandas as pd

def fid2df():
 
    fid = input('Please enter flight ID: ')

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

    return df_out

if __name__ == "__main__":
    fid2df()