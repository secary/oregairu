#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Filename :Abukuma.py
@Description : To get Teitokus' KC data from https://myfleet.moe/
@Datatime :2020/12/18 11:44:32
@Author :Secary
@Version :v1.0.3
'''

import pandas as pd 
import bs4
import os                          
import re                               
import urllib.request,urllib.error,urllib.parse     
import xlwt                             
from bs4 import BeautifulSoup
import datetime
from datetime import datetime,date,timedelta


# uids you want
uids = [str(17117461),str(17114528),str(17037441),str(669051),str(17068868)]

# Rules to get the correct data
find_name = re.compile(r'<h1>(.*?)\n')
find_server = re.compile(r'class="label label-default">(.*?)</span')
find_medalnum = re.compile(r'class="label label-danger">(.*?)</span')
find_sign = re.compile(r'<span class="label label-info">\n        (.*?)\n',re.S)
find_honor = re.compile(r'\n          (.*?)\n')
find_lv = re.compile(r'll>(.*?)</small')
find_equip_name = re.compile(r'onclick="return false;">(.*?)\n',re.S)
find_equip_num = re.compile(r'<span class="badge">(.*?)</span>')
find_shipinfo = re.compile(r'>(.*)</td')
find_shipname = re.compile(r'href="aship/(.*?)">(.*?)</a></td>')
find_shipheaders = re.compile(r'<th>(.*?)</th>')
find_enforcedequipments = re.compile(r'<th>(.*?)</th>')
find_equippedships = re.compile(r'">(.*?)<small>(.*?)</small></a></td>')
find_statistics = re.compile(r'<td>(.*?)</td>')

# Main procedure
def main():
    # get&print teitoku's name
    name = getname()

    # get top,ships & etc. info
    top = gettop()
    ships = getshipdata()
    equipments = getequipdata()
    enforcedequipment = getenforcementdata()
    stat = getstatistic()

    # print some infomation
    info = {'server':top[0],'Medal':top[1],'Signature':top[2],'Honor':top[3],'Level':top[4]}
    df_top = pd.DataFrame(info,index=[name])
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    pd.set_option('display.width', 400)
    index = list(stat.keys()) 
    df_stat = pd.DataFrame({'経験値':stat.values()},index=index)
    print(df_top)
    print("-"*70)
    print(df_stat)
    print("-"*70)    
    # save your info locally
    savedata(top,ships,equipments,enforcedequipment,stat,name,)
    print("="*70)   

def geturl(url):        
    head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.3'}    
    request = urllib.request.Request(url,headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reson"):
            print(e.reason)
    return html

def getname():
    url = topURL
    html = geturl(url)
    soup = BeautifulSoup(html,"html.parser")
    tempname = ""
    for item in soup.find_all('div',class_='jumbotron'):
        item = str(item)
        tempname = re.findall(find_name,item)
        name = tempname[0]
    return name

def gettop():
    url = topURL
    html = geturl(url)
    # f = open('%s.html'%uid,'w',encoding='utf-8')
    # f.write(html)
    soup = BeautifulSoup(html,"html.parser")
    top = []
    
    # find sever's name
    for item in soup.find_all('span',class_='label label-default'):
        item = str(item)
        server = re.findall(find_server,item)[0]
        top.append(server)

    # find Kya Medal's num
    for item in soup.find_all('span',class_='label label-danger'):
        item = str(item)
        medalnum = re.findall(find_medalnum,item)[0]
        top.append(medalnum)
        
    # find teitoku's personal sign
    for item in soup.find_all('span',class_='label label-info'):
        item = str(item)
        sign = re.findall(find_sign,item)[0]
        if len(sign) != 0:
            top.append(sign)
        else:
            top.append(" ")

    # find teitoku's honor name
    for item in soup.find_all('span',class_='label label-primary'):
        item = str(item)
        honor = re.findall(find_honor,item)[0]
        top.append(honor)

    # find teitoku's command level
    for item in soup.find_all('div',class_='jumbotron'):
        item = str(item)
        level = re.findall(find_lv,item)[0]
        top.append(level)

    return top

def getshipdata():
    url = shipURL
    html = geturl(url)
    ship = []
    ships = {}
    # f = open('%s.html'%uid,'w',encoding='utf-8')
    # f.write(html)
    soup = BeautifulSoup(html,"html.parser")
    for item in soup.find_all('tr'):
        item = str(item)
        shipinfo = re.findall(find_shipinfo,item)
        ship.append(shipinfo)  
    ship.pop(0)
    # print(len(ships))
    for item in soup.find_all('table',class_='table table-striped table-condensed'):
        item = str(item)
        shipname = re.findall(find_shipname,item)
    # print(len(shipname))
    for i in range(0,len(ship)):
        ship[i].pop(2)
        ship[i].pop(0)
        shipname[i] = list(shipname[i])
        ship[i] = shipname[i] + ship[i]
        ship[i][1],ship[i][2] = ship[i][2],ship[i][1] 
    for item in soup.find_all('thead'):
        item = str(item)
        shipdataheaders = re.findall(find_shipheaders,item)
    ship.insert(0,shipdataheaders)
    return ship

def getequipdata():
    equip = []
    url = equipmentsURL
    html = geturl(url)
    # f = open('equipment.html','w',encoding='utf-8')
    # f.write(html)
    soup = BeautifulSoup(html,"html.parser")
    for item in soup.find_all('ul',class_="list-group"):
        item = str(item)

        # find equipments names
        equip_name = re.findall(find_equip_name,item)
        equip.append(equip_name)

        # find nums of equipments
        equip_num = re.findall(find_equip_num,item)
        equip.append(equip_num)

    return equip

def getenforcementdata():
    enforcedequipment = []
    equipments = []
    equippedships = []

    html = geturl(equipmentsURL)
    soup = BeautifulSoup(html,"html.parser")
    for item in soup.find_all("tbody"):
        item = str(item)
        equipments = re.findall(find_enforcedequipments,item)
    enforcedequipment.append(equipments)
    for item in soup.find_all("td"):
        item = str(item)
        equippedship = re.findall(find_equippedships,item)
        if len(equippedship) != 0:
            equippedships.append(equippedship[0])
        else:
            equippedships.append('')
    enforcedequipment.append(equippedships)
    # print(enforcedequipment)
    return enforcedequipment

def getstatistic():
    statistics = []
    stat = {}
    html = geturl(statisticsURL)
    # f = open('stat.html','w',encoding='utf-8')
    # f.write(html)
    # f.close()
    soup = BeautifulSoup(html,'html.parser')
    for item in soup.find_all('tr'):
        item = str(item)
        statisitc = re.findall(find_statistics,item)
        statistics.append(statisitc)
    statistics.pop(0)
    for i in range(0,len(statistics)):
        stat[statistics[i][0]] = statistics[i][1] 

    return stat

def savedata(top,ships,equipments,enforcedequipment,stat,name):
    book = xlwt.Workbook(encoding='utf-8')

    sheet = book.add_sheet("Info",cell_overwrite_ok=True)
    sheet.write(0,0,name)
    sheet.write(0,1,top[-1])
    for i in range(0,len(top)-1):
        sheet.write(1,i,top[i])
    for i in range(0,4):
        sheet.col(i).width = 256 * 50


    sheet = book.add_sheet("Ships",cell_overwrite_ok=True)
    for i in range(0,len(ships)):
        for j in range(0,len(ships[i])):
            sheet.write(i,j,ships[i][j])
    for i in range(0,len(ships[0])):
        sheet.col(i).width = 256 * 20

    sheet = book.add_sheet('Equipments Totally',cell_overwrite_ok=True)
    sheet.write(0,0,"Equipments")
    sheet.write(0,1,'Num')
    for i in range (0,len(equipments[0])):
        sheet.write(i+1,0,equipments[0][i])
        sheet.write(i+1,1,equipments[1][i])
    for i in range(0,2):
        sheet.col(i).width = 256 * 75

    sheet = book.add_sheet('Enforced Equipments',cell_overwrite_ok=True)
    sheet.write(0,0,'Equipments')
    sheet.write(0,1,'Equipped Ships')
    for i in range(0,len(enforcedequipment[0])):
        sheet.write(i+1,0,enforcedequipment[0][i])
        sheet.write(i+1,1,enforcedequipment[1][i])
    for i in range(0,2):
        sheet.col(i).width = 256 * 50
    
    sheet = book.add_sheet('EXP Statistics',cell_overwrite_ok=True)
    row0 = ['艦種','経験値']
    col0 = list(stat.keys())
    col1 = list(stat.values())
    for i in range (0,len(row0)):
        sheet.write(0,i,row0[i])
    for i in range (0,len(col0)):
        sheet.write(i+1,0,col0[i])
        sheet.write(i+1,1,col1[i])
    for i in range(0,2):
        sheet.col(i).width = 256 * 50    

    book.save('\%s.xls'%name)   
    print("saved")    

if __name__ == "__main__":
    # match uids with urls
    for i in range(0,len(uids)):
        uid = uids[i]
        baseurl = "https://myfleet.moe/user"
        topURL = baseurl + "/%s/top"%uid
        shipURL = baseurl + "/%s/ship"%uid
        equipmentsURL = baseurl + "/%s/slotitem"%uid
        statisticsURL = baseurl + "/%s/statistics"%uid
        
        # run main procedure with uids you want
        main()
