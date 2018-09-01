import urllib.request
import urllib.response
import re
import json
import sqlite3
import time
import sys
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import ctypes


def requestData(url):
    html = urllib.request.urlopen(url)
    bytesItem = html.read()
    dataItem = bytesItem.decode("utf8")
    html.close()
    return dataItem

def QueryHcp(date, start, end, purpose_codes):
    reurl = "https://kyfw.12306.cn/otn/leftTicket/queryA?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes={}".format(date, start, end, purpose_codes)
    data = requestData(reurl)
    hcp = json.loads(data)
    results = hcp['data']['result']
    for row in results:
        curlist = (str(row)).split('|')
        if ((str(curlist[3]) in ["k8363","K1048","K8402","K8482", "K8386", "K8366", "K1506"]) & ((curlist[23] != "无") | (curlist[28] != "无"))):
            return curlist

i = 0
while(1!=-1):
    time.sleep(5)
    i = i+1
    print(i)
    data = QueryHcp('2018-09-30', 'SHH', 'FYH', 'ADULT')
    if (data != None):
        print(data[3]+ "|" + data[23] + "|" + data[28])
        i = -1
        ctypes.windll.user32.MessageBoxA(0, (data[3]+ "|" + data[23] + "|" + data[28]).encode('gb2312'),u' 信息'.encode('gb2312'),0)
