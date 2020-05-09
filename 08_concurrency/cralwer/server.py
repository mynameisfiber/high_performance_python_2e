import json
import time
from collections import defaultdict

from tornado import gen, httpserver, ioloop, options, web

options.define("port", default=8080, help="Port to serve on")


class AddMetric(web.RequestHandler):
    metric_data = defaultdict(list)

    async def get(self):
        if self.get_argument("flush", False):
            json.dump(self.metric_data, open("metric_data.json", "w+"))
        else:
            name = self.get_argument("name")
            try:
                delay = int(self.get_argument("delay", 1024))
            except ValueError:
                raise web.HTTPError(400, reason="Invalid value for delay")

            start = time.time()
            await gen.sleep(delay / 1000.0)
            self.write(".")
            self.finish()
            end = time.time()
            self.metric_data[name].append(
                {"start": start, "end": end, "dt": end - start}
            )


if __name__ == "__main__":
    options.parse_command_line()
    port = options.options.port

    application = web.Application([(r"/add", AddMetric)])

    http_server = httpserver.HTTPServer(application)
    http_server.listen(port)
    print(("Listening on port: {}".format(port)))
    ioloop.IOLoop.instance().start()
