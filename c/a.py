from tornado.web import Application
from  tornado.ioloop import IOLoop
from tornado.options import define, options, parse_command_line
from tornado.httpserver import HTTPServer
from app.views import *
import os
import pymysql

BASE_DIR = os.path.dirname(os.path.abspath('__file__'))

define('port', default=8001, type=int)

settings = {
    "static_path": os.path.join(BASE_DIR, "statics"),
    "template_path": os.path.join(BASE_DIR, "templates"),
    "cookie_secret": "VbWwTyk6R/y60UzYK/AURrI/zEB9tExYl2gMJI8z85E=",
    "xsrf_cookie": "ToHS43etRfCRUTFP6ULQC4XfPd+xw0ooghvqHwrB8g8=",
    "debug": True,

}

mysql_options = dict(
    host="localhost",
    user="root",
    password="123456",
    database="study",
    charset="utf8"
)

class Application(Application):
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
        self.dbc = pymysql.connect(**mysql_options)
        self.db = self.dbc.cursor()

def make_app():
    return Application(
            [   (r'/', Index),
                (r'/list/([^/]+)', List),
                (r'/register', Register),
                (r'/login', Login),
                (r'/logout', Logout),
                (r'/home', Home),
                (r'/write', Write),
                (r'/article/([^/]+)', Article),
                (r'/text', Test)
            ],  **settings
        )

if __name__ == "__main__":
    parse_command_line()
    app = make_app()
    server = HTTPServer(app)
    server.bind(options.port)
    server.start()
    IOLoop.current().start()