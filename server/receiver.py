import tornado.ioloop
import tornado.web
from tornado.web import RequestHandler, Application
from server.config import *
from server.db import RedisClient


class Receiver():
    class MainHandler(RequestHandler):

        redis = RedisClient()

        def post(self):
            token = self.get_body_argument('token', default=None, strip=False)
            port = self.get_body_argument('port', default=None, strip=False)
            if token == TOKEN and port:
                ip = self.request.remote_ip
                proxy = ip + ':' + port
                print('Receive from', proxy)
                self.redis.add(proxy)
            elif token != TOKEN:
                self.write('Wrong Token')
            elif not port:
                self.write('No Client Port')

    def run(self):
        application = Application([
            (r'/', self.MainHandler),
        ])
        application.listen(8888)


if __name__ == '__main__':
    receiver = Receiver()
    receiver.run()
