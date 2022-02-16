import socket
from collections import deque
from select import select

class Send:
    def __init__(self, client, msg):
        self.client = client
        self.msg = msg

    def __await__(self):
        yield ('send', self.client)
        return self.client.send(self.msg)

class Recv:
    def __init__(self, client):
        self.client = client

    def __await__(self):
        yield ('recv', self.client)
        return self.client.recv(1024)

class Accept:
    def __init__(self, socket):
        self.socket = socket

    def __await__(self):
        yield ('recv', self.socket)
        return self.socket.accept()
        

def accept(socket):
    return Accept(socket) 

def send(client, msg):
    return Send(client, msg)

def recv(client):
    return Recv(client)

class Scheduler:
    def __init__(self):
        self.tasks = deque()
        self.recv_wait = {}
        self.send_wait = {}
    
    def create_task(self, task):
        self.tasks.append(task)

    def run(self):
        while any([self.tasks, self.recv_wait, self.send_wait]):
            while not self.tasks:
                # Not active tasks to run
                # Wait for I/O
                can_recv, can_send, _ = select(self.recv_wait,  self.send_wait, [])
                for s in can_recv:
                    self.tasks.append(self.recv_wait.pop(s))
                for s in can_send:
                    self.tasks.append(self.send_wait.pop(s))

            task = self.tasks.popleft()
            try:
                why, what = task.send(None)
                if why == 'recv':
                    self.recv_wait[what] = task
                elif why == 'send':
                    self.send_wait[what] = task
                else:
                    raise RuntimeError("ARG!")
            except StopIteration:
                print("Task done")



def create_socket(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    opts = ("127.0.0.1", port)
    s.bind(opts)
    s.setblocking(False)
    s.listen(1000)
    return s

async def server(scheduler, port=8080):
    s = create_socket(port)
    print("Server started")
    while True:
        client, addr = await accept(s)
        client.setblocking(False)
        scheduler.create_task(handle_connection(client, addr))
        
async def handle_connection(client, addr):
    print("Connected by", addr)
    while True:
        data = await recv(client)
        if not data:
            break
        n = int(data.decode())
        res = f"{n * 2}\n"
        print(n, res.strip())
        await send(client, res.encode())
    print("Disconnected by", addr)



if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.create_task(server(scheduler))
    scheduler.run()
