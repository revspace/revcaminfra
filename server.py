#!/usr/bin/python3

import sys, os, datetime, http.server, socketserver, socket, signal

camNumberToAnalogInput = {7:7, 8:8, 9:6, 10:5}

def out(str):
	print(datetime.datetime.now().strftime('[%Y-%m-%d_%H:%M:%S.%f]'), str)

class MyWebServer(socketserver.ForkingMixIn, http.server.HTTPServer):
	def server_bind(self):
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind(self.server_address)

class WebHandler(http.server.BaseHTTPRequestHandler):
	protocol_version = 'HTTP/1.1'
	def do_GET(self):
		out('['+self.path+'] ['+repr(self.client_address)+'] do_GET')
		if self.client_address[0] not in('127.0.0.1', '::1'):
			self.send_response(403)
			self.end_headers()
			out('['+self.path+'] ['+repr(self.client_address)+'] wrong IP')
		elif not self.path.startswith('/cam'):
			self.send_response(404)
			self.end_headers()
			out('['+self.path+'] ['+repr(self.client_address)+'] not a cam')
		else:
			self.send_response(200)
			port = 9000 + camNumberToAnalogInput[int(self.path[4:])]
			self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--RevSpaceCam')
			self.end_headers()
			client = socket.create_connection(('localhost', port))
			out('['+self.path+'] ['+repr(self.client_address)+'] open (port '+str(port)+')')
			try:
				while not self.wfile.closed:
					data = client.recv(4096)
					if not data:
						out('['+self.path+'] ['+repr(self.client_address)+'] break')
						break
					self.wfile.write(data)
			except Exception as e:
				out('['+self.path+'] ['+repr(self.client_address)+'] Exception: '+repr(e))
			out('['+self.path+'] ['+repr(self.client_address)+'] close')
			client.close()
		self.finish()
		self.connection.close()

def signal_handler(signal, frame):
	out('SIGINT received, shutting down')
	sys.exit(0)

if __name__ == "__main__":
	out('begin')
	server = MyWebServer(('', 9080), WebHandler)
	out('started httpserver')
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		pass
	server.server_close()
	out('end')

