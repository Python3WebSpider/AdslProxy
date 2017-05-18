import time

import tornado
from tornado.curl_httpclient import CurlAsyncHTTPClient
from tornado.httpclient import HTTPRequest

from server.config import *
from server.db import RedisClient


class TestHandler():
    http_client = CurlAsyncHTTPClient(force_instance=True)
    redis = RedisClient()

    def handle_proxy(self, response):
        request = response.request
        host = request.proxy_host
        port = request.proxy_port
        proxy = '{host}:{port}'.format(host=host, port=port)
        if response.error:
            print('Request failed Using', proxy, response.error)
            print('Invalid Proxy', proxy, 'Remove it')
            self.redis.remove(proxy)
        else:
            print('Valid Proxy', proxy)

    def test_proxies(self):
        while True:
            print('Test Proxies')
            proxies = self.redis.all()
            print(proxies)
            for item in proxies:
                self.test_proxy(item)
            time.sleep(TEST_CYCLE)

    def test_proxy(self, item):
        proxy = item.get('proxy')
        name = item.get('name')
        try:
            (proxy_host, proxy_port) = tuple(proxy.split(':'))
            print('Testing Proxy', name, proxy)
            request = HTTPRequest(url=TEST_URL, proxy_host=proxy_host, proxy_port=int(proxy_port))
            self.http_client.fetch(request, self.handle_proxy)
        except ValueError:
            print('Invalid Proxy', proxy)
            self.redis.remove(name)
