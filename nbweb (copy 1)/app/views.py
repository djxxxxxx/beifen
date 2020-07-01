import tornado.web
import psycopg2

class BaseHandler(tornado.web.RequestHandler):
    async def execute(self, stmt, *args):
        with (await self.application.db.cursor()) as cur:
            await cur.execute(stmt, args)

    async def query(self, stmt, *args):
        with (await self.application.db.cursor()) as cur:
            await cur.execute(stmt, args)
            return await cur.fetchall()

    async def queryone(self, stmt, *args):
        result = await self.query(stmt, *args)
        return result[0]

    async def prepare(self):
        try:
            self.uname = self.get_secure_cookie("uname")
            return self.uname
        except:
            self.uname = 0
            return self.uname


class Index(BaseHandler):
    async def get(self):
        notes = await self.query('select * from notes')
        self.render('index.html', uname=self.uname, notes=notes)

class Note(BaseHandler):
    async def get(self, nid):
        note = await self.queryone('select * from notes where nid=%s', nid)
        self.render('note.html', uname=self.uname, note=note)


class Home(BaseHandler):
    async def get(self, uname):
        notes = await self.query('select * from notes where nuname=%s', uname)
        self.render('home.html', uname=self.uname, notes=notes)


class Login(BaseHandler):
    async def get(self):
        error = ''
        self.render('login.html', uname=self.uname, error=error)

    async def post(self):
        uname = self.get_argument('uname')
        upwd = self.get_argument('upwd')
        try:
            pwd = await self.queryone('select upasswd from users where uname = %s', uname)
            if upwd == str(pwd[0]):
                error = ''
                self.set_secure_cookie("uname", uname)
                self.redirect('/')
        except:
            error = 'wrong info'
            self.render('login.html', uname=self.uname, error=error)


class Logout(BaseHandler):
    def get(self):
        self.clear_cookie("uname")
        self.redirect('/')


class Register(BaseHandler):
    async def get(self):
        error = ''
        self.render('register.html', uname=self.uname, error=error)

    async def post(self):
        ip = self.request.remote_ip
        uname = self.get_argument('uname')
        upwd = self.get_argument('upwd')
        try:
            await self.execute('insert into users(uname, upasswd, uip, uctime)'
                'values(%s, %s, %s, CURRENT_TIMESTAMP)', uname, upwd, ip)
            self.redirect('/login/')
        except:
            error = 'account exit'   # 不管用，最后修
            self.render('register.html', uname=self.uname, error=error)


class Gly(BaseHandler):
    async def get(self):
        self.render('gly.html', uname=self.uname)
