#!/bin/env python
# _*_coding:utf-8_*_
import requests
import time
import csv

import os

sumlines = 0
curlines = 0

class ip_data():
    def __init__(self):
        self.count = 0
        self.upband = 0
        self.downband = 0
        self.ipgeo = ''
    def add_data(self,up,down):
        self.count += 1
        self.upband += up
        self.downband += down
    def set_geo(self,geo):
        self.ipgeo = geo


def ipapi(ipdatas):
    iplist = ipdatas.keys()

    while len(iplist):
        ip100 = []
        for i in range(100):
            if len(iplist) == 0:
                break
            ip100.append(iplist.pop())
        
        # r = requests.get('http://ip-api.com/json/{}?lang=zh-CN'.format(ip))
        r = requests.post('http://ip-api.com/batch?lang=zh-CN', json=ip100)
        try:
            apijson = r.json()
            for apiitem in apijson:
                curip = apiitem['query']
                apistr = apiitem['country'] + apiitem['regionName'] + apiitem['city']
                ipdatas[curip].set_geo(apistr)
        except:
            # print r.text
            continue

        # ip-api Usage limits
        try:
            if r.headers['x-rl'] == '1':
                time.sleep(int(r.headers['x-ttl']) + 1)
        except:
            time.sleep(1)


def main():
    ip_list = []
    datas = {}

    f = open('/rinetd_+1s/rinetd.log','r')
    # f = open('C:/Users/Administrator/Desktop/rinetd_+1s/rinetd.log','r')
    en = f.readlines()
    global sumlines
    global curlines
    sumlines = len(en)
    curlines = 0

    for line in en:
        curlines += 1

        part = line.split()
        if len(part) < 9:
            continue
        ip = part[1]
        upband = part[6]
        downband = part[7]
        if ip not in ip_list:
            ip_list.append(ip)
            datas[ip] = ip_data()
        datas[ip].add_data(int(upband),int(downband))

    f.close()

    ipapi(datas)

    return sorted(datas.items(), key=lambda item:item[1].count, reverse = True)

def csvout(datas):
    csvfile = open('/rinetd_+1s/iplog.csv', 'wb')
    # csvfile = open('iplog.csv', 'wb')
    csvfile.write(u'\ufeff'.encode('utf-8'))
    writer = csv.writer(csvfile)
    #设置表头
    gen_time = time.asctime( time.localtime(time.time()) ) 
    result = ['IP Address', 'Connect Num', 'Up Bandwidth', 'Down Bandwidth', 'IP Geolocation', gen_time]
    writer.writerow(result)
    for item in datas:
        itemdata = item[1]
        #将CsvData中的数据写入到csv文件中
        try:
            CsvData = [item[0], str(itemdata.count), str(itemdata.upband), str(itemdata.downband), itemdata.ipgeo.encode('utf-8')]
        except:
            CsvData = [item[0], str(itemdata.count), str(itemdata.upband), str(itemdata.downband), item[0]]    
        writer.writerow(CsvData)
    csvfile.close()

def printout(datas):
    for item in datas:
        itemdata = item[1]
        try:
            print item[0] + '\t' + str(itemdata.count) + '\t' + str(itemdata.upband) + '\t' + str(itemdata.downband) + '\t' + itemdata.ipgeo
        except:
            print item[0] + '\t' + str(itemdata.count) + '\t' + str(itemdata.upband) + '\t' + str(itemdata.downband)


def reportcur():
    return [curlines, sumlines]



if __name__ == '__main__':
    outdata = main()
    printout(outdata)
    csvout(outdata)