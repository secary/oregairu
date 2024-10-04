#!/usr/bin/env python
"""
@Filename: kcdb.py
@Description: This is the module of mt's kcdb tool kits, including set connection to mt's kcdb, get data from kcwiki api, import personal kancolle data from clipboard and database importer.
"""


import pandas as pd
import numpy as np
import kcdb
import ast
import time
import os
import json
import requests
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
import socket


current_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
current_time

api_url = {
    'ship': "http://api.kcwiki.moe/ships",
    'ship_stats': "http://api.kcwiki.moe/ships/stats",
    'slotitems': "http://api.kcwiki.moe/slotitems",
    'slotitems_type': "http://api.kcwiki.moe/slotitems/type",
    'slotitems_detail': "http://api.kcwiki.moe/slotitems/detail"
}

# Set the engine of kcdb connection
def engine():
    sql = {
        'user': 'root',
        'password': '1519040104',
        'host': '172.20.43.197',
        'database': 'kancolle'
        }

    kc_engine = create_engine((f"mysql+pymysql://{sql['user']}:{sql['password']}@{sql['host']}/{sql['database']}"))
    return kc_engine

# Get data from api url
def get_api():
    for api in api_url.keys():
        response = requests.get(api_url[api])
    try:
        response = requests.get(api_url[api], timeout=10)
        response.raise_for_status() 
        data = response.json() 
        
        
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")

    df = pd.DataFrame(data)
    df.to_csv(f'rawdata/apidata/{api}.csv', index=True)

    return 'Api data has been successfully saved!'


# Get the data from kancolle.logbook
def get_logbook():
    query = "SELECT * FROM kancolle.`logbook`;"
    df_kc_rawdata = pd.read_sql(query, con=engine())
    return df_kc_rawdata


# Import data from clipboard
def get_clipboard():
    try:
        data_str = pd.read_clipboard(header=None)[0][0]
        data_json = json.loads(data_str)
        df = pd.DataFrame(data_json)

        if 'st' in df.columns:
            df.to_csv(f'rawdata/secary/ships_{current_time}.csv')
        else:
            df.to_csv(f'rawdata/secary/slotitems_{current_time}.csv')

    except json.JSONDecodeError as Decode_err:
        print(f'Error decoding JSON from clipboard: {Decode_err}\nPlease check the contents.' )
    except Exception as e:
        print('An unexpected error occured: ', e)

    return 'The clipboard data has been successfully saved!'


# Import data to kcdb
def db_importer():
    '''
    Read the csv files from kcwiki api.
    The path is "C:/Users/secar/OneDrive/oregairu/yukinoshita/kcdb/rawdata/apidata"
    '''
    df_ship = pd.read_csv('rawdata/apidata/ship.csv')
    df_ship_stats = pd.read_csv('rawdata/apidata/ship_stats.csv')
    df_slotitems = pd.read_csv('rawdata/apidata/slotitems.csv')
    # df_slotitems_type = pd.read_csv('rawdata/apidata/slotitems_type.csv')
    df_slotitems_detail = pd.read_csv('rawdata/apidata/slotitems_detail.csv')
    print('Api raw data successfully read!')

    '''
    Read the ship data and merge the ship stats with ship names through id.
    '''
    df_ship_detail = pd.merge(df_ship, df_ship_stats, on='id', how='right')
    df_ship_detail = df_ship_detail.drop(['Unnamed: 0_x', 'Unnamed: 0_y', 'chinese_name', 'stype_name_chinese'], axis=1)
    # df_ship_detail 
    print("Ships' detail successfully updated!")

    '''
    Read the slotitems data and processing with stats string to dataframe.
    Then merge to a new dataframe with slotitems' id, name, type and stats data
    '''

    df_slotitems_stats = df_slotitems_detail[['id', 'name', 'chinese_name', 'type','stats']]

    df_slotitems_stats = pd.merge(df_slotitems_stats, df_slotitems, on='id', how='left')
    df_slotitems_stats = df_slotitems_stats.drop(['Unnamed: 0', 'type_x', 'use_bull', 'name_y','chinese_name_y','chinese_name_x'], axis=1)
    df_slotitems_stats = df_slotitems_stats.rename(columns={'name_x': 'name', 'type_y': 'type'})

    df_slotitems_stats['stats'] = df_slotitems_stats['stats'].apply(ast.literal_eval)
    stats_df = df_slotitems_stats['stats'].apply(pd.Series)
    df_slotitems_stats = pd.concat([df_slotitems_stats.drop(columns='stats'), stats_df], axis=1)
    # df_slotitems_stats
    print("Slotitems' detail successfully updated!")

    '''
    Put the ship data and slotitems data into kancolle db
    '''
    try:
        df_ship_detail.to_sql('ship_details', con=engine(), if_exists='replace', index=False)
        df_slotitems_stats.to_sql('slotitems_details', con=engine(), if_exists='replace', index=False)
        print('Ships and slotitems data has been successfully imported!')
    
    except OperationalError as e:
    # Handle OperationalError (including TimeoutError)
        print(f"OperationalError occurred: {e.orig}. \nPlease verify your connection details.")
        if "Can't connect to MySQL server" in str(e.orig):
            print("Please check if the MySQL server is running and accessible at the specified address.")

    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")



