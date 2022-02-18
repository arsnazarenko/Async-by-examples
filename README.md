# Asynchronous programming step by step
---
## Step 1. Generators in python 
[source code](https://github.com/arsnazarenko/async-by-examples/blob/master/generators.py)
>
> Examples of generators in python. Some trick for asynchronous function execution with Future and generators. 

## Step 2. From generators to async/await
[source code](https://github.com/arsnazarenko/async-by-examples/blob/master/one_thread_concurrency.py)
>
> Concurrency in one thread. Building your own async/await from scratch. Scheduler for tasks.

## Step 3. Blocking IO
[source code](https://github.com/arsnazarenko/async-by-examples/blob/master/block.py)
>
> Examples of one thread server for finding squares of numbers. Sockets in blocking mode. Clients can only be processed sequentially.

## Step 3. Blocking IO with multiply threads
[source code](https://github.com/arsnazarenko/async-by-examples/blob/master/thread.py)
>
> The modified server from the previous step. One thread per client.

## Step 4. Non-blocking IO
[source code](https://github.com/arsnazarenko/async-by-examples/blob/master/non_block.py)
>
> Non-blocking server with *select()* API

## Step 5. Non blocking IO with async/await
[source code](https://github.com/arsnazarenko/async-by-examples/blob/master/async_server.py)
>
> Non blocking server with scheduler and async/await syntax.

# Results
---
### Synchronous blocking server
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
>
> As you can see from the code, we are now writing asynchronous code in a synchronous style
## Client for servers:
[source code](https://github.com/arsnazarenko/async-by-examples/blob/master/client.py)

