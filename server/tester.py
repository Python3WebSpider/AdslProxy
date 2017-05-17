import time
import tornado
from tornado.curl_httpclient import CurlAsyncHTTPClient
from tornado.httpclient import HTTPRequest
from server.config import TEST_URL, TEST_CYCLE
from server.db import RedisClient


class Tester():
    def __init__(self):
        self.http_client = CurlAsyncHTTPClient(force_instance=True)
        self.redis = RedisClient()

    def test_proxy(self, response):
        request = response.request
        host = request.proxy_host
        port = request.proxy_port
        proxy = '{host}:{port}'.format(host=host, port=port)
        if response.error:
            print('Request failed', response.error)
            self.redis.remove(proxy)
        else:
            print('Valid Proxy', proxy)

    def verify(self, proxy):

        try:
            (proxy_host, proxy_port) = tuple(proxy.split(':'))
            print('Testing Proxy', proxy)
            request = HTTPRequest(url=TEST_URL, proxy_host=proxy_host, proxy_port=int(proxy_port))
            print(request)
            self.http_client.fetch(request, self.test_proxy)
        except ValueError:
            print('Invalid Proxy', proxy)
            self.redis.remove(proxy)

    def run(self):
        while True:
            proxies = self.redis.all()
            for proxy in proxies:
                self.verify(proxy)
            time.sleep(TEST_CYCLE)

        tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    tester = Tester()
    tester.run()
