# Examples of async excution tasks with futures + generators

from concurrent.futures import ThreadPoolExecutor
import time

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
        result = yield pool.submit(sleep_func, x, y)
        print("Got:", result)
    except Exception as e:
        print("Failed:", repr(e))


def after(delay, gen):
    yield pool.submit(time.sleep, delay)
    yield from gen


#t = Task(do_func(2, 'str'))
#t.step()
Task(after(10, do_func(2, 3))).step()
time.sleep(15)
