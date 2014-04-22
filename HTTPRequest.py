from http.server import BaseHTTPRequestHandler
from io import StringIO
from contextlib import suppress
from http.client import HTTPException
from os.path import isdir

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


    # def send_response(self):
    #     self.file = None
    #     if isdir(self.path):
    #         try:
    #             self.file = open(self.path + "/index.html", "rb")
    #         except IOError as e:
    #             if self.verbose:
    #                 print(str(e.errno) + " " + e.errstr)
    #             try:
    #                 self.file = open(self.path + "/index.htm", "rb")
    #             except IOError as f:
    #                 if self.verbose:
    #                     print(str(f.errno) + " " + f.errstr)
    #                 #generate index page
    #         if self.file is not None:
    #             #read in file and send

    #     else:
    #         try:
    #             self.file = open(self.path, "rb")
    #         except IOError as e:
    #             if self.verbose:
    #                 print(str(f.errno) + " " + f.errstr)
    #             send_error(404, "File not found.")
