from tornado.web import RequestHandler
import random

class Base(RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")
    @property    
    def dbc(self):
        return self.application.dbc

    @property
    def db(self):
        return self.application.db

    @property
    def user(self):
        return self.get_current_user()

    @property
    def type(self):
        sql_type = "select type_name from type"
        self.db.execute(sql_type)
        return self.db.fetchall()


class Msg(Base):
    async def get(self):
        self.render('test.html', user=self.user, type=self.type)

class Index(Base):
    async def get(self):
        try:
            user = self.user.decode()
        except:
            user = self.user
        sql = "select * from article order by article_utime desc"
        self.db.execute(sql)
        article = self.db.fetchall()
        self.render('index.html', user=user, type=self.type, article=article)

class List(Base):
    async def get(self, atc_tp):
        try:
            user = self.user.decode()
        except:
            user = self.user
        sql_ls = "select * from article where article_type=%s order by article_utime desc"
        self.db.execute(sql_ls, atc_tp)
        tp_atc = self.db.fetchall()
        self.render('list.html', user=user, type=self.type, atc_tp=atc_tp,tp_atc=tp_atc)


class Register(Base):
    async def get(self):
        self.render('register.html', user=self.user, type=self.type,)

    async def post(self):
        ip = self.request.remote_ip
        name = self.get_argument('name')
        mobile = self.get_argument('mobile')
        email = self.get_argument('email')
        passwd = self.get_argument('passwd')
        if name and mobile and email and passwd:
            sql = "insert into user(user_name, user_passwd, user_mobile, user_email, user_ip) values(%s, %s, %s, %s, %s)"
            try:
                self.db.execute(sql, (name, passwd, mobile, email, ip))
            except:
                self.redirect("/register")
            self.dbc.commit()
            self.redirect("/login")
        else:
            self.redirect("/register")
        



class Login(Base):
    async def get(self):
        error = ""
        self.render('login.html', user=self.user, type=self.type, error=error)

    async def post(self):
        name = self.get_argument("name")
        passwd = self.get_argument("passwd")
        if name and passwd:
            sql = "select user_passwd from user where user_name=%s"
            try:
                self.db.execute(sql, name)
                upw = str(self.db.fetchone()[0])
            except:
                error = "帐号或密码有误"
                self.render("login.html", user=self.user, type=self.type, error=error)
            if passwd == upw:
                self.set_secure_cookie("user", name)
            else:
                error = "帐号或密码有误"
                self.render("login.html", user=self.user, type=self.type, error=error)
            self.redirect('/')
        else:
            error = "帐号密码不能为空"
            self.render("login.html", user=self.user, type=self.type, error=error)

class Logout(Base):
    async def get(self):
        self.clear_cookie("user")
        self.redirect("/")

class Home(Base):
    async def get(self, name):
        user = self.user.decode()
        if user =="dujiaxing":
            sql_uli = "select user_name, user_ip, user_status, user_ctime from user"
            self.db.execute(sql_uli)
            user_li = self.db.fetchall()
            sql_tyli = "select type_name, type_ctime from type"
            self.db.execute(sql_tyli)
            type_li = self.db.fetchall()
            sql_uatc = "select * from article where article_user_name=%s order by article_utime desc"
            self.db.execute(sql_uatc, name)
            usr_atc = self.db.fetchall()
            self.render('home.html', user=user, type=self.type, name=name, user_li=user_li, type_li=type_li, add=False, usr_atc=usr_atc)
        else:
            sql_uatc = "select * from article where article_user_name=%s order by article_utime desc"
            self.db.execute(sql_uatc, name)
            usr_atc = self.db.fetchall()
            sql_status = "select user_status from user where user_name=%s"
            self.db.execute(sql_status, name)
            usr_status = self.db.fetchone()[0]
            if name == user and usr_status:
                add = True
            else:
                add = False
            self.render('home.html', user=user, type=self.type, usr_atc=usr_atc, name=name, add=add)

class Write(Base):
    async def get(self):
        user = self.user.decode()
        self.render('write.html', user=user, type=self.type)

    async def post(self):
        user = self.user.decode()
        sql1 = "select user_id from user where user_name=%s"
        self.db.execute(sql1, user)
        uid = str(self.db.fetchone()[0])
        title = self.get_argument("title")
        atype = self.get_argument("atype")
        article = self.get_argument("article")
        type = self.type
        type_list = []
        for t in type:
            type_list.append(t[0])
        if atype in type_list:
            pass
        else:
            sql2 = "insert into type(type_name) values(%s)"
            self.db.execute(sql2, atype)
            self.dbc.commit()
        sql = "insert into article(article_title, article_type, article_user_id, article_user_name, article_body) values(%s, %s, %s, %s,%s)"
        self.db.execute(sql, (title, atype, uid, user, article))
        self.dbc.commit()
        self.redirect("/home/{}".format(user))

class Article(Base):
    async def get(self, atc_id):
        sql_atc = "select * from article where article_id=%s"
        self.db.execute(sql_atc, atc_id)
        article = self.db.fetchone()
        self.render('article.html', user=self.user, type=self.type, article=article)

class Search(Base):
    async def get(self):
        search = self.get_query_argument("search")
        sql_srch = "select * from article where article_title like %search%"
        self.db.execute(sql_srch, search)
        srch_atc = self.db.fetchall()
        self.render('search.html', user=self.user, type=self.type, srch_atc=srch_atc)

class Del(Base):
    async def get(self, id, name):
        user = self.user.decode()
        sql_cfrm = "select article_user_name from article where article_id=%s"
        self.db.execute(sql_cfrm, id)
        cfrm_nm = self.db.fetchone()
        if cfrm_nm == user or user == "dujiaxing":
            sql_del = "delete from article where article_id=%s"
            try:
                self.db.execute(sql_del, id)
                self.dbc.commit()
            except:
                pass
            self.redirect("/home/{}".format(name))
        else:
            msg = "Get fuck off !!!"
            self.render('message.html', user=self.user, type=self.type, msg=msg)

class Ban(Base):
    async def get(self, nm):
        sql_ckstatus = "select user_status from user where user_name=%s"
        self.db.execute(sql_ckstatus, nm)
        current_status = str(self.db.fetchone()[0])
        status_in = str(abs(int(current_status) - 1))
        sql_ban = "update user set user_status=%s where user_name=%s"
        self.db.execute(sql_ban, (status_in, nm))
        self.dbc.commit()
        self.redirect("/")

class Retype(Base):
    async def post(self, tpnm):
        user = self.user.decode()
        retype = self.get_argument("retype")
        sql_artp = "update article set article_type=%s where article_type=%s"
        self.db.execute(sql_artp, (retype, tpnm))
        sql_trtp = "update type set type_name=%s where type_name=%s"
        try:
            self.db.execute(sql_trtp, (retype, tpnm))
            self.dbc.commit()
        except:
            sql_deltp = "delete from type where type_name=%s"
            self.db.execute(sql_deltp, tpnm)
        self.redirect("/home/{}".format(user))
        