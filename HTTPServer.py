#!/usr/bin/python3

import socket
import HTTPRequest
import os
import argparse
from os.path import isdir


class HTTPServer():

    BUFFER_SIZE = 1024*8

    def __init__(self, sock, verbose=False):
        self.sock = sock
        self.conn = None
        self.addr = None
        self.verbose = verbose
        self.cwd = os.getcwd()
        self.servPath = os.path.dirname(os.path.realpath(__file__))

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
            else:
                if self.verbose:
                    print(request.path)
                self.handle_request(request)

            conn.close()


    def handle_request(self, request):
        request.file = None
        if isdir(self.cwd + request.path):
            try:
                path = self.cwd + request.path + "/index.html"
                request.file = open(path, "rb")
                request.fileSize = os.stat(path).st_size
            except IOError as e:
                if request.verbose:
                    print(str(e.errno) + " " + e.errstr)
                try:
                    path = self.cwd + request.path + "/index.htm"
                    request.file = open(path, "rb")
                    request.fileSize = os.stat(path).st_size
                except IOError as f:
                    if request.verbose:
                        print(str(f.errno) + " " + f.errstr)
                    #should generate index here but 404 for now
                    self.handle_error(404, "File not found.")
            if request.file is not None:
                header = generate_response_header(200, "OK", "text/html", request.fileSize)
                self.conn.send(header + request.file.read())

            else:
                try:
                    path = self.cwd + request.path
                    request.file = open(path, "rb")
                    request.fileSize = os.stat(path).st_size
                    header = generate_response_header(200, "OK", "text/html", request.fileSize)
                    self.conn.send(request.file.read())
                except IOError as e:
                    if request.verbose:
                        print(str(f.errno) + " " + f.errstr)
                    self.handle_error(404, "File not found.")


    def handle_error(self, errno, errstr):
        fd = errstr
        size = len(fd)
        try:
            path = self.servPath + "/errors/" + str(errno) + ".html"
            fd = open(path, "rb")
            size = os.stat(path).st_size
        except IOError as e:
            print("Error opening error")
            path = self.servPath + "/errors/500.html"
            fd = open(path, "rb")
            size = os.stat(path).st_size
                
            header = generate_response_header(errno, errstr, "text/html", size)
            self.conn.send(header + fd.read())


    def generate_response_header(self, code, message, type, length):
        header = "HTTP/1.1 " + code + " " + message + "\r\n" 
        header += "Content-Type: " + type + "; charset=utf-8\r\n" 
        header += "Content-Length: " + length + "\r\n\r\n"
        return header


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("port", type=int, nargs="?", default=8888, 
            help="The port to run on. Defaults to 8888.")
    parser.add_argument("-v", "--verbose", action="store_true", 
            help="Verbosity.")
    args = parser.parse_args()

    host = socket.gethostbyname(socket.gethostname())

    if args.verbose:
        print("verbose ON")
        print("host: " + str(host) + ":" + str(args.port))

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", args.port))
    sock.listen(1)
    print("ready") 

    server = HTTPServer(sock, verbose=args.verbose)
    server.run()
