# coding=utf-8
import json
import tornado.ioloop
import tornado.web
from tornado.web import RequestHandler, Application
from adslproxy.db import RedisClient
from adslproxy.settings import *
from loguru import logger


class Server(RequestHandler):
    """
    服务器，对接 Redis 并提供 API
    """
    
    def initialize(self, redis):
        """
        初始化
        :param redis:
        :return:
        """
        self.redis = redis
    
    def get(self, api=''):
        """
        API 列表
        :param api:
        :return:
        """
        if not api:
            links = ['random', 'proxies', 'names', 'all', 'count']
            self.write('<h4>Welcome to ADSL Proxy API</h4>')
            for link in links:
                self.write('<a href=' + link + '>' + link + '</a><br>')
        
        if api == 'random':
            result = self.redis.random()
            if result:
                self.write(result)
        
        if api == 'names':
            result = self.redis.names()
            if result:
                self.write(json.dumps(result))
        
        if api == 'proxies':
            result = self.redis.proxies()
            if result:
                self.write(json.dumps(result))
        
        if api == 'all':
            result = self.redis.all()
            if result:
                self.write(json.dumps(result))
        
        if api == 'count':
            self.write(str(self.redis.count()))


def serve(redis=None, port=SERVER_PORT, address=SERVER_HOST):
    if not redis:
        redis = RedisClient()
    application = Application([
        (r'/', Server, dict(redis=redis)),
        (r'/(.*)', Server, dict(redis=redis)),
    ])
    application.listen(port, address=address)
    logger.info(f'API listening on http://{address}:{port}')
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    serve()
