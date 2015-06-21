from hitchserve import Service
import subprocess
import os

class RedisService(Service):
    def __init__(self, version, redis_exec="redis-server", redis_cli="redis-cli", port=16379, **kwargs):
        self.version = version
        self.port = port
        self.redis_exec = redis_exec
        self.redis_cli = redis_cli
        kwargs['command'] = ["redis-server", "--port", str(port)]
        kwargs['log_line_ready_checker'] = lambda line: "The server is now ready to accept connections" in line
        super(RedisService, self).__init__(**kwargs)

    def setup(self):
        self.log("Checking redis version...")
        version_output = self.subcommand(self.redis_exec, "--version").run(check_output=True)
        if self.version not in version_output:
            raise RuntimeError("Redis version needed is {}, output is {}.".format(self.version, version_output))

    def cli(self, *args, **kwargs):
        cmd = [self.redis_cli, "-p", str(self.port)] + list(args)
        return self.subcommand(*cmd, **kwargs)
