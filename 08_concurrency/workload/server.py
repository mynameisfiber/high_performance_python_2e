import asyncio

from tornado import httpserver, ioloop, options, web

options.define("port", default=8080, help="Port to serve on")
response = '{{"result": "{result}", "t": 0.5}}'


class Addresult(web.RequestHandler):
    async def post(self):
        result = self.request.body
        await asyncio.sleep(0.1)
        self.write(response.format(result=result))
        self.set_header("Content-Type", "application/json")
        self.finish()


if __name__ == "__main__":
    options.parse_command_line()
    port = options.options.port

    application = web.Application([(r"/add", Addresult)])

    http_server = httpserver.HTTPServer(application)
    http_server.listen(port)
    print(("Listening on port: {}".format(port)))
    ioloop.IOLoop.instance().start()
