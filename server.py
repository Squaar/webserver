#!/usr/bin/python3

import socket
import argparse

BUFFER_SIZE = 1024

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

    data = ""
    while 1:
        newData = conn.recv(BUFFER_SIZE)
        if not newData:
            break
        else:
            data += str(newData)

    if args.verbose:
        print(str(data))

    conn.close()



