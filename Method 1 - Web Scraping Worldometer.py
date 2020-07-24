from bs4 import BeautifulSoup
import requests
import csv

# url
URL = 'https://www.worldometers.info/coronavirus/'

# use requests to get the html at the URL
source = requests.get(URL).text

# BeautifulSoup object on the html
soup = BeautifulSoup(source,'lxml')

# get the table with all of the countries/stats
table = soup.find('table',id="main_table_countries_today")

# get the table header
table_header = table.find('thead').find_all('th')

# open a csv file to write the results to
with open('results.csv','w',newline='') as f:

    # csv writer object
    writer = csv.writer(f)

    # two lists used to get the header
    # header - the raw data from the header
    # new list - the data after parsing it to remove newlines / other unicode characters
    header = []
    new_list = []

    # get the data from the header and add it to the list
    for th in table_header:
        header.append(th.text)

    # strip the new lines and add it to the new list
    for element in header:
        new_list.append(element.strip())

    # remove all new lines / weird unicode chars
    for i,data in enumerate(new_list):
        new_list[i] = data.replace('\xa0', ' ')
        new_list[i] = data.replace('\n',' ')

    # write the row to the csv
    # header row
    writer.writerow(new_list)

    # go through each row in the table
    for row in table.find_all('tr'):

        # csvRow list used to hold the data in each row
        # empty after the data is written to the csv
        csvRow = []

        # get the data and add it to the list
        for data in row.find_all('td'):
            csvRow.append(data.text)
        
        # remove all \n from the data
        for i in range(len(csvRow)):
            csvRow[i] = csvRow[i].replace('\n','')

        # write the data to the csv
        writer.writerow(csvRow)

# close file
f.close()
