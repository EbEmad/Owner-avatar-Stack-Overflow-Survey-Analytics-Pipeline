from Scripts.Extraction.config import csv_files, appID, dates, urls,appID,dates
from Scripts.Extraction.data_extraction import load_survey_data ,fetch_usd_exchange_rates


for idx,val in urls.items():
    load_survey_data(val, csv_files[idx])
    print("file downloaded")

fetch_usd_exchange_rates(appID, dates)
print("file downloaded")
