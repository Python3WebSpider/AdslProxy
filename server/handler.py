import tornado.ioloop
import tornado.web
import json
from tornado.web import RequestHandler, Application
from server.config import *
from server.db import RedisClient


class MainHandler(RequestHandler):
    redis = RedisClient()

    def post(self):
        token = self.get_body_argument('token', default=None, strip=False)
        port = self.get_body_argument('port', default=None, strip=False)
        print(token)

        if token == TOKEN and port:
            ip = self.request.remote_ip
            print(ip)
            proxy = ip + ':' + port
            print(proxy)
            self.redis.add(proxy)
        elif token != TOKEN:
            self.write('Wrong Token')
        elif not port:
            self.write('No Client Port')


if __name__ == '__main__':
    application = Application([
        (r'/', MainHandler),
    ])
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
