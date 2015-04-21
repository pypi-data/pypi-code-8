import subprocess
import os
import saddle
import shutil
import subprocess
import sys

class PostgresDatabase(saddle.Fixture):
    def __init__(self, name, owner):
        self.name = name
        self.owner = owner

class PostgresUser(saddle.Fixture):
    def __init__(self, username, password):
        self.username = username
        self.password = password

class PostgresService(saddle.Service):
    def __init__(self, service_engine, port=15432, encoding='UTF-8', locale='en_US', users=None, databases=None, needs=None):
        self.encoding = encoding
        self.locale = locale
        self.port = port
        self.users = None if users is None else users
        self.databases = None if databases is None else databases
        self.pgdata = service_engine.saddledir() + os.sep + 'pgdata'
        super(PostgresService, self).__init__(
            service_engine,
            "Postgres",
            ['/usr/lib/postgresql/9.3/bin/postgres',
                '-p', str(self.port),
                '-D', self.pgdata,
                '--unix_socket_directories=' + self.pgdata,
                "--log_destination=stderr",],
            {'logline': lambda line: "database system is ready to accept connections" in line,},
            needs=needs,
        )

    def setup(self):
        sys.stdout.write("Initializing postgresql database...\n")
        shutil.rmtree(self.pgdata, ignore_errors=True)
        # TODO : Put back encoding + locale
        subprocess.Popen(["/usr/lib/postgresql/9.3/bin/initdb", self.pgdata,], stdout=sys.stdout, stderr=sys.stderr).communicate()

    def poststart(self):
        sys.stdout.write("Creating users and databases...\n")
        for user in self.users:
            self.psql("""create user {} with password '{}';""".format(user.username, user.password))
        for database in self.databases:
            self.psql("""create database {} with owner {};""".format(database.name, database.owner.username))

    def psql(self, command=None):
        """Run PSQL command."""
        fullcmd = ["psql", "-d", "template1", "-p", str(self.port), "--host", self.pgdata,]
        if command is not None:
            fullcmd = fullcmd + ["-c", command, ]
        subprocess.Popen(fullcmd, stdout=sys.stdout, stderr=sys.stderr).communicate()
    
    # TODO : Pgdump
    # TODO : Commands / postgres database
    # TODO : postgres loading fixture
