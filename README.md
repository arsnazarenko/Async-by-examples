# Asynchronous programming in Python step by step

### Prerequisites
- Python3.8

### Server

#### 1. One-thread server with blocking IO

Run:
```shell
$ python3 block_server.py
```

Simple one thread server for finding squares of numbers. Sockets in blocking mode. Clients can only be processed sequentially.

[block_server.py](https://github.com/arsnazarenko/async-by-examples/blob/master/block_server.py)

#### 2. Server with blocking IO and thread per connection
Run:
```shell
$ python3 thread_block_server.py
```
The modified server from the previous step. One thread per client. C10k problem
[thread_block_server.py](https://github.com/arsnazarenko/async-by-examples/blob/master/thread_block_server.py)

#### 3. Server with non-blocking IO
Run:
```shell
$ python3 non_block_server.py
```
Non-blocking server with *select()* API

[non_block_server.py](https://github.com/arsnazarenko/async-by-examples/blob/master/non_block_server.py)


#### 4. Server with non-blocking IO and async/await syntax
Run:
```shell
$ python3 async_server.py
```
Non-blocking server with scheduler and async/await syntax.

[async_server.py](https://github.com/arsnazarenko/async-by-examples/blob/master/async_server.py)

### Client

Run: 
```shell
$ python3 client.py - one thread client 
$ python3 client.py [N] - client with N thread 
```
Client send to server numbers in infinity loop

[async_server.py](https://github.com/arsnazarenko/async-by-examples/blob/master/async_server.py)

## Result

``` python
def server(port=8080):
    s = create_socket(port)
    print("Server started")
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
```


### Asynchronous non-blocking server
``` python
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
```

As you can see from the code, we are now writing asynchronous code in a synchronous style
