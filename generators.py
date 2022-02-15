# Examples of async excution tasks with futures + generators

from concurrent.futures import ThreadPoolExecutor
import time

# simple generators

def fibbonachi():
    a, b = 1, 1
    while True:
        yield a
        a, b = b, a + b


def gen_sum():
    total = 0
    while True:
        print(total)
        value = yield       # recieve value from send(<val>)
        if not value:
            return total    # return in generator throw exception with ret. value
        total+=value

def gen_curr_sum():
    total = 0
    while True:
         # function send return total and stop, after next send(<val>) assign <val>
         # and continue exec function body
        value = yield total
        total += value
    

def generators_example():
    g = fibbonachi()
    for i in range(20):
        print(next(g))

    g2 = gen_sum()
    g2.send(None)
    for i in range(1, 10):
        g2.send(i)
    try:
        g2.send(None)
    except StopIteration as ex:
        print(ex.value)
        pass

    g3 = gen_curr_sum()
    print(g3.send(None)) # go to first yield ( g3.send(None) ==   )
    for i in range(1, 10):
        print(g3.send(i))

# async task in background

class Task:
    def __init__(self, gen):
        self._gen = gen


    def step(self, value=None, exc=None):
        try:
            if exc:
                fut = self._gen.throw(exc)
            else:
                fut = self._gen.send(value)
            fut.add_done_callback(self._wakeup)
        except StopIteration as exc:
            pass

    def _wakeup(self, fut):
        try:
            result = fut.result()
            self.step(result)
        except Exception as exc:
            self.step(None, exc)


pool = ThreadPoolExecutor(max_workers=8)

def sleep_func(x, y):
    time.sleep(5)
    return x + y


def do_func(x, y):
    try:
        result = yield pool.submit(sleep_func, x, y)    # code after yieldexec in other thread
        print("Got:", result)
    except Exception as e:
        print("Failed:", repr(e))


def after(delay, gen):
    yield pool.submit(time.sleep, delay)
    yield from gen


#t = Task(do_func(2, 'str'))
#t.step()
#Task(after(10, do_func(2, 3))).step()
#time.sleep(15) # wait background task
generators_example()
