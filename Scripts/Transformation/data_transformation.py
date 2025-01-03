import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_data(dataframes, cols_to_rename, cols_with_parentheses, exchange_rates):
    logging.info("Starting data processing.")
    df = union_dataframes(dataframes)
    df = rename_columns(df, cols_to_rename) 
    clean_cols_with_parentheses(df, cols_with_parentheses)
    clean_currency(df)
    replace_nulls(df)
    df['YearsCoding'] = df['YearsCoding'].apply(map_years)
    df['YearsCodingProfessionally'] = df['YearsCodingProfessionally'].apply(map_years)
    df.loc[df.DeveloperType == 'Other (please specify):', 'DeveloperType'] = 'Other'
    df.loc[df['Industry'] == 'Other:', 'Industry'] = 'Other'
    df.loc[df.DeveloperType == 'Engineer, data', 'DeveloperType'] = 'Data engineer'
    df = convert_salary_to_usd(df, exchange_rates)
    logging.info("Data processing completed.")
    return df

def union_dataframes(dataframes):
    logging.info("Combining dataframes.")
    return pd.concat(dataframes)

def rename_columns(df, new_col_names):
    logging.info("Renaming columns.")
    return df.rename(columns = new_col_names)

def clean_cols_with_parentheses(df, cols_with_parentheses):
    logging.info(f"Cleaning columns with parentheses")
    for col in cols_with_parentheses:
        df[col] = df[col].str.replace(r'\s*\(.*?\)', '', regex=True)

def clean_currency(df):
    logging.info("Cleaning currency data.")
    df['Currency'] = df['Currency'].str.replace('\t', ' ').str.split(' ').str[0]
    df.loc[(df['Currency'] == 'none') | (df['Currency'] == 'None'), 'Currency'] = np.nan
    df.loc[df['Currency'].isna(), 'CompTotal'] = np.nan

def map_years(years):
    if years == 'No Answer' or years == "Less than 1 year" or years == "More than 50 years":
        return years
    if int(years) <= 4: return "1 to 4 years"
    if int(years) <= 9: return "5 to 9 years"
    if int(years) <= 14: return "10 to 14 years"
    if int(years) <= 19: return "15 to 19 years"
    if int(years) <= 24: return "20 to 24 years"
    if int(years) <= 29: return "25 to 29 years"
    if int(years) <= 34: return "30 to 34 years"
    if int(years) <= 39: return "35 to 39 years"
    if int(years) <= 44: return "40 to 44 years"
    if int(years) <= 49: return "45 to 49 years"

def replace_nulls(df):
    logging.info("Replacing null values.")
    cols_with_empty_vals = df.columns[df.isna().any()]
    for col in cols_with_empty_vals:
        if df[col].dtype == 'object':
            df[col].fillna('No Answer', inplace=True)

def convert_salary_to_usd(df, exchange_rate_df):
    logging.info("Converting salary to USD.")
    df = pd.merge(df, exchange_rate_df, on=['Currency', 'Year'], how='left')
    df['Salary'] = df['CompTotal'] / df['Rate']
    df.drop(['Currency','CompTotal', 'Rate'], axis=1, inplace=True)
    return df

def create_multivalued_table(df, fact_table, column_name, new_column_name, technology_type = None):
    table = df[['ResponseId', 'Year', column_name]]
    table = table.merge(fact_table[['ResponseId', 'Year', 'ResponseKey']], on = ['ResponseId', 'Year'])
    table = table.assign(col=table[column_name].str.split(';'))
    table = table.explode('col')
    table = table.rename(columns = {'col': new_column_name})
    if technology_type:
        table['TechnologyType'] = technology_type
        table = table[['ResponseKey', 'TechnologyType', new_column_name]]
    else:
        table = table[['ResponseKey', new_column_name]]
    table = table.loc[table[new_column_name] != 'No Answer']
    return table