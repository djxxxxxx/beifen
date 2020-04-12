import os

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "statics"),
    "templates_path": os.path.join(os.path.dirname(__file__), "templates"),
    "cookie_secret": "VbWwTyk6R/y60UzYK/AURrI/zEB9tExYl2gMJI8z85E=",
    "xsrf_cookie": "ToHS43etRfCRUTFP6ULQC4XfPd+xw0ooghvqHwrB8g8=",
    "debug": True,

}

mysql_options = dict(
    host="localhost",
    user="root",
    password="123456",
    database="itcast",
    charset="utf8"
)

redis_options = dict(
    host="localhost",
    port=6379
)