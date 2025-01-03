from Scripts.Loading.config import destination_engine
def load_to_sql(dataframe, table_name, engine = destination_engine):
    dataframe.to_sql(table_name, engine, if_exists = 'append', index = False)