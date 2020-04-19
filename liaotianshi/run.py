import tornado.web
import tornado.ioloop
import tornado.websocket
from tornado.options import define, options, parse_command_line
import tornado.httpserver
import tornado.log
import os
import json


BASE_DIR = os.path.dirname(os.path.abspath('__file__'))

define('port', default=8001, type=int)

options.log_file_prefix = os.path.join(BASE_DIR, 'logs/tornado_main.log')


class IndexHandler(tornado.web.RequestHandler):

	def get(self):
		self.render('index.html')

	def post(self):
		username = str(self.get_argument('username'))
		self.render('room.html', username=username)


class ChatHandler(tornado.websocket.WebSocketHandler):

	conns = []

	def open(self):
		username = self.get_argument('username')
		self.conns.append(self)
		xiaoxi = {
			'user': 'sys',
			'message': '欢迎 [ %s ]' % username,
		}
		self.send(xiaoxi)
		

	def on_message(self, message):
		username = self.get_argument('username')
		xiaoxi = {
			'user': username,
			'message': message,
		}
		self.send(xiaoxi)

	def on_close(self, ):
		username = self.get_argument('username')
		self.conns.remove(self)
		xiaoxi = {
			'user': 'sys',
			'message': '[ %s ] 离开' % username
		}
		self.send(xiaoxi)


	def send(self, xiaoxi):
		for conn in self.conns:
			conn.write_message(json.dumps(xiaoxi))



def make_app():
	return tornado.web.Application(
			[
				(r'/', IndexHandler),
				(r'/chat/', ChatHandler),
			],
			template_path = os.path.join(BASE_DIR, 'templates'),
			static_path = os.path.join(BASE_DIR, 'statics')
		)

def main():
	parse_command_line()
	app = make_app()
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.bind(options.port)
	http_server.start()
	tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
	main()
