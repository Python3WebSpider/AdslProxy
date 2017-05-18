import json
from urllib.parse import urlencode, parse_qs, urlsplit

import tornado.ioloop
import tornado.web
from tornado.curl_httpclient import CurlAsyncHTTPClient
from tornado.web import RequestHandler, Application
from server.config import *
from server.db import RedisClient
from tornado.httpclient import HTTPRequest


class MainHandler(RequestHandler):
    redis = RedisClient()
    http_client = CurlAsyncHTTPClient(force_instance=True)

    def handle_proxy(self, response):
        request = response.request
        host = request.proxy_host
        port = request.proxy_port
        name = parse_qs(urlsplit(request.url).query).get('name')[0]
        proxy = '{host}:{port}'.format(host=host, port=port)
        if response.error:
            print('Request failed Using', proxy, response.error)
            print('Invalid Proxy', proxy, 'Remove it')
            self.redis.remove(name)
        else:
            print('Valid Proxy', name)

    def test_proxies(self):
        print('Test Proxies')
        items = self.redis.all()
        for item in items:
            self.test_proxy(item)

    def test_proxy(self, item):
        proxy = item.get('proxy')
        name = item.get('name')
        try:
            (proxy_host, proxy_port) = tuple(proxy.split(':'))
            print('Testing Proxy', name, proxy)
            test_url = TEST_URL + '?' + urlencode({'name': name})
            request = HTTPRequest(url=test_url, proxy_host=proxy_host, proxy_port=int(proxy_port))
            self.http_client.fetch(request, self.handle_proxy)
        except ValueError:
            print('Invalid Proxy', proxy)
            self.redis.remove(name)

    def post(self):
        token = self.get_body_argument('token', default=None, strip=False)
        port = self.get_body_argument('port', default=None, strip=False)
        name = self.get_body_argument('name', default=None, strip=False)
        if token == TOKEN and port:
            ip = self.request.remote_ip
            proxy = ip + ':' + port
            print('Receive proxy', proxy)
            self.redis.set(name, proxy)
            self.test_proxies()
        elif token != TOKEN:
            self.write('Wrong Token')
        elif not port:
            self.write('No Client Port')

    def get(self, api):
        if api == 'first':
            result = self.redis.first()
            if result:
                self.write(result)

        if api == 'random':
            result = self.redis.random()
            if result:
                self.write(result)

        if api == 'list':
            result = self.redis.list()
            print(result)
            if result:
                for proxy in result:
                    self.write(proxy + '<br>')

        if api == 'count':
            self.write(str(self.redis.count()))


def run():
    application = Application([
        (r'/', MainHandler),
        (r'/(.*)', MainHandler),
    ])
    print('Listening on', RECEIVER_PORT)
    application.listen(RECEIVER_PORT)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    run()
