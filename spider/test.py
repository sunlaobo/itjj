import threading
import time
import requests
import checker
import socks
import socket
import qqwry

S = requests.session()


class timer(threading.Thread):  # The timer class is derived from the class threading.Thread
    def __init__(self, num, interval):
        threading.Thread.__init__(self)
        self.thread_num = num
        self.interval = interval
        self.thread_stop = False

    def run(self):  # Overwrite run() method, put what you want the thread do here
        # while not self.thread_stop:
        print 'Thread Object(%d), Time:%s\n' % (self.thread_num, time.ctime())
        r = S.get('http://www.baidu.com/')
        print r.content

        # time.sleep(self.interval)

    def stop(self):
        self.thread_stop = True


exitFlag = 0
class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print "Starting " + self.name
        print_time(self.name, self.counter, 5,self)
        print "Exiting " + self.name

def print_time(threadName, delay, counter,thread):
    while counter:
        if exitFlag:
            thread.exit()
        time.sleep(delay)
        print "%s: %s" % (threadName, time.ctime(time.time()))
        counter -= 1


def test():
    thread1 = timer(1, 1)
    thread2 = timer(2, 2)
    thread1.start()
    thread2.start()
    time.sleep(10)
    thread1.stop()
    thread2.stop()
    return


if __name__ == '__main__':
    # test()
    # thread1 = myThread(1, "Thread-1", 1)
    # thread2 = myThread(2, "Thread-2", 2)

    # thread1.start()
    # thread2.start()

    # type='https'.lower()
    # if 'HTTP'.lower() in type:
    #     print 'true'
    PROXY_LIST = [[0, 10, "42.121.33.160", 809, "", "", 0],
                [1, 0, "42.121.33.160", 8080, "", "", 0],
                [2, 0, "110.176.127.177", 80, "", "", 0],
                [3, 0, "218.92.227.168", 33948, "", "", 0],
                [4, 0, "218.92.227.166", 33925, "", "", 0],
                [5, 0, "218.97.195.38", 81, "", "", 0],
                ]
    PROXY_LIST[0][6] -= 1
    print PROXY_LIST[0][6]
    s=requests.session()
    # s.proxies={
    #     # "http":"42.121.33.160:8080",
    #     # "http":"183.111.169.204:3128",
    #     # 'socks4':'218.92.227.168:33948'
    #     # 'http':'222.88.236.234:80',
    #     # 'https':'120.198.236.10:80',
    #     'https':'socks5://202.38.95.66:1080'
    #     # 'http':'220.248.224.242:8089',
    #     # 'http':'175.1.196.190:80'
    # }
    # checker.checkProxy('socks5','202.38.95.66','1080')
    # def EnableProxy():
    #     socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'128.199.129.179',3128)
    #     socket.socket = socks.socksocket
    # EnableProxy()
    # s.proxies={'http':'175.156.132.212:80'}
    # for i in xrange(2):
    #     try:
    #         r=s.get('http://115.239.136.52/zjisag/getip.jsp',headers = {'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:41.0) Gecko/20100101 Firefox/41.0'})
    #         print r.content
    #     except Exception,e:
    #         print e
    # checker.checkProxy('socks4',yeshi '221.1.215.138','1080')
    qqwry=qqwry.QQWry("qqwry.dat")
    c, a = qqwry.query('115.239.136.52')
    print c,a
