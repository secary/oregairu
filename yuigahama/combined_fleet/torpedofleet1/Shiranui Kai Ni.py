#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Filename :Amakaze ai Ni
@Description :This is a Web Crawler to get Exchange Rate data from CNY to AUD
@Datatime :2024/06/13
@Author :Secary
@Version :v1.0
'''

import bs4                              
import re                               
import urllib.request,urllib.error,urllib.parse                            #
from bs4 import BeautifulSoup
import datetime
import time
from datetime import datetime,date,timedelta

website = "https://www.boc.cn/sourcedb/whpj/"

def askurl(url):
    head = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
    }
    request = urllib.request.Request(url,headers=head)
    html = ""
    try:
        # time.sleep(5)
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reson"):
            print(e.reason)
    return html

def askurl(url):
    head = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
    }
    request = urllib.request.Request(url,headers=head)
    html = ""
    try:
        # time.sleep(5)
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reson"):
            print(e.reason)
    return html

def getexchange_rate(url):
    html = askurl(url)
    soup = BeautifulSoup(html,"html.parser")
    target_td = soup.find('td', text='美元')
    if target_td:
        next_td = target_td.find_next_sibling('td')
        if next_td:
            result = float(next_td.text.strip())
        else:
            result = "未找到相邻的<td>标签"
    else:
        result = "未找到包含'美元'的<td>标签"
        
    return result

def main(url):
    cny_usd = getexchange_rate(url)
    if type(cny_usd) == float:
        CurrentTime = time.strftime('%Y-%m-%d %H:%m:%S', time.localtime(time.time()))
        print("%s\nToday's Exchange Rate of CNY to USD is %s "%(CurrentTime,cny_usd))
        Exchange_rate = float(cny_usd)
        while 1:
            currency = input("enter your currency(press Q to esc):")
            
            if currency == "usd" or currency == "cny":
               
                while 1:
                    amount = input(f"{currency} amount:") 
                    if amount.isnumeric() == False:
                        break
                    else:
                        if currency == "usd":
                            cny = float(amount) * 100 / Exchange_rate 
                            print(f"usd:{amount}\ncny:{cny}\n" + "=" * 60)
                        if currency == "cny":
                            usd = float(amount) * 100 / Exchange_rate 
                            print(f"cny:{amount}\nusd:{usd}\n" + "=" * 60)   
                    
            
    else:
       print("抓取汇率失败，原因：" +  cny_usd)


if __name__ == "__main__":
    main(website)