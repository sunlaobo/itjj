#coding: utf8
# http://git.oschina.net/ragnaroks/ZhaGanSharp
import sys;
import random;
import time;
reload(sys)

sys.setdefaultencoding('utf8')

import re
import urllib2
import time
import logging
#from tornado import ioloop
#from tornado.httpclient import AsyncHTTPClient, HTTPRequest
#from tornado.httputil import url_concat
from Queue import Queue
import threading, errno, datetime
import json
import requests
import MySQLdb as mdb

DB_HOST = '127.0.0.1'
DB_USER = 'root'
DB_PASS = ''


re_start = re.compile(ur'start=(\d+)')
# re_uid = re.compile(ur'query_uk=(.*?)&')
re_uid = re.compile(ur'query_uk=(\d+)')
re_pptt = re.compile(ur'&pptt=(\d+)')
re_urlid = re.compile(ur'&urlid=(\d+)')

ONEPAGE = 24
ONESHAREPAGE = 24

URL_SHARE = 'http://yun.baidu.com/pcloud/feed/getsharelist?auth_type=1&start={start}&limit=24&query_uk={uk}&urlid={id}'
URL_FOLLOW = 'http://yun.baidu.com/pcloud/friend/getfollowlist?query_uk={uk}&limit=24&start={start}&urlid={id}'
URL_FANS = 'http://yun.baidu.com/pcloud/friend/getfanslist?query_uk={uk}&limit=24&start={start}&urlid={id}'

QNUM = 1000
hc_q = Queue(24)
hc_r = Queue(QNUM)

success = 0
failed = 0

logger = logging.getLogger()
#set loghandler
file = logging.FileHandler("bdy.log")
logger.addHandler(file)
#set formater
#formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
file.setFormatter(formatter)
#set log level
logger.setLevel(logging.NOTSET)

PROXY_LIST = [[0, 10, "42.121.33.160", 809, "", "", 0],
                [1, 0, "42.121.33.160", 8080, "", "", 0],
                [2, 0, "110.176.127.177", 80, "", "", 0],
                [3, 0, "218.92.227.168", 33948, "", "", 0],
                [4, 0, "218.92.227.166", 33925, "", "", 0],
                [5, 0, "218.97.195.38", 81, "", "", 0],
                ]


def req_worker(inx):
    s = requests.Session()
    while True:
        req_item = hc_q.get()
        
        req_type = req_item[0]
        url = req_item[1]
        r = s.get(url)
        # print url
        if r.text.find('"errno":0')==-1:
            print url
            print "url result:",r.text
        hc_r.put((r.text, url.decode('utf8')))
        #{"errno":-55,"request_id":"184063151348304054"}  happens we need proxy!
        # print "req_worker#", inx, url.decode('utf8')
        time.sleep(0.001*random.randint(0, 1000))
def response_worker():
    dbconn = mdb.connect(DB_HOST, DB_USER, DB_PASS, 'baiduyun', charset='utf8')
    dbcurr = dbconn.cursor()
    dbcurr.execute('SET NAMES utf8')
    dbcurr.execute('set global wait_timeout=60000')
    while True:
        
        metadata, effective_url = hc_r.get()
        #print "response_worker:", effective_url
        try:
            tnow = int(time.time())
            id = re_urlid.findall(effective_url)[0]
            start = re_start.findall(effective_url)[0]
            if True:
                if 'getfollowlist' in effective_url: #type = 1
                    follows = json.loads(metadata)
                    uid = re_uid.findall(effective_url)[0]
                    if "total_count" in follows.keys() and follows["total_count"]>0 and str(start) == "0":
                        for i in range((follows["total_count"]-1)/ONEPAGE):
                            try:
                                dbcurr.execute('INSERT INTO urlids(uk, start, limited, type, status) VALUES(%s, %s, %s, 1, 0)' % (uid, str(ONEPAGE*(i+1)), str(ONEPAGE)))
                            except Exception as ex:
                                print "E1", str(ex)
                                pass
                    
                    if "follow_list" in follows.keys():
                        for item in follows["follow_list"]:
                            try:
                                dbcurr.execute('INSERT INTO user(userid, username, files, status, downloaded, lastaccess) VALUES(%s, "%s", 0, 0, 0, %s)' % (item['follow_uk'], item['follow_uname'], str(tnow)))
                            except Exception as ex:
                                print "E13", str(ex)
                                pass
                    else:
                        # print "delete 1", uid, start
                        dbcurr.execute('delete from urlids where uk="%s" and type=1 and start>%s' % (uid, start))
                elif 'getfanslist' in effective_url: #type = 2
                    fans = json.loads(metadata)
                    uid = re_uid.findall(effective_url)[0]
                    if "total_count" in fans.keys() and fans["total_count"]>0 and str(start) == "0":
                        for i in range((fans["total_count"]-1)/ONEPAGE):
                            try:
                                dbcurr.execute('INSERT INTO urlids(uk, start, limited, type, status) VALUES(%s, %s, %s, 2, 0)' % (uid, str(ONEPAGE*(i+1)), str(ONEPAGE)))
                            except Exception as ex:
                                print "E2", str(ex)
                                pass
                    
                    if "fans_list" in fans.keys():
                        for item in fans["fans_list"]:
                            try:
                                dbcurr.execute('INSERT INTO user(userid, username, files, status, downloaded, lastaccess) VALUES(%s, "%s", 0, 0, 0, %s)' % (item['fans_uk'], item['fans_uname'], str(tnow)))
                            except Exception as ex:
                                print "E23", str(ex)
                                pass
                    else:
                        print "delete 2", uid, start
                        dbcurr.execute('delete from urlids where uk="%s" and type=2 and start>%s' % (uid, start))
                else:
                    shares = json.loads(metadata)
                    uid = re_uid.findall(effective_url)[0]
                    if "total_count" in shares.keys() and shares["total_count"]>0 and str(start) == "0":
                        for i in range((shares["total_count"]-1)/ONESHAREPAGE):
                            try:
                                dbcurr.execute('INSERT INTO urlids(uk, start, limited, type, status) VALUES(%s, %s, %s, 0, 0)' % (uid, str(ONESHAREPAGE*(i+1)), str(ONESHAREPAGE)))
                            except Exception as ex:
                                print "E3", str(ex)
                                pass
                    if "records" in shares.keys():
                        for item in shares["records"]:
                            try:
                                dbcurr.execute('INSERT INTO share(userid, filename, shareid, status) VALUES(%s, "%s", %s, 0)' % (uid, item['title'], item['shareid']))
                            except Exception as ex:
                                print "E33", str(ex), item
                                pass
                    else:
                        print "delete 0", uid, start
                        dbcurr.execute('delete from urlids where uk="%s" and type=0 and start>%s' % (uid, str(start)))
                dbcurr.execute('delete from urlids where id=%s' % (id, ))
                dbconn.commit()
        except Exception as ex:
            print "E5", str(ex), id

        
        pid = re_pptt.findall(effective_url)
        
        if pid:
            print "pid>>>", pid
            ppid = int(pid[0])
            PROXY_LIST[ppid][6] -= 1
    dbcurr.close()
    dbconn.close()
    
def start():
    global success, failed
    dbconn = mdb.connect(DB_HOST, DB_USER, DB_PASS, 'baiduyun', charset='utf8')
    dbcurr = dbconn.cursor()
    dbcurr.execute('SET NAMES utf8')
    dbcurr.execute('set global wait_timeout=60000')
    while True:

        dbcurr.execute('select * from urlids where status=0 order by type limit 1')
        # dbcurr.execute('select * from urlids where status=0 and type>0 limit 1')
        d = dbcurr.fetchall()
        # print d
        if d:
            id = d[0][0]
            uk = d[0][1]
            start = d[0][2]
            limit = d[0][3]
            type = d[0][4]
            dbcurr.execute('update urlids set status=1 where id=%s' % (str(id),))
            url = ""
            if type == 0:
                url = URL_SHARE.format(uk=uk, start=start, id=id).encode('utf-8')
            elif  type == 1:
                url = URL_FOLLOW.format(uk=uk, start=start, id=id).encode('utf-8')
            elif type == 2:
                url = URL_FANS.format(uk=uk, start=start, id=id).encode('utf-8')
            if url:
                hc_q.put((type, url))#put hc_q
                
            #print "processed", url
        else:
            dbcurr.execute('select * from user where status=0 limit 1000')
            d = dbcurr.fetchall()
            if d:
                for item in d:
                    try:
                        dbcurr.execute('insert into urlids(uk, start, limited, type, status) values("%s", 0, %s, 0, 0)' % (item[1], str(ONESHAREPAGE)))
                        dbcurr.execute('insert into urlids(uk, start, limited, type, status) values("%s", 0, %s, 1, 0)' % (item[1], str(ONEPAGE)))
                        dbcurr.execute('insert into urlids(uk, start, limited, type, status) values("%s", 0, %s, 2, 0)' % (item[1], str(ONEPAGE)))
                        dbcurr.execute('update user set status=1 where userid="%s"' % (item[1],))
                    except Exception as ex:
                        print "E6", str(ex)
            else:
                time.sleep(1)
                
        dbconn.commit()
    dbcurr.close()
    dbconn.close()
        

for item in range(1):
    t = threading.Thread(target = req_worker, args = (item,))
    t.setDaemon(True)
    t.start()

s = threading.Thread(target = start, args = ())
s.setDaemon(True)
s.start()

response_worker()
