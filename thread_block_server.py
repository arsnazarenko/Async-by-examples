#   Step 2. Create one thread for one client.
#   Problem. C10k

import socket
import random
import time
import threading


def server(port=8080):
    # socket.AF_INET - use IPv4, socket.SOCK_STREAM - use TCP protocol
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    opts = ("127.0.0.1", port)
    s.bind(opts)
    print("Server started on", opts)
    # listen(n): n - number of allowed conntections in queue for accept
    s.listen(1000);
    while True:
        conn, addr = s.accept() 
        t = threading.Thread(target=handle_connection, args=(conn, addr))
        t.start()

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

