#   Step 3. Non-blocking server


import socket
import random
import time
import random
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE
from functools import partial

handlers = {}

def server(port=8080):
    # socket.AF_INET - use IPv4, socket.SOCK_STREAM - use TCP protocol
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    opts = ("127.0.0.1", port)
    s.bind(opts)
    print("Server started on", opts)
    # listen(n): n - number of allowed conntections in queue for accept
    s.listen(10000);
    s.setblocking(False)
    sel = DefaultSelector()
    #   register(s, t, o):
    #   s - socket
    #   t - event type
    #   o - some optional object, for example - callback
    sel.register(s, EVENT_READ, accept)
    handlers[s] = accept(sel, s)
    while True:
        # events - dictionary {selector key: events mask}
        events = sel.select()
        for key, _ in events:
            # key.data - callbask object, which added in register method
            # key.fileobj = file descriptor of client socket
            callback = handlers[key.fileobj]
            try:
                next(callback)
            except StopIteration as ex:
                pass

def accept(sel, s):
    while True:
        conn, addr = s.accept()
        print("Connected by", addr)
        conn.setblocking(False)
        handlers[conn] = handle(sel, conn)
        sel.register(conn, EVENT_READ)
        yield

def handle(sel, conn):
    while True:
        data = conn.recv(1024)
        if not data:
            sel.unregister(conn)
            print("Disconnected by", addr)
            conn.close()
            return
        n = int(data.decode())
        res = f"{n * 2}\n"
        print(n, res.strip())
        sel.modify(conn, EVENT_WRITE)
        yield
        conn.send(res.encode())
        sel.modify(conn, EVENT_READ)
        yield

if __name__ == '__main__':
    server()
