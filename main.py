from Scripts.Extraction.config import csv_files, appID, dates,urls
from Scripts.Extraction.data_extraction import load_csv_file, fetch_usd_exchange_rates, load_survey_data

from Scripts.Transformation.config import cols_to_rename, cols_with_parentheses, relevant_cols, dev_cols, technologies
from Scripts.Transformation.data_transformation import union_dataframes, process_data, create_multivalued_table

from Scripts.Loading.data_loading import load_to_sql
import os
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':

    # download the data using the URLs
    for idx, val in urls.items():
        load_survey_data(val, csv_files[idx])
        logging.info(f"File downloaded for {idx}")

    dataframes = [load_csv_file(year, path, relevant_cols) for year, path in csv_files.items()]

    exchange_rates_df = fetch_usd_exchange_rates(appID, dates)

    output_dir = '/app/Data'
    os.makedirs(output_dir, exist_ok=True)


    for i,(year,df) in enumerate(aip(csv_files.keys(),dataframes)):
        output_path=os.path.join(output_dir,f"data_{year}.csv")
        df.to_csv(output_path,index=False)
        logging.info(f"Data for {year} saved to {output_path}")