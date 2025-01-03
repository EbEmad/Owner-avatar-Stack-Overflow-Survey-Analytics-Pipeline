from Scripts.Extraction.config import csv_files, appID, dates
from Scripts.Extraction.data_extraction import load_csv_file, fetch_usd_exchange_rates

from Scripts.Transformation.config import cols_to_rename, cols_with_parentheses, relevant_cols, dev_cols, technologies
from Scripts.Transformation.data_transformation import union_dataframes, process_data, create_multivalued_table

from Scripts.Loading.data_loading import load_to_sql

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    dataframes = [load_csv_file(year, path, relevant_cols) for year, path in csv_files.items()]

    exchange_rates_df = fetch_usd_exchange_rates(appID, dates)

    clean_data = process_data(dataframes, cols_to_rename, cols_with_parentheses, exchange_rates_df)
    
    logging.info("Loading Developer dimension")
    clean_data['DeveloperKey'] = clean_data.index + 1
    dev_df = clean_data[['DeveloperKey'] + dev_cols]
    load_to_sql(dev_df, 'Developer')

    logging.info("Loading the Fact Table")
    fact_responses = clean_data[['ResponseId', 'Year', 'DeveloperKey',  'WorkExp', 'Salary']].copy()
    fact_responses['ResponseKey'] = fact_responses.index + 1
    fact_responses = fact_responses.rename(columns={'WorkExp': 'WorkExperience'})
    load_to_sql(fact_responses, 'FactResponses')

    logging.info("Loading Employee Status")
    emp_df = create_multivalued_table(clean_data, fact_responses, 'Employment', 'EmploymentStatusDescription')
    load_to_sql(emp_df, 'ResponseEmploymentStatus')

    logging.info("Loading Technologies")
    tech_dfs = [create_multivalued_table(clean_data, fact_responses, tech,'TechnologyName', tech_type) for tech, tech_type in technologies.items()]
    technologies_df = union_dataframes(tech_dfs).dropna()
    load_to_sql(technologies_df, 'ResponseTechnologies')