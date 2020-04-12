from tornado.web import RequestHandler

class Base(RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")
    @property    
    def dbc(self):
        return self.application.dbc

    @property
    def db(self):
        return self.application.db


class Test(Base):
    async def get(self):
        user = self.get_current_user()
        sql_type = "select type_name from type"
        self.db.execute(sql_type)
        type = self.db.fetchall()
        self.render('test.html', user=user, type=type)

class Index(Base):
    async def get(self):
        user = self.get_current_user()
        sql_type = "select type_name from type"
        self.db.execute(sql_type)
        type = self.db.fetchall()
        sql = "select * from article order by article_utime desc"
        self.db.execute(sql)
        article = self.db.fetchall()
        self.render('index.html', user=user, type=type, article=article)

class List(Base):
    async def get(self, atc_tp):
        user = self.get_current_user()
        sql_type = "select type_name from type"
        self.db.execute(sql_type)
        type = self.db.fetchall()
        sql_ls = "select * from article where article_type=%s"
        self.db.execute(sql_ls, atc_tp)
        tp_atc = self.db.fetchall()
        self.render('list.html', user=user, type=type, atc_tp=atc_tp,tp_atc=tp_atc)

class Register(Base):
    async def get(self):
        user = self.get_current_user()
        sql_type = "select type_name from type"
        self.db.execute(sql_type)
        type = self.db.fetchall()
        self.render('register.html', user=user, type=type)

    async def post(self):
        user = self.get_current_user()
        name = self.get_argument('name')
        mobile = self.get_argument('mobile')
        email = self.get_argument('email')
        passwd = self.get_argument('passwd')
        sql_type = "select type_name from type"
        self.db.execute(sql_type)
        type = self.db.fetchall()
        sql = "insert into user(user_name, user_passwd, user_mobile, user_email) values(%s, %s, %s, %s)"
        try:
            self.db.execute(sql, (name, passwd, mobile, email))
        except:
            self.write("db error")
        self.dbc.commit()
        self.render('login.html', user=user, type=type)


class Login(Base):
    async def get(self):
        error = ""
        user = self.get_current_user()
        sql_type = "select type_name from type"
        self.db.execute(sql_type)
        type = self.db.fetchall()
        self.render('login.html', user=user, type=type, error=error)

    async def post(self):
        user = self.get_current_user()
        name = self.get_argument("name")
        passwd = self.get_argument("passwd")
        sql_type = "select type_name from type"
        self.db.execute(sql_type)
        type = self.db.fetchall()
        sql = "select user_passwd from user where user_name=%s"
        self.db.execute(sql, name)
        try:
            upw = str(self.db.fetchone()[0])
        except:
            error = "帐号或密码有误"
            self.render("login.html", user=user, type=type, error=error)
        if passwd == upw:
            self.set_secure_cookie("user", name)
        else:
            error = "帐号或密码有误"
            self.render("login.html", user=user, type=type, error=error)
        self.redirect('/')

class Logout(Base):
    async def get(self):
        self.clear_cookie("user")
        self.redirect("/")

class Home(Base):
    async def get(self):
        user = self.get_current_user()
        sql_type = "select type_name from type"
        self.db.execute(sql_type)
        type = self.db.fetchall()
        sql_uatc = "select * from article where article_user_name=%s"
        self.db.execute(sql_uatc, user)
        usr_atc = self.db.fetchall()
        self.render('home.html', user=user, type=type, usr_atc=usr_atc)

class Write(Base):
    async def get(self):
        user = self.get_current_user()
        sql_type = "select type_name from type"
        self.db.execute(sql_type)
        type = self.db.fetchall()
        self.render('write.html', user=user, type=type)

    async def post(self):
        user = self.get_secure_cookie("user")
        sql1 = "select user_id from user where user_name=%s"
        self.db.execute(sql1, user)
        uid = str(self.db.fetchone()[0])
        title = self.get_argument("title")
        atype = self.get_argument("atype")
        article = self.get_argument("article")
        sql_type = "select type_name from type"
        self.db.execute(sql_type)
        type = self.db.fetchall()
        type_list = []
        for t in type:
            type_list.append(t[0])
        if atype in type_list:
            pass
        else:
            sql2 = "insert into type(type_name) values(%s)"
            self.db.execute(sql2, atype)
            self.dbc.commit()
            type.append(atype)
        sql = "insert into article(article_title, article_type, article_user_id, article_user_name, article_body) values(%s, %s, %s, %s,%s)"
        self.db.execute(sql, (title, atype, uid, user, article))
        self.dbc.commit()
        self.render("home.html", user=user, type=type)

class Article(Base):
    async def get(self, atc_id):
        user = self.get_current_user()
        sql_type = "select type_name from type"
        self.db.execute(sql_type)
        type = self.db.fetchall()
        sql_atc = "select * from article where article_id=%s"
        self.db.execute(sql_atc, atc_id)
        article = self.db.fetchone()
        self.render('article.html', user=user, type=type, article=article)