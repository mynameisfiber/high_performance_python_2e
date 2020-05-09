import json
import random
import string
import urllib.error
import urllib.parse
import urllib.request
from contextlib import closing
from itertools import cycle

import gevent
import numpy as np
import pylab as py
from gevent import monkey
from gevent.lock import Semaphore

monkey.patch_socket()


markers = cycle("h*o>Dxsp8")
linestyles = cycle(["-", ":", "--", "-."])


def generate_urls(base_url, num_urls):
    for i in range(num_urls):
        yield base_url + "".join(random.sample(string.ascii_lowercase, 10))


def download(url, semaphore):
    try:
        with semaphore, closing(urllib.request.urlopen(url)) as data:
            return data.read()
    except Exception as e:
        print("retrying: ", e)
        return download(url, semaphore)


def chunked_requests(urls, chunk_size=100):
    semaphore = Semaphore(chunk_size)
    requests = [gevent.spawn(download, u, semaphore) for u in urls]
    for response in gevent.iwait(requests):
        yield response


def run_experiment(base_url, num_iter=500, parallel_requests=100):
    urls = generate_urls(base_url, num_iter)
    response_futures = chunked_requests(urls, parallel_requests)
    response_size = sum(len(r.value) for r in response_futures)
    return response_size


if __name__ == "__main__":
    try:
        data = json.load(open("parallel_requests.json"))
    except IOError:
        import time

        delay = 100
        num_iter = 500

        data = {}
        for delay in range(50, 1000, 250):
            base_url = f"http://127.0.0.1:8080/add?name=concurrency_test&delay={delay}&"
            data[delay] = []
            for parallel_requests in range(1, num_iter, 25):
                start = time.time()
                result = run_experiment(base_url, num_iter, parallel_requests)
                t = time.time() - start
                print(f"{delay},{parallel_requests},{t}")
                data[delay].append((parallel_requests, t))

        json.dump(data, open("parallel_requests.json", "w+"))
    finally:
        py.figure()
        for delay, values in data.items():
            values = np.asarray(values)
            py.plot(
                values[:, 0],
                values[:, 1],
                label=f"{delay}ms request time",
                linestyle=next(linestyles),
                marker=next(markers),
                linewidth=4,
            )

        py.axvline(x=100, alpha=0.5, c="r")
        ax = py.gca()
        ax.set_yscale("log")

        py.xlabel("Number of concurrent downloads")
        py.ylabel("Time to download 500 concurrent files (s)")
        py.title("Finding the right number of concurrent requests")
        py.legend()

        py.savefig("images/parallel_requests.png")
