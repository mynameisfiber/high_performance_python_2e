import asyncio
import random
import string
from functools import partial

from tornado.httpclient import AsyncHTTPClient

AsyncHTTPClient.configure(
    "tornado.curl_httpclient.CurlAsyncHTTPClient", max_clients=100  # <1>
)


def generate_urls(base_url, num_urls):
    for i in range(num_urls):
        yield base_url + "".join(random.sample(string.ascii_lowercase, 10))


async def run_experiment(base_url, num_iter=1000):
    http_client = AsyncHTTPClient()
    urls = generate_urls(base_url, num_iter)
    response_sum = 0
    tasks = [http_client.fetch(url) for url in urls]  # <2>
    for task in asyncio.as_completed(tasks):  # <3>
        response = await task  # <4>
        response_sum += len(response.body)
    return response_sum


if __name__ == "__main__":
    import time

    delay = 100
    num_iter = 1000
    run_func = partial(
        run_experiment,
        f"http://127.0.0.1:8080/add?name=tornado&delay={delay}&",
        num_iter,
    )

    start = time.time()
    result = asyncio.run(run_func)  # <5>
    end = time.time()
    print(f"Result: {result}, Time: {end - start}")
