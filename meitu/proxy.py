# encoding=utf8
import random
import urllib2, json


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


@singleton
class ProxyPool:
    def __init__(self):
        self.ip_pool = self._read_ip_cache()
        self.cur = 0
        self.NUM = 100
        self.MAIN_URL = """http://svip.kuaidaili.com/api/getproxy/?orderid=954974497840319&num=%d&b_pcchrome=1&b_pcie=1&b_pcff=1&b_android=1&b_iphone=1&b_ipad=1&carrier=1&protocol=1&method=2&an_an=1&an_ha=1&sp1=1&quality=2&sort=0&format=json&sep=1""" % (
            self.NUM)

    def _read_ip_cache(self):
        ips = []
        try:
            f = open("ip.txt", "r")
            data = f.read()
            f.close()
            ips = json.loads(data)
        except IOError, e:
            print("no ip cache")
            pass
        return ips
        pass

    def _save_ip_cache(self, ips):
        str = json.dumps(ips)
        f = open("ip.txt", "w")
        f.write(str)
        f.close()
        pass

    def _request_proxy_ips(self):
        ips = []
        str = urllib2.urlopen(self.MAIN_URL).read()
        if str:
            obj = json.loads(str)
            code = obj['code']
            if code == 0:
                ips = obj['data']['proxy_list']
                self._save_ip_cache(ips=ips)
        return ips

    def getIp(self):
        ip = "http://10.0.1.1:3128"
        if self.ip_pool:
             if self.cur == (len(self.ip_pool) - 1):
                self.cur = 0
                self.ip_pool = self._request_proxy_ips()
                pass
        else:
            self.ip_pool = self._request_proxy_ips()
            self.cur = 0
            pass

        if self.ip_pool:
            ip = random.choice(self.ip_pool)
            self.cur += 1

        return ip


if __name__ == "__main__":
    for i in range(0, 300):
        print(ProxyPool().getIp())

PROXY = True


# PROXY = False


class ProxyMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        if PROXY:
            request.meta['proxy'] = "http://" + ProxyPool().getIp()

        # Use the following lines if your proxy requires authentication
        # proxy_user_pass = "USERNAME:PASSWORD"

        # setup basic authentication for the proxy
        # encoded_user_pass = base64.encodestring(proxy_user_pass)
        # request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
        pass
