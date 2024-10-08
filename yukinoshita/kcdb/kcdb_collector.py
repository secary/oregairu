#!/usr/bin/env python
"""
@Filename: kcdb.py
@Description: This is the module of mt's kcdb tool kits, including set connection to mt's kcdb, get data from kcwiki api, import personal kancolle data from clipboard and database importer.
"""

import pandas as pd
import json
import requests
from io import StringIO
import os

ships_api = "http://api.kcwiki.moe/ships/detail"
slots_url = 'https://wikiwiki.jp/kancolle/%E8%A3%85%E5%82%99%E4%B8%80%E8%A6%A7%28%E7%A8%AE%E9%A1%9E%E5%88%A5%29/%E3%83%86%E3%83%BC%E3%83%96%E3%83%AB'

# Get data from api url
def get_api(url) -> pd.DataFrame :
    response = requests.get(url)
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status() 
        data = response.json() 
        df = pd.DataFrame(data)
        return df
        
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")


# Get data from clipboard
def get_clipboard() -> pd.DataFrame:
    try:
        data_str = pd.read_clipboard(header=None)[0][0]
        data_json = json.loads(data_str)
        df = pd.DataFrame(data_json)
        return df

    except json.JSONDecodeError as Decode_err:
        print(f'Error decoding JSON from clipboard: {Decode_err}\nPlease check the contents.' )
    except Exception as e:
        print('An unexpected error occured: ', e)


# Get data from url tables:
def get_url(url) -> pd.DataFrame:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        tables = pd.read_html(StringIO(response.text))
        df = tables[0]  

        return df

    except requests.exceptions.RequestException as req_err:
        print(f"Request Failure: {req_err}")
    except ValueError as val_err:
        print(f"Failed to parse HTML: {val_err}")
    except Exception as e:
        print(f"Unexpected error: {e}")



def ships() -> pd.DataFrame:
    try:   
        # Get raw ships data from api
        df_ships_details = get_api(ships_api)
        # Expand the stats series to seperate series
        stats = df_ships_details['stats'].apply(pd.Series)
        df_ships_details = pd.concat([df_ships_details, stats], axis=1).drop(columns=['stats'])

    except Exception as e:
        print('Unexpected error in processing ships details: ', e)

    return df_ships_details

def slots() -> pd.DataFrame:
    try:
        # Get raw slots data from wiki url
        df_slots_details = get_url(slots_url)
        # Taming slots data
        df_slots_details = df_slots_details[df_slots_details['No.'] != 'No.']
        df_slots_details = df_slots_details.apply(lambda col: col.map(lambda x: x.replace('+', '') if isinstance(x, str) else x))
        df_slots_details = df_slots_details.apply(lambda col: col.map(lambda x: x.replace('-', '0') if isinstance(x, str) else x))
        df_slots_details = df_slots_details.apply(lambda col: col.map(lambda x: x.replace('＋', '+') if isinstance(x, str) else x))
        df_slots_details = df_slots_details.apply(lambda col: col.map(lambda x: x.replace('／', '/') if isinstance(x, str) else x))
        df_slots_details = df_slots_details.drop([col for col in df_slots_details.columns if '装備可能艦種' in col], axis=1)
        df_slots_details.columns = ['id', 'rare', 'name', 'type', 'houg', 'raig', 'baku', 'tyku', 'tais', 'saku', 'houm', 'houk', 'souk', 'leng', 'comments']
        df_slots_details['id'] = df_slots_details['id'].astype('int64')

    except Exception as e:
        print('Unexpected error in processing slots details: ', e)

    return df_slots_details

def main():
    # Export to csv
    try:
        os.makedirs('data/rawdata', exist_ok=True)
    except Exception as e:
        print('Unexpected error in creating path: ', e)

    ships().to_csv('data/rawdata/ships_details.csv', index=False)
    slots().to_csv('data/rawdata/slots_details.csv', index=False)

    try: 
        df = get_clipboard()
        if 'st' in df.columns:
            df.to_csv('data/rawdata/user_ships.csv')
        else:
            df.to_csv('data/rawdata/user_slots.csv')
    except Exception:
        pass


if __name__ == "__main__":
    main()
