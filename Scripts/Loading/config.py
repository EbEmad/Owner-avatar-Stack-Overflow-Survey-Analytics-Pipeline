import os
from sqlalchemy import create_engine

server = os.getenv("DB_SERVER")
destination_database = os.getenv("DESTINATION_DATABASE")

destination_connection_string = f"mssql+pyodbc://{server}/{destination_database}?driver=ODBC+Driver+17+for+SQL+Server"
destination_engine = create_engine(destination_connection_string)