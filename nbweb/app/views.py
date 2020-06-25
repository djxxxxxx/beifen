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


class Beiwang(BaseHandler):
    async def get(self):
        if self.user_id:
            login = self.user_id
        else:
            login = 0
        neirong = self.query('select * from notes where nt_usr_id=%s', login)
        self.render('beiwang.html', login=login, neirong=neirong)

    async def post(self):
        await self.execute('')
        self.redirect('/')
