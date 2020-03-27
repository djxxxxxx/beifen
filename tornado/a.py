import tornado.ioloop
import tornado.httpserver
from tornado.options import define, options, parse_command_line
from tornado.web import Application, RequestHandler
import pymysql

define('port', default=8001, type=int)

class A(RequestHandler):

    def get(self):
        uid = self.get_argument('uid')
        sql = "select ui_name, ui_mobile, hi_name, hi_address, hi_price\
            from it_user_info join it_house_info on ui_user_id=hi_user_id\
            where ui_user_id=%s"
        try:
            self.application.db.execute(sql, uid)
        except Exception as e:
            return self.write("db_error, data=[]")
        data = self.application.db.fetchall()
        houses = []
        if data:
            for d in data:
                house = {
                    "uname":d[0],
                    "mobile":d[1],
                    "hname":d[2],
                    "adress":d[3],
                    "price":d[4],
                }
                houses.append(house)
        self.render('b.html', data=data, houses=houses)

    def post(self):
        name = self.get_argument('name')
        passwd = self.get_argument('passwd')
        mobile = self.get_argument('mobile')
        sql = "insert into it_user_info(ui_name, ui_passwd, ui_mobile)\
            values(%s, %s, %s)"
        try:
            self.application.db.execute(sql, (name,
                passwd, mobile))
        except Exception as e:
            return self.write('db_error')
        self.application.dbc.commit()
        print(self.application.db.lastrowid)
        self.application.db.execute('select * from it_user_info')
        data = self.application.db.fetchall()
        self.render('b.html', data=data)

class Application(Application):

    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
        self.dbc = pymysql.connect(
            host='localhost', user='root', password='123',
            database='itcast', charset='utf8')
        self.db = self.dbc.cursor()

def make_app():
    return Application(
        [(r'/', A), ], debug = True)

if __name__ == '__main__':
    parse_command_line()
    app = make_app()
    sv = tornado.httpserver.HTTPServer(app)
    sv.bind(options.port)
    sv.start()
    tornado.ioloop.IOLoop.current().start()
