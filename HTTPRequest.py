from http.server import BaseHTTPRequestHandler
from io import StringIO

class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, request):
        self.rfile = StringIO(request)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message
