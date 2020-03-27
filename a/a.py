import tornado.web
import tornado.ioloop

data = []

class A(tornado.web.RequestHandler):

    def get(self):
        self.render('a.html', data=data)
    def post(self):
        info = self.get_arguments('a')
        data.append(info)
        self.render('a.html', data=data)

app = tornado.web.Application([(r'/',A)])
app.listen(8001)
tornado.ioloop.IOLoop.current().start()
