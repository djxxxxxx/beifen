import tornado.web


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
        uid = self.get_secure_cookie("uid")
        if uid:
            self.uinfo = await self.queryone(
                'select * from users where uid=%s', int(uid)
            )
        else:
            self.uinfo = 0
            return self.uinfo


class Index(BaseHandler):
    async def get(self):
        self.render('index.html', uid=self.uinfo)

class Blog(BaseHandler):
    async def get(self):
        self.render('blog.html')


class Home(BaseHandler):
    async def get(self):
        self.render('home.html')


class Login(BaseHandler):
    async def get(self):
        self.render('login.html')


class Register(BaseHandler):
    async def get(self):
        self.render('register.html')


class Gly(BaseHandler):
    async def get(self):
        self.render('register.html')
