import tornado.web
import tornado.ioloop
import tornado.websocket
import os

base = os.path.dirname(os.path.abspath('__file__'))

class A(tornado.web.RequestHandler):
    def get(self):
        self.render('c.html')

jilu = []
class B(tornado.websocket.WebSocketHandler):
    conn = []
    def open(self):
        self.conn.append(self)
        for j in jilu:
            self.write_message(j)
        for c in self.conn:
            c.write_message('欢迎新来的,目前人数 %s' %len(self.conn))
    def on_message(self, msg):
        jilu.append(msg)
        if len(jilu) > 6:
            del jilu[0]
        for c in self.conn:
            c.write_message(msg)
    def on_close(self):
        self.conn.remove(self)
        for c in self.conn:
            c.write_message('有人离开,目前人数 %s' %len(self.conn))

app = tornado.web.Application([(r'/',A),(r'/b/',B)],
    static_path=os.path.join(base,'statics'),debug=True)
app.listen(8001)
tornado.ioloop.IOLoop.current().start()
