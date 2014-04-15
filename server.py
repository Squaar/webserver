#!/usr/bin/python3

import socket
import argparse
import HTTPRequest

BUFFER_SIZE = 1024*8

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

while 1:
    conn, addr = sock.accept()

    if args.verbose:
        print("\nconnection: " + addr[0])

    data = conn.recv(BUFFER_SIZE)
    if not data:
        conn.close()
        continue

    if args.verbose:
        print(str(data))

    request = HTTPRequest.HTTPRequest(str(data))
    print(request.path)
    print(request.error_code)

    conn.close()



