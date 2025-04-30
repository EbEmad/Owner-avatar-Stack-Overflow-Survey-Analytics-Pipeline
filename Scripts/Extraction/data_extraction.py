import pandas as pd
import logging
import requests
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# functions to load the csv files and make sure the columns are in the right format
def load_csv_file(year, filepath, cols):
    logging.info(f"Loading data for {year} from {filepath}")
    df = pd.read_csv(filepath)
    
    if 'Industry' not in df.columns:
        df['Industry'] = 'Not Available'
    
    df = df[cols]
    df['Year'] = year
    return df


# function to download the data from the url
# and save it to the specified file path
def load_survey_data(url,filepath):

    response = requests.get(url)

    with open(filepath, 'wb') as file:
        file.write(response.content)




# function to save the exchange rates to a CSV file
def save_exchange_rates_csv(rates_usd, file_path):
    with open(file_path, mode='w', encoding='utf-8') as file:
        file.write("Year,Currency,Rate\n")
        
        for year in rates_usd:
            for currency in rates_usd[year]:
                line = f"{year},{currency},{rates_usd[year][currency]}\n"
                file.write(line)



# function to fetch the exchange rates
# for USD from the openexchangerates API
# and save it to a CSV file
def fetch_usd_exchange_rates(appID, dates):
    logging.info(f"Fetching USD exchange rates from openexchangerates API.")
    rates_usd = {}

    for year in dates.keys():
        url = f"https://openexchangerates.org/api/historical/{dates[year]}.json?app_id={appID}&base=USD"
        rates_usd[year] = requests.get(url).json()['rates']
    
    save_exchange_rates_csv(rates_usd, 'Data/external/currency_rates.csv')
    return pd.read_csv('Data/external/currency_rates.csv')



