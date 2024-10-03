#!/usr/bin/env python
'''
@Filename: kcdb_engine.py
@Description: This is the sql engine to connect to the local wsl server and access to kancolle db.
'''

from sqlalchemy import create_engine 
import pandas as pd
user = 'root'
password = '20107991'
host = '172.20.43.197'
database = 'kancolle'


# Set the engine of connection
def engine():
    return create_engine((f'mysql+pymysql://{user}:{password}@{host}/{database}'))

# Get the data from logbook
def logbook():
    query = "SELECT * FROM kancolle.`logbook`;"
    df_kc_rawdata = pd.read_sql(query, con=engine())
    return df_kc_rawdata




# print(df)