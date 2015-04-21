import subprocess
import os
import saddle


class RedisService(saddle.Service):
    def __init__(self, service_engine, port=16379, needs=None):
        self.port = port
        super(RedisService, self).__init__(
            service_engine,
            name="Redis",
            command=["redis-server", "--port", str(port)],
            readysignal={
                'logline': lambda line: "The server is now ready to accept connections" in line,
            },
            needs=needs,
        )

    def cli(self, args, **kwargs):
        self.run(["redis-cli", "-p", str(self.port)] + args, **kwargs)
