#!/usr/bin/env python
'''
@Filename: kcdb_api.py
@Description: This is python file to get kancolle data through kcwiki api urls.
'''

import requests
import pandas as pd

api_url = {
    'ship': "http://api.kcwiki.moe/ships",
    'ship_stats': "http://api.kcwiki.moe/ships/stats",
    'slotitems': "http://api.kcwiki.moe/slotitems",
    'slotitems_type': "http://api.kcwiki.moe/slotitems/type",
    'slotitems_detail': "http://api.kcwiki.moe/slotitems/detail"
}

for api in api_url.keys():
    response = requests.get(api_url[api])
    try:
        response = requests.get(api_url[api], timeout=10)
        response.raise_for_status()  # 如果请求失败，将引发 HTTPError
        data = response.json()  # 解析响应数据
        
        
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