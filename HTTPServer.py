import socket
import HTTPRequest
from os.path import isdir
from os import getcwd

class HTTPServer():

	BUFFER_SIZE = 1024*8

	def __init__(self, socket, verbose=False):
		self.sock = socket
		self.conn = None
		self.addr = None
		self.verbose = verbose
		self.cwd = os.getcwd()



	def run(self):
		while 1:
		    conn, addr = self.sock.accept()
		    self.conn = conn
		    self.addr = addr

		    if self.verbose:
		        print("\nconnection: " + addr[0])

		    data = conn.recv(HTTPServer.BUFFER_SIZE)
		    if not data:
		        conn.close()
		        continue

		    request = HTTPRequest.HTTPRequest(data)

		    if request.error_code is not None:
		    	handle_error(request.errno, request.errstr)

		    if self.verbose:
		        print(request.path)
		    self.handle_request(request)

		    conn.close()


	def handle_request(self, request):
		request.file = None
		if isdir(request.path):
			try:
				request.file = open(self.cwd + request.path + "/index.html", "rb")
			except IOError as e:
				if request.verbose:
					print(str(e.errno) + " " + e.errstr)
				try:
					request.file = open(self.cwd + request.path + "/index.htm", "rb")
				except IOError as f:
					if request.verbose:
						print(str(f.errno) + " " + f.errstr)
					#generate index page
			# if request.file is not None:
				#read in file and send

		else:
			try:
				request.file = open(self.cwd + request.path, "rb")
			except IOError as e:
				if request.verbose:
					print(str(f.errno) + " " + f.errstr)
				handle_error(404, "File not found.")

	def handle_error(self, errno, errstr):
		fd = errstr
		try:
			fd = open("errors/" + str(errno) + ".html", "rb")
		except IOError as e:
			fd = open("errors/500.html", "rb")

		self.conn.send(fd.read())

