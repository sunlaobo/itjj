#-*- coding: UTF-8 -*-
import re
import MySQLdb as mdb
import requests
from threading import Thread
import sys
import datetime
import socks
import socket
import checker

# reload(sys)
# sys.setdefaultencoding('utf8')

DB_HOST = '127.0.0.1'
DB_USER = 'root'
DB_PASS = ''

VIDEO_TYPE = {'动作': 'ddc2', '灵异': 'ddc5', '科幻': 'dko1', '罪案': 'ddc6', '情景': 'ddc3', '律政': 'heme', '真人秀': 'season'}

class Cn163_Video(Thread):  # Thread base class
    def __init__(self, url):
        Thread.__init__(self)
        # self.setDaemon(True)
        self.dbconn = mdb.connect(DB_HOST, DB_USER, DB_PASS, 'itjj', charset='utf8')
        self.dbconn.autocommit(False)
        self.dbcurr = self.dbconn.cursor()
        self.dbcurr.execute('SET NAMES utf8')
        self.url = url
        self.s = requests.Session()

    def run(self):
        try:
            # r=self.s.get('http://cn163.net/ddc1/ddc2/page/2/')
            print self.url
            r=self.s.get(self.url)
        except Exception,e:
            print self.url,e
        # self.getVideo()

        # print ''

    def getVideo(self):
        find_re = re.compile(
            #     r'<tr>.+?\(.+?">(.+?)</a>.+?class="detLink".+?">(.+?)</a>.+?<a href="(magnet:.+?)" .+?已上传 <b>(.+?)</b>, 大小 (.+?),',
            r'',
            re.DOTALL)
        r=self.s.get('http://cn163.net/ddc1/ddc2/page/2/')
        type = sys.getfilesystemencoding()   # 关键
        print type
        print r.content.decode(r.apparent_encoding).encode(type)  # 关键

DB_HOST = '127.0.0.1'
DB_USER = 'root'
DB_PASS = ''
class ProxyGet(Thread):
    def __init__(self,baseurl,start,end,find_re):
        Thread.__init__(self)
        self.bu=baseurl
        self.st=start
        self.ed=end
        self.find_re=find_re
        self.s = requests.Session()
        # self.type=type


    def getType(self,type):
        if(type.lower().startswith('http')):
            return socks.PROXY_TYPE_HTTP
        elif(type.lower().startswith('socks5')):
            return socks.PROXY_TYPE_SOCKS5
        elif(type.lower().startswith('socks4')):
            return socks.PROXY_TYPE_SOCKS4
        else:
            return socks.PROXY_TYPE_SOCKS5


    def run(self):
        dbconn = mdb.connect(DB_HOST, DB_USER, DB_PASS, 'itjj', charset='utf8')
        dbcurr = dbconn.cursor()
        dbcurr.execute('SET NAMES utf8')
        dbcurr.execute('set global wait_timeout=60000')
        global cks
        cks=self.s.cookies
        for i in xrange(self.st,self.ed):
            url=self.bu
            if(i>1):
                url=self.bu+i.__str__()
            print url
            self.s.cookies=cks
            r=self.s.get(url
                         ,headers = {'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:41.0) Gecko/20100101 Firefox/41.0'}
                         )
            cks=self.s.cookies
            # print r.content.decode(r.apparent_encoding).encode(sys.getfilesystemencoding())
            html=r.content
            for x in self.find_re.findall(html):
                print x
                values = dict(
                    country=x[0],
                    ip=x[1],
                    port=x[2],
                    location=x[3],
                    anonymous=x[4],
                    type=x[5],
                    speed=x[6],
                    conntime=x[7],
                    catchtime=x[8]
                             )
                bol=checkProxy(self.getType(values['type']),values['ip'],int(values['port']))
                if(bol):
                    print values['ip']+':'+values['port']
                    #insert db
                    #check if item exists
                    try:
                        sql='select * from web_proxy where ip=%s and port=%s'
                        dbcurr.execute(sql,(values['ip'],int(values['port'])))
                        d = dbcurr.fetchall()
                        # print d
                        # print len(d)
                        if(len(d)<1):
                            sql='INSERT INTO web_proxy(ip, port, type,create_time) VALUES(%s,%s,%s,%s)'
                            dbcurr.execute(sql, (values['ip'],int(values['port']),values['type'],datetime.datetime.now()))
                    except Exception as ex:
                        print "E2", str(ex)
                        continue
                    dbconn.commit()
        dbconn.close()
        dbcurr.close()


def checkProxy(type,ip, port):
    session=requests.Session()

    # session.proxies = {
    #       "http": "http://"+ip+":"+port.__str__()
    # }
    if(socks.PROXY_TYPE_HTTP==type):
        session.proxies={"http":ip+":"+str(port)}
    else:
        socks.setdefaultproxy(type,ip,port)
        socket.socket = socks.socksocket
    try:
        starttime = datetime.datetime.now()
        testProxy = session.get('http://115.239.136.52/zjisag/getip.jsp',timeout=10)
        # print testProxy.content
        endtime = datetime.datetime.now()
        # print endtime-starttime
        return True
    except Exception ,e:
        print e
        return False
    finally:
        session.close()

def auth():
    pass

if __name__ == '__main__':
    # url_base = 'http://cn163.net/ddc1/'
    # Cn163_Video('').start()
    # for key in VIDEO_TYPE:
    #     u = url_base + VIDEO_TYPE[key]
    #     Cn163_Video(u).start()
    # s = requests.Session()

    find_re=re.compile(
            #     r'<tr>.+?\(.+?">(.+?)</a>.+?class="detLink".+?">(.+?)</a>.+?<a href="(magnet:.+?)" .+?已上传 <b>(.+?)</b>, 大小 (.+?),',
            r'<tr.+?>.+?<td><img.+?alt="(.+?)".+?<td>(\d+.\d+.\d+.\d+)</td>.+?<td>(\d+)</td>.+?<td>\s*(.+?)\s*</td>'
            r'.+?<td>\s*(.+?)\s*</td>.+?<td>\s*(.+?)\s*</td>.+?title="(.+?)".+?title="(.+?)".+?<td>(\d{2}-\d{2}-\d{2}\s+\d{2}:\d{2})</td>.+?</tr>',re.DOTALL)
    wn=ProxyGet("http://www.xicidaili.com/wn/",1,10,find_re)
    wn.start()

    # ProxyGet("http://www.xicidaili.com/nn/",1,10,find_re).start()
    # s=requests.Session()

    # ProxyGet("http://www.xicidaili.com/qq/",1,10,find_re).start()
    # s=requests.Session()
    # r=s.get('http://www.google.com',timeout=0.1)
    # print r.text

# print 'Done!'
