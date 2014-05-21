from http.server import BaseHTTPRequestHandler
from io import StringIO
from contextlib import suppress
from http.client import HTTPException


class HTTPRequest(BaseHTTPRequestHandler):
	def __init__(self, request, verbose=False):
		self.verbose = verbose
		self.rfile = StringIO(str(request, "UTF-8"))
		self.raw_requestline = bytes(self.rfile.readline(), "UTF-8")
		self.error_code = self.error_message = None

		#Ignore this exception. It is not relevant if you're not useing the http.client class
		with suppress(HTTPException):
			self.parse_request()


	def send_error(self, code, message):
		self.error_code = code
		self.error_message = message
