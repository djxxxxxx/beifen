import tornado.web
import tornado.ioloop
from tornado.options import define, options, parse_command_line
import tornado.httpserver
import tornado.websocket
import re

define('port', default=8001, type=int)

data = []
class A(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        if re.match('192.168.(\d{1}.\d{1,3})', self.request.remote_ip):
            self.render('b.html', data=data)
        else:
            ag = self.request.remote_ip + '----'\
                + self.request.headers['host'] + self.request.uri
            data.append(ag)
            if len(data) > 6:
                del data[0]
            self.render('b.html', data=data)

parse_command_line()
app = tornado.web.Application([(r'(.*?)',A)])
sv = tornado.httpserver.HTTPServer(app, xheaders=True)
sv.bind(options.port)
sv.start()
tornado.ioloop.IOLoop.current().start()
