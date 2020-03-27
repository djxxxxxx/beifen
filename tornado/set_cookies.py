import tornado.ioloop
import tornado.httpserver
from tornado.options import define, options, parse_command_line
from tornado.web import Application, RequestHandler
import pymysql
import time

define('port', default=8001, type=int)

class A(RequestHandler):

    def get(self):
        # self.set_cookie('itvast', 'abc', expires=time.mktime(time.strptime\
        #     ("2020-03-28 23:59:59","%Y-%m-%d %H:%M:%S")))
        self.set_secure_cookie("itcast", "1")
        self.write('a')

class CookieCountHandler(RequestHandler):
    def get(self):
        ct = self.get_secure_cookie("page_count")
        if not ct:
            ct = 1
            self.set_secure_cookie("page_count", str(ct))
        else:
            ct = int(ct)
            ct += 1
            self.set_secure_cookie("page_count", str(ct))
        self.write(str(ct))

def make_app():
    return Application(
        [   (r'/', A),(r'/c/', CookieCountHandler) ],
            debug = True,
            cookie_secret = "LokoLorDRuO0guuL6krvwHdI14qhFkshm/BgtOG82fA=",
    )

if __name__ == '__main__':
    parse_command_line()
    app = make_app()
    sv = tornado.httpserver.HTTPServer(app)
    sv.bind(options.port)
    sv.start()
    tornado.ioloop.IOLoop.current().start()
