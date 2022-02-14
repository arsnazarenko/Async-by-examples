#   Step 1. Simple blocking echo-server and echo-client in Python.
#   Problem: We always block on operations accept, recv and send so
#   we can handle only one client in one thread

import socket
import random
import sys
import time


def server(port=8080):
    # socket.AF_INET - use IPv4, socket.SOCK_STREAM - use TCP protocol
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    opts = ("127.0.0.1", port)
    s.bind(opts)
    print("Server started on", opts)
    # listen(n): n - number of allowed conntections in queue for accept
    s.listen(10);
    while True:
        conn, addr = s.accept() 
        handle_connection(conn, addr)


def handle_connection(conn, addr):
    print("Connected by", addr)
    while True:
        data = conn.recv(1024)
        if not data:    
            break
        n = int(data.decode())
        res = f"{n * 2}\n"
        print(n, res.strip())
        conn.send(res.encode())
    print("Disconnected by", addr)

if __name__ == '__main__':
    server()

