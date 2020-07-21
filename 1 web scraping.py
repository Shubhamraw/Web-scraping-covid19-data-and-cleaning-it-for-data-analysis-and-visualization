import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

def data_downloader():
        
    #testing the url and sending request to grab HTML Data
    url = "https://www.worldometers.info/coronavirus/#countries"
    html_page = requests.get(url).text
    soup = BeautifulSoup(html_page,'lxml')
    
    get_table = soup.find("table",id="main_table_countries_today")
    get_table_data = get_table.tbody.find_all("tr")

    dic = {}

    for i in range(len(get_table_data)):
        try:
            key = get_table_data[i].find_all("a",href =True)[0].string
        except:
            key = get_table_data[i].find_all("td")[0].string

        values =[j.string for j in get_table_data[i].find_all('td')]

        dic[key] = values
        
    column_names = ['Total Cases', 'New Cases', 'Total Deaths', 'New Deaths', 'Total Recovered', 'Active Cases', 'Serious Critical',
                    'Tot Cases/1M pop', 'Deaths/1M pop']

    df = pd.DataFrame(dic).iloc[2:,:].T.iloc[:,:9]

    df.index.name = "Country"
    
    df.columns = column_names

    df.index.values[0]= 'World'
    
    df.to_csv("coronalivetry.csv")
    print("file saved")
    
import os
try:
    os.remove('C:/Users/Shubham Rawat/Python/Covid project/coronalivetry.csv')
except:
    data_downloader()