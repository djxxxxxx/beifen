import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    async def execute(self, stmt, *args):
        with (await self.application.db.cursor()) as cur:
            await cur.execute(stmt, args)

    async def query(self, stmt, *args):
        with (await self.application.db.cursor()) as cur:
            await cur.execute(stmt, args)
            return await cur.fetchall()

    async def user_id(self):
        user_name =  await self.get_secure_cookie('user')
        return  await self.query('select usr_id from users where usr_name=%s', user_name)


class Index(BaseHandler):
    async def get(self):
        login = 1
        note = ['abc路其袖子','def加油干','ghi绿水青山']
        self.render('index.html',login=login, note=note)

    async def post(self):
        await self.execute('')
        self.redirect('/')
