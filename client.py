import socket
import random
import time
import threading
import sys
def client(port=8080):
    s = socket.create_connection(("127.0.0.1", port))
    while True:
        n = random.randrange(10)
        msg = f"{n}\n".encode()
        s.send(msg)
        resp = s.recv(1024)
        print(resp.decode().strip())
        time.sleep(random.random() * 2)

def multiply_clients(n=8):
    threads = [threading.Thread(target=client) for _ in range(n)] 
    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    if len(sys.argv) == 2:
        multiply_clients(int(sys.argv[1]))
    elif len(sys.argv) == 1:
        client()
    assert False, "invalid args"
