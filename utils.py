from bs4 import BeautifulSoup
import urllib
import requests
import os
import dbUtil
import pymysql
import time
import random
# import ssl

start_url="https://www.mzitu.com/all/"
projectPath='/Users/ParisCheng/Downloads/pinkdao/'
my_agents=["Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0"
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:60.0) Gecko/20100101 Firefox/60.0'
]

def initial_links(url):
    web_data=requests.get(url)
    soup=BeautifulSoup(web_data.text,'lxml')
    archives=soup.select('body > div.main > div.main-content > div.all > ul.archives > li > p.url > a')
    
     # 打开数据库连接
    db = pymysql.connect("localhost","root","Test123456","pinkdao" )

    for list in archives:
        url = list.get('href')
        # print(url)
        update_totals(url,db)
        # set_list_info(url, db)
    # 关闭数据库连接
    db.close()
    print('finished!!')

def update_totals(url,db):
    time.sleep(random.uniform(1,3))
    web_data=requests.get(url)
    soup=BeautifulSoup(web_data.text,'lxml')
    content=soup.select('body > div.main > div.content')
    links = content[0].select('div.pagenavi > a')
    lastpage = links[len(links)-2]
    path = url.split('/')
    id = path[len(path)-1]
    total = lastpage.select("span")[0].text
    dbUtil.save_total(id,total,db)

def set_list_info(url, db):
    # url='http://www.mzitu.com/69075'
    path = url.split('/')
    id = path[len(path)-1]
    isExists = create_folder(id)
    if not isExists:
        time.sleep(1)
        web_data=requests.get(url)
        soup=BeautifulSoup(web_data.text,'lxml')
        content=soup.select('body > div.main > div.content')
        print(url)
        tag = content[0].select('div.main-meta > span > a')[0].text
        img = content[0].select('div.main-image > p > a > img')[0]
        title = img.get('alt')
        src = img.get('src')

        # 使用 cursor() 方法创建一个游标对象 cursor
        dbUtil.save_mm_info(id, tag, src, title, url, db)

def create_folder(id):
    path= projectPath+id
    isExists = os.path.exists(path)
    if not isExists:
        os.mkdir(path)
    else:
        print(path + ' exists')
    return isExists

# initial_links(start_url)

def get_pics():
    url="https://www.mzitu.com/152846"
    id="152846"
    next="1"
    # 打开数据库连接
    db = pymysql.connect("localhost","root","Test123456","pinkdao" )

    save_pic_info(url,id,next,db)

    # 关闭数据库连接
    db.close()
    print('finished!!')


#获取列表页的详细信息
def save_pic_info(url,id,next,db):
    # url='http://www.mzitu.com/69075'
    url = url+"/"+next
    web_data=requests.get(url)
    soup=BeautifulSoup(web_data.text,'lxml')
    content=soup.select('body > div.main > div.content')
    print(url)
    img = content[0].select('div.main-image > p > a > img')[0]
    title = img.get('alt')
    src = img.get('src')
    path = src.split('/')
    filename = path[len(path)-1]

    dbUtil.save_mm_pic(id, filename, next, db)
    try:
#         :authority: www.mzitu.com
# :method: GET
# :path: /152846/1
# :scheme: https
# accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
# accept-encoding: gzip, deflate, br
# accept-language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7
# cookie: Hm_lvt_dbc355aef238b6c32b43eacbbf161c3c=1545637564; Hm_lpvt_dbc355aef238b6c32b43eacbbf161c3c=1546782974
# upgrade-insecure-requests: 1
        randdom_agent=random.choice(my_agents)
        my_header = {
            "User-Agent": randdom_agent,
            "Authority": "www.mzitu.com",
            "Host": "i.meizitu.net",
            "Method": "GET",
            "Pth": url[21:],
            "Scheme": "https",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-encoding": "gzip, deflate, br",
            "Accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "Referer": "http://www.mzitu.com/",
            "upgrade-insecure-requests": "1",
            "cookie": "Hm_lvt_dbc355aef238b6c32b43eacbbf161c3c=1545637564; Hm_lpvt_dbc355aef238b6c32b43eacbbf161c3c=1546782974"
        }
        # req=urllib.request.Request(url)
        # req.add_header("User-Agent",randdom_agent)
        # req.add_header("authority","www.mzitu.com")
        # req.add_header("method","GET")
        # req.add_header("path",url[21:])
        # req.add_header("scheme","https")
        # req.add_header("accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8")
        # req.add_header("accept-encoding","gzip, deflate, br")
        # req.add_header("accept-language","en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7")
        # req.add_header("cookie","Hm_lvt_dbc355aef238b6c32b43eacbbf161c3c=1545637564; Hm_lpvt_dbc355aef238b6c32b43eacbbf161c3c=1546782974")
        # req.add_header("Referer","www.mzitu.com")
        # req.add_header("GET",url)
        data = requests.get(src, headers=my_header).content
        # data=urllib.request.urlopen(req).read()

        fileName = projectPath+"/"+id+"/"+filename
        fph = open(fileName, "wb")
        fph.write(data)
        fph.flush()
        fph.close()
    except Exception as e:
        print(e)

# ssl._create_default_https_context = ssl._create_unverified_context
get_pics()

