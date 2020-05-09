import asyncio
import json
import random
import string
import tempfile
import time
from itertools import cycle

import aiohttp
import bcrypt
import numpy as np
import pylab as py
import requests
import uvloop


class AsyncBatcher(object):
    def __init__(self, batch_size):
        self.batch_size = batch_size
        self.batch = []
        self.client_session = None
        self.url = f"http://127.0.0.1:8080/add"

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.flush()

    def save(self, result):
        self.batch.append(result)
        if len(self.batch) == self.batch_size:
            self.flush()

    def flush(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.__flush())

    async def __flush(self):
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch(result, session) for result in self.batch]
            for task in asyncio.as_completed(tasks):
                await task
        self.batch.clear()

    async def fetch(self, result, session):
        async with session.post(self.url, data=result) as response:
            return await response.json()


def save_result_serial(result):
    url = f"http://127.0.0.1:8080/add"
    response = requests.post(url, data=result)
    return response.json()


def save_result_aiohttp(client_session):
    sem = asyncio.Semaphore(100)

    async def saver(result):
        nonlocal sem, client_session
        url = f"http://127.0.0.1:8080/add"
        async with sem:
            async with client_session.post(url, data=result) as response:
                return await response.json()

    return saver


def do_task(i, difficulty):
    passwd = "".join(random.sample(string.ascii_lowercase, 10)).encode("utf8")
    salt = bcrypt.gensalt(difficulty)
    result = bcrypt.hashpw(passwd, salt)
    return result.decode("utf8")


def calculate_task_serial(num_iter, task_difficulty):
    for i in range(num_iter):
        result = do_task(i, task_difficulty)
        save_result_serial(result)


def calculate_task_batch(num_iter, task_difficulty):
    batcher = AsyncBatcher(100)
    for i in range(num_iter):
        result = do_task(i, task_difficulty)
        batcher.save(result)
    batcher.flush()


def calculate_task_noio(num_iter, task_difficulty):
    for i in range(num_iter):
        result = do_task(i, task_difficulty)


def calculate_task_fileio(num_iter, task_difficulty):
    with tempfile.TemporaryFile("w+") as fd:
        for i in range(num_iter):
            result = do_task(i, task_difficulty)
            fd.write(f"{result}\n")


async def calculate_task_aiohttp(num_iter, task_difficulty):
    tasks = []
    async with aiohttp.ClientSession() as client_session:
        saver = save_result_aiohttp(client_session)
        for i in range(num_iter):
            result = do_task(i, task_difficulty)
            task = asyncio.create_task(saver(result))  # <1>
            tasks.append(task)
            await asyncio.sleep(0)  # <2>
        await asyncio.wait(tasks)  # <3>


async def calculate_task_aiohttp_timer(num_iter, task_difficulty):
    tasks = []
    times = []
    async with aiohttp.ClientSession() as client_session:
        saver = save_result_aiohttp(client_session)

        async def saver_time(result):
            nonlocal saver, times
            start = time.perf_counter()
            output = await saver(result)
            end = time.perf_counter()
            times.append((1, start, end))
            return output

        for i in range(num_iter):
            start = time.perf_counter()
            result = do_task(i, task_difficulty)
            end = time.perf_counter()
            times.append((0, start, end))
            task = asyncio.create_task(saver_time(result))  # <1>
            tasks.append(task)
            await asyncio.sleep(0)  # <2>
        await asyncio.wait(tasks)  # <3>
    return times


def async_callgraph():
    loop = asyncio.get_event_loop()
    times = loop.run_until_complete(calculate_task_aiohttp_timer(25, 12))
    times.sort(key=lambda x: x[1])
    data = np.asarray(times)
    min_time = min(data[:, 1])

    fig = py.figure()
    py.title("Call timeline for async saver")
    marks = ["-*r", "--ob"]
    lines = [None, None]
    for i in range(data.shape[0]):
        d = data[i]
        idx = int(d[0])
        line = py.plot(d[1:] - min_time, [i, i], marks[idx])
        lines[idx] = line[0]
    py.legend(lines, ("CPU Time", "IO Time"))
    py.xlabel("Time")
    py.ylabel("Request Number")
    py.savefig("images/async_callgraph.png")
    py.close(fig)


if __name__ == "__main__":
    num_iter = 1000

    try:
        data = json.load(open("workloads.json"))
    except FileNotFoundError:
        data = {
            "async": [],
            "serial": [],
            "no IO": [],
            "file IO": [],
            "batches": [],
            "async+uvloop": [],
        }
        _aloop = asyncio.get_event_loop()
        _uvloop = uvloop.new_event_loop()
        for difficulty, num_iter in ((8, 600), (10, 400), (11, 400), (12, 400)):
            print(f"Difficulty: {difficulty}")

            start = time.perf_counter()
            calculate_task_noio(num_iter, difficulty)
            t = time.perf_counter() - start
            print("noIO code took: {} {}s".format(num_iter, t))
            data["no IO"].append((num_iter, difficulty, t))

            start = time.perf_counter()
            calculate_task_batch(num_iter, difficulty)
            t = time.perf_counter() - start
            print("batch code took: {} {}s".format(num_iter, t))
            data["batches"].append((num_iter, difficulty, t))

            start = time.perf_counter()
            calculate_task_fileio(num_iter, difficulty)
            t = time.perf_counter() - start
            print("fileIO code took: {} {}s".format(num_iter, t))
            data["file IO"].append((num_iter, difficulty, t))

            start = time.perf_counter()
            task = calculate_task_aiohttp(num_iter, difficulty)
            _aloop.run_until_complete(task)
            t = time.perf_counter() - start
            print("Async code took: {} {}s".format(num_iter, t))
            data["async"].append((num_iter, difficulty, t))

            start = time.perf_counter()
            task = calculate_task_aiohttp(num_iter, difficulty)
            _uvloop.run_until_complete(task)
            t = time.perf_counter() - start
            print("Async+uvloop code took: {} {}s".format(num_iter, t))
            data["async+uvloop"].append((num_iter, difficulty, t))

            start = time.perf_counter()
            calculate_task_serial(num_iter, difficulty)
            t = time.perf_counter() - start
            print("Serial code took: {} {}s".format(num_iter, t))
            data["serial"].append((num_iter, difficulty, t))
        json.dump(data, open("workloads.json", "w+"))

    m = cycle(".ovPX*1")
    c = cycle("bgrcmk")
    cm = (f"-{c}{m}" for c, m in zip(c, m))
    markers = dict(zip(data.keys(), cm))

    subplot_keys = [
        ["serial", "no IO"],
        ["batches", "no IO"],
        ["async", "no IO"],
        ["serial", "batches", "async", "no IO"],
        ["batches", "async", "no IO"],
    ]
    for keys in subplot_keys:
        keys.sort(key=lambda i: data[i][2][-1], reverse=True)

    b = np.asarray(data["no IO"])
    baseline = b[:, 2] / b[:, 0]
    for keys in subplot_keys:
        fig = py.figure()
        ax = py.gca()
        for k in keys:
            d = np.asarray(data[k])
            t = d[:, 2] / b[:, 0]
            ax.plot(baseline, t / baseline, markers[k], ms=8, label=k)
        ax.legend()

        py.title("Comparison of CPU and IO workload methods")
        py.xlabel("Time per iteration (s)")
        py.ylabel("Number of times slower compared to doing no IO")
        py.legend()
        name = "_".join(sorted(keys)).replace(" ", "-")
        py.savefig(f"images/workload_{name}.png")
