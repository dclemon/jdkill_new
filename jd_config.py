import requests
from bs4 import BeautifulSoup
import json
import configparser
import time

def key_value_to_json(str):
    a = str.split('&')
    data_js = {}
    for b in a:
        c = b.split('=')
        data_js[c[0]] = c[1]
    return data_js
def getmidstring(html, start_str, end):
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()


def write_ini(inikey, inivaluse, str, filepath):
    config = configparser.ConfigParser()
    parent_dir = 'D:\数据\SynologyDrive\软件\jd_seckill'
    config.read(parent_dir + "/" + filepath,encoding = 'utf-8')
    convaluse = config.set(inikey, inivaluse, str)
    config.write(open(parent_dir + "/" + filepath, "w"))
    return convaluse


def read_ini(inikey, inivaluse, filepath):
    config = configparser.RawConfigParser()
    parent_dir = 'D:\数据\SynologyDrive\软件\jd_seckill'
    config.read(parent_dir + "\\" + filepath, encoding='utf-8')
    convaluse = config.get(inikey, inivaluse)
    return convaluse


def jd_checklogin(cokstr):
    manual_cookies = {}
    for item in cokstr.split(';'):
        name, value = item.strip().split('=', 1)
        manual_cookies[name] = value
    cookie = manual_cookies
    url = "https://try.jd.com/activity/getActivityList"
    res = requests.get(url)
    html_str = res.text
    besoup = BeautifulSoup(html_str, features='lxml')
    div_str = str(besoup.find_all('div', attrs={'class': "con"}))
    items = BeautifulSoup(div_str, "html.parser")
    a = items.find_all('li')
    b = getmidstring(str(a[1]), 'activity_id="', '"')
    url = 'https://try.jd.com/migrate/getActivityById?id=' + b
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/75.0.3770.142 Safari/537.36',
        'ContentType': 'text/html; charset=utf-8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'try.jd.com',
        'Referer': 'https://try.jd.com/public'
    }
    res = requests.get(url, headers=head, cookies=cookie)
    c = json.loads(res.text)
    d = c['data']['login']
    print("是否登录：" + str(d))
    return d, cookie

def gettime():
    # 获取京东时间，延迟以及抢购时间
    url = 'https://api.m.jd.com/client.action?functionId=queryMaterialProducts&client=wh5'
    r = requests.get(url, timeout=5).json()
    jdtime = r["currentTime2"]
    localtime = int(time.time() * 1000)
    difftime = int(jdtime) - localtime
    return jdtime, difftime