# Step1. Motivation

# Coroutines in python make it easy to create cooperative multitasking in one thread

def step1():

    def coro1():
        print("coro1 doing some work")
        yield
        print("coro1 doing some work")
        yield

    def coro2():
        print("coro2 doing some work")
        yield
        print("coro2 doing some work")
        yield
    

    # It's brain of this program - it controls the flow of program execution
    def scheduler():    
        c1 = coro1()
        c2 = coro2()
        c1.send(None)
        c2.send(None)
        c1.send(None)
        c2.send(None)

    scheduler()

# Step2. Create automatic scheduler 

'''
    Let's create automatic scheduler, wich will can execute all coroutinnes, 
    which can perform all the tasks given to it while they are available
'''

def step2():
    from collections import deque
    
    def coro1():
        print("coro1 doing some work")
        yield
        print("coro1 doing some work")
        yield

    def coro2():
        print("coro2 doing some work")
        yield
        print("coro2 doing some work")
        yield
    

    def scheduler(coros):
        ready = deque(coros)
        while ready:
            try:
                # take next coroutine that is ready to run
                coro = ready.popleft()
                
                #run it unitl the next yield
                result = coro.send(None)
                
                #schedule it for another execution
                ready.append(coro)
            except StopIteration:
                pass

    scheduler([coro1, coro2])


# Step3. Modify scheduler for waiting tasks

# Example without concurrency
# We just sleep while execute waiting tasks
def step3():

    import time    

    def get_page():
        print("Starting to download page")
        time.sleep(1)
        print("Done downloading page")
        return "<html>Hello</html>"

    def read_db():
        print("Starting to retrieve data from db")
        time.sleep(0.5)
        print("Connected to db")
        time.sleep(1)
        print("Done retrieving data from db")
        return "db-data"

    def run():
        get_page()
        read_db()

    run()   # 2.5 s

# Step 4. Smart scheduler
# But we can execute other operation, until waiting operation can't continue execution

# Let's improve Scheduler implementation
import time
from collections import deque
import heapq

class Scheduler:
    
    def __init__(self, coros):
        self.ready = deque(coros)
        self.sleeping = []
    
    def run(self):
        while True:
            if not self.ready and not self.sleeping:
                break
            # wait for nearest sleeper,
            # if no coro can be executed immediately right now 
            if not self.ready:
                dedline, coro = heapq.heappop(self.sleeping)
                wait = dedline - time.time()
                if wait > 0: 
                    time.sleep(wait)
                self.ready.append(coro)
        
            try:
                coro = self.ready.popleft()
                result = coro.send(None)
                # special case for a coro that wonts to be put to sleep
                if len(result) == 2 and result[0] == "sleep":
                    dedline = time.time() + result[1]
                    heapq.heappush(self.sleeping, (dedline, coro))
                else:
                    print(f"Got: {result}")
                    self.ready.append(coro)
            except StopIteration:
                pass

def step4():
    # New impls of tasks. Now it's coroutines 
    def get_page():
        print("Starting to download page")
        yield ("sleep", 1)
        print("Done downloading page")
        yield "<html>Hello</html>"

    def read_db():
        print("Starting to retrieve data from db")
        yield ("sleep", 0.5)
        print("Connected to db")
        yield ("sleep", 1)
        print("Done retrieving data from db")
        yield "db-data"

    
       
    #Scheduler([get_page(), read_db()]).run()  # 1.5 s
    
    '''

    Create 100 tasks:
    get_page()  
    get_from_db()
    get_page()
    get_from_db()
    .
    .
    .
    1000

    '''
    # Exec time: 1.53 s
    # Sequentially impl of scheduler exec this tasks for 2500 s ~ 40 min
    Scheduler([get_page() if i%2 == 0 else read_db() for i in range(1000)]).run()   


# Step 5. Nested coroutines

'''
 Example. We have some task that downloads some page and then dumps it into a database
 We want to create the same function:
    
 def worker():
     page = get_page()
     write_db(page)
    
 HOW?

'''
def step5():

    
    def get_page():
        print("Starting to download page")
        yield ("sleep", 1)
        print("Done downloading page")
        yield "<html>Hello</html>"

    def write_db(page):
        print("Starting to write data to db")
        yield ("sleep", 0.5)
        print("Connected to db")
        yield ("sleep", 1)
        print("Done writing data to db")


    
    def worker():
        for step in get_page():
            yield step 
        page = step
        for step in write_db(page):
            yield step
    

    Scheduler([worker()]).run()


# Step 6. yield from


def step6():
 
    def get_page():
        print("Starting to download page")
        yield ("sleep", 1)
        print("Done downloading page")
        return "<html>Hello</html>" # now, we use return !!!

    def write_db(page):
        print("Starting to write data to db")
        yield ("sleep", 0.5)
        print("Connected to db")
        yield ("sleep", 1)
        print("Done writing data to db")


    
    def worker_old():
        for step in get_page():     # return <value> will assign to variable before ' = yield from'
            yield step              # 
        page = step                 # the same as: page = yield from get_page() 

        for step in write_db(page): # the same as: yield from write_db(page)
            yield step              #
    
    # new beautiful version
    def worker():
        page = yield from get_page()
        yield from write_db(page)


    Scheduler([worker()]).run()


# Step 7. yield from -> await

def step7():

    class Sleep:
        def __init__(self, delay):
            self.delay = delay

        def __await__(self):
            yield ("sleep", self.delay)

    def sleep(delay):
        return Sleep(delay)

    async def get_page():
        print("Starting to download page")
        await sleep(1)  # await can use only with awaiteable object
        print("Done downloading page")
        return "<html>Hello</html>" # now, we use return !!!

    async def write_db(page):
        print("Starting to write data to db")
        await sleep(0.5)
        print("Connected to db")
        await sleep(1)
        print("Done writing data to db")


    
    async def worker():
        page = await get_page()
        await write_db(page)
    
    Scheduler([worker() for i in range(1000)]).run()


if __name__ == '__main__':
    #step1()i
    #step2()
    #step3()
    #step4()
    #step5()
    #step6()
    step7()




