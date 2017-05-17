import tornado
from tornado.curl_httpclient import CurlAsyncHTTPClient
from tornado.httpclient import HTTPRequest
from server.config import TEST_URl
from server.db import RedisClient


class Verify():
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
        (proxy_host, proxy_port) = tuple(proxy.split(':'))
        print(proxy_host, proxy_port)
        request = HTTPRequest(url=TEST_URl, proxy_host=proxy_host, proxy_port=int(proxy_port))
        print(request)
        self.http_client.fetch(request, self.test_proxy)

    def run(self):
        while True:
            self.verify('127.0.0.1:9743')




        tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    verify = Verify()
    verify.run()
