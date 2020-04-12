import tornado.web
import tornado.ioloop
import tornado.httpserver
import config
import pymysql
# import tornadoredis

from tornado.options import options, define, parse_command_line
from urls import handlers

define("port", default=8001, type=int)

class Application(tornado.web.Application):
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
        # self.dbc = pymysql.connect(
        #         host=config.mysql_options("host"),
        #         database=config.mysql_options("database"),
        #         user=config.mysql_options("user"),
        #         password=config.mysql_options("password")
        #     )
        self.dbc = pymysql.connect(**config.mysql_options)
        self.db = self.dbc.cursor()
        # self.redis = redis.StrictRedis(
        #         host=config.redis_options("host"),
        #         port=config.redis_options("port"),
        #     )
        # self.redis = tornadoredis.Client(**config.redis_options)
        # self.redis.set("name", "zhangsan")


def main():
    parse_command_line()
    app = Application(
            handlers, **config.settings, 
        )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()