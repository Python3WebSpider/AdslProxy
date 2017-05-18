import time
import tornado.ioloop
import tornado.web
from multiprocessing import Process
from tornado.web import RequestHandler, Application
from server.config import *
from server.db import RedisClient
from server.tester import TestHandler


class MainHandler(RequestHandler):
    redis = RedisClient()

    def post(self):
        token = self.get_body_argument('token', default=None, strip=False)
        port = self.get_body_argument('port', default=None, strip=False)
        name = self.get_body_argument('name', default=None, strip=False)
        if token == TOKEN and port:
            ip = self.request.remote_ip
            proxy = ip + ':' + port
            print('Receive proxy', proxy)
            self.redis.set(name, proxy)
        elif token != TOKEN:
            self.write('Wrong Token')
        elif not port:
            self.write('No Client Port')

    def get(self, api):
        if api == 'get':
            result = self.redis.get()
            if result:
                self.write(result)
        if api == 'count':
            self.write(str(self.redis.count()))


def run():
    application = Application([
        (r'/', MainHandler),
        (r'/(.*)', MainHandler),
    ])
    print('Listening on', RECEIVER_PORT)
    application.listen(RECEIVER_PORT)
    tester = TestHandler()
    Process(target=tester.test_proxies).start()
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    run()
