import time
import pandas as pd
import schedule

confirmed_cases_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
recovered_cases_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
death_cases_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"


def get_n_melt_data(data_url, case_type):
    df = pd.read_csv(data_url)
    melted_df = df.melt(id_vars = ['Province/State', 'Country/Region', 'Lat', 'Long'])
    melted_df.rename(columns={"variable":"Date", "value": case_type}, inplace = True)
    return melted_df

def merge_data(confirmed_df, recovered_df, deaths_df):
    
    final_df   =  [confirmed_df,deaths_df,recovered_df]
    final_df   =  [df.set_index(['Province/State','Country/Region','Lat','Long','Date']) for df in final_df]
    final_df   =  final_df[0].join(final_df[1:])
    final_df  = final_df.reset_index()
    final_df[['Lat','Long','Confirmed','Deaths','Recovered']] = final_df[['Lat','Long','Confirmed','Deaths','Recovered']].apply(pd.to_numeric)
    final_df[['Date']] = final_df[['Date']].apply(pd.to_datetime)
    final_df[["Confirmed","Deaths","Recovered"]] = final_df[["Confirmed","Deaths","Recovered"]].fillna("0").astype(int)
    
    
    return final_df

def fetch_data():
    #fetch and prepare
    
    confirmed_df = get_n_melt_data(confirmed_cases_url, "Confirmed")
    recovered_df = get_n_melt_data(recovered_cases_url, "Recovered")
    deaths_df = get_n_melt_data(death_cases_url, "Deaths")
    print('Merging Data')
    final_df = merge_data(confirmed_df, recovered_df, deaths_df)
    print("preview data")
    print(final_df.tail(5))
    filename = "C:/Users/Shubham Rawat/Python/Covid project/covid19_updated_dataset.csv"
    print("Saving Dataset")
    final_df.to_csv(filename,index=False)
    print('Finished')
    
    with open('C:/Users/Shubham Rawat/Python/Covid project/'+ time.strftime("%Y%m%d-%H%M%S")+".txt", "w") as file:
        file.write("Updated Succesfully on:{}".format(time.strftime("%Y%m%d-%H%M%S")))  

    
# task
schedule.every(5).seconds.do(fetch_data)

while True:
    schedule.run_pending()
    time.sleep(1)
    