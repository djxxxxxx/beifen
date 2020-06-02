import tornado.web
import tornado.ioloop
import os
import aiopg
import tornado.locks
from tornado.options import define, options, parse_command_line

define("port", default=8001, type=int)
settings = {
    "static_path": os.path.join(os.path.dirname('__file__'), 'statics'),
    "template_path": os.path.join(os.path.dirname('__file__'), "templates"),
    "coocie_secret": "nv+yNoPSQf29VcDE/d7F6T1+M/N+kEbLm+DhWOenDjM=",
    "xsrf_cookie": "Z6fsvaBMQJCMZ1LAPwB1bmTyaRcGgkR0rZqULdcX+JU=",
    "debug": "{}".format(os.environ['debug']),
}

class Application(tornado.web.Application):
    def __init__(self,db):
        self.db = db
        handlers = [
            (r'/', A)
        ]
        super(Application, self).__init__(handlers, **settings)

class BaseHandler(tornado.web.RequestHandler):
    async def execute(self, stmt, *args):
        with (await self.application.db.cursor()) as cur:
            await cur.execute(stmt, args)

    async def query(self, stmt, *args):
        with (await self.application.db.cursor()) as cur:
            await cur.execute(stmt, args)
            return await cur.fetchall()


class A(BaseHandler):
    async def get(self):
        names = await self.query('select user_name from users')
        self.render('a.html', names=names)

    async def post(self):
        name = self.get_argument("name")
        passwd = self.get_argument("passwd")
        await self.execute('insert into users(user_name, passwd) values(%s,%s)', name,passwd,)
        self.redirect('/')


async def main():
    async with aiopg.create_pool(
        host='localhost',
        port=5432,
        user=os.environ['dbusr'],
        password=os.environ['dbpwd'],
        dbname=os.environ['dbnm'],
    )as db:
        parse_command_line()
        app = Application(db)
        app.listen(options.port)
        shutdown_event = tornado.locks.Event()
        await shutdown_event.wait()


if __name__ == '__main__':
    tornado.ioloop.IOLoop.current().run_sync(main)
