#   Step 3. Non-blocking server
#   Problem: Very obscure code. Very different from the synchronous version of the server

import socket
import random
import time
import random
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE
from functools import partial

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
    while True:
        # events - dictionary {selector key: events mask}
        events = sel.select()
        for key, _ in events:
            # key.data - callbask object, which added in register method
            # key.fileobj = file descriptor of client socket
            callback = key.data     
            callback(sel, key.fileobj)


def accept(sel, s):
    conn, addr = s.accept()
    print("Connected by", addr)
    conn.setblocking(False)
    sel.register(conn, EVENT_READ, read)
    
def read(sel, conn):
    data = conn.recv(1024)
    if not data:
        sel.unregister(conn)
        print("Disconnected by", addr)
        conn.close()
        return
    n = int(data.decode())
    res = f"{n * 2}\n"
    print(n, res.strip())
    sel.modify(conn, EVENT_WRITE, partial(write, msg=res))

def write(sel, conn, msg = None):
    if msg:
        conn.send(msg.encode())
    sel.modify(conn, EVENT_READ, read)


if __name__ == '__main__':
    server()
