#!/bin/env python
# _*_coding:utf-8_*_
import requests
import time
import csv

ip_list = []
datas = {}

class ip_data():
    def __init__(self,geo):
        self.count = 0
        self.upband = 0
        self.downband = 0
        self.ipgeo = geo
    def add_data(self,up,down):
        self.count += 1
        self.upband += up
        self.downband += down


def ipapi(ip):
    r = requests.get('http://ip-api.com/json/{}?lang=zh-CN'.format(ip))
    try:
        apijson = r.json()
        apistr = apijson['country'] + apijson['regionName'] + apijson['city']
    except:
        # print r.text
        apistr = ip

    # ip-api Usage limits
    try:
        if r.headers['x-rl'] == '1':
            time.sleep(int(r.headers['x-ttl']) + 1)
    except:
        time.sleep(1)

    return apistr

# f = open('/rinetd_+1s/rinetd.log','r')
f = open('C:/Users/Administrator/Desktop/rinetd_+1s/rinetd.log','r')
en = f.readlines()

for line in en[0:7] :
    part = line.split()
    if len(part) < 9:
        continue
    ip = part[1]
    upband = part[6]
    downband = part[7]
    if ip not in ip_list:
        ip_list.append(ip)
        datas[ip] = ip_data(ipapi(ip))
    datas[ip].add_data(int(upband),int(downband))

f.close()

outdata = sorted(datas.items(), key=lambda item:item[1].count, reverse = True)

csvfile = open('ceshi.csv', 'wb')
writer = csv.writer(csvfile)
#设置表头
result = ['IP Address', 'Connect Num', 'Up Bandwidth', 'Down Bandwidth', 'IP Geolocation']
writer.writerow(result)

for item in outdata:
    itemdata = item[1]
    try:
        print item[0] + '\t' + str(itemdata.count) + '\t' + str(itemdata.upband) + '\t' + str(itemdata.downband) + '\t' + itemdata.ipgeo
    except:
        print item[0] + '\t' + str(itemdata.count) + '\t' + str(itemdata.upband) + '\t' + str(itemdata.downband)
    
    #将CsvData中的数据写入到csv文件中
    CsvData = [item[0], str(itemdata.count), str(itemdata.upband), str(itemdata.downband), itemdata.ipgeo.encode('gbk')]        
    writer.writerow(CsvData)

csvfile.close()