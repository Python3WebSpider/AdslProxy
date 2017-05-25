import tornado.ioloop
import tornado.web
from tornado.web import RequestHandler, Application
from adslproxy.config import *
from adslproxy.db import RedisClient


class MainHandler(RequestHandler):
    redis = RedisClient()

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
    application.listen(API_PORT)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    run()
