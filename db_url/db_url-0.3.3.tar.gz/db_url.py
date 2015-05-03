#!/usr/bin/env python2

import os
import sys
import subprocess
import urlparse


def get_connection_command(scheme, user, database):
    """Returns the token list of the base command to connect to a database."""
    if scheme in ['postgres', 'postgresql']:
        return ['psql']
    elif scheme == 'mysql':
        return ['mysql', '-u', user, '-D', database]
    elif scheme == 'sqlite':
        return ['sqlite3', database]
    else:
        return None


def get_database_env_vars(scheme, user, password, host, port, database):
    """Returns the environment variables to set to connect to a database."""
    if scheme in ['postgres', 'postgresql']:
        env_vars = {
            'PGPASSWORD': password,
            'PGHOST': host,
            'PGDATABASE': database
        }
        if user:
            env_vars['PGUSER'] = user

        if port:
            env_vars['PGPORT'] = str(port)

        return env_vars
    elif scheme == 'mysql':
        env_vars = {
            'MYSQL_PWD': password,
            'MYSQL_HOST': host,
        }

        if port:
            env_vars['MYSQL_TCP_PORT'] = str(port)

        return env_vars
    else:
        return {}

def parse_db_url(database_url):
    """Return a base command list and list of environment variables tuples to connect to a database_url."""
    parsed_url = urlparse.urlparse(database_url)

    scheme = parsed_url.scheme
    user = parsed_url.username or ''
    password = parsed_url.password or ''
    host = parsed_url.hostname or ''
    database = parsed_url.path[1:]

    query_params = dict(urlparse.parse_qsl(parsed_url.query))
    if 'user' in query_params:
        user = query_params['user']
    if 'password' in query_params:
        password = query_params['password']

    database_command = get_connection_command(scheme, user, database)
    if not database_command:
        raise ValueError('Scheme "{}" not recognized.'.format(scheme))

    return database_command, get_database_env_vars(scheme,
                                                   user,
                                                   password,
                                                   host,
                                                   parsed_url.port,
                                                   database)


def connect_to_database():
    """Connect to the DATABASE_URL environment variable."""
    database_url = os.environ.get('DATABASE_URL', None)
    if not database_url:
        print('Error: set the DATABASE_URL environment variable')
        exit(1)

    database_url = database_url.strip('jdbc:')

    try:
        base_connection_command, env_vars = parse_db_url(database_url)
    except ValueError as e:
        print('Error: {}'.format(e))
        exit(1)

    os.environ.update(env_vars)

    command = base_connection_command + sys.argv[1:]

    try:
        subprocess.call(command)
    except OSError:
        missing_command = base_connection_command[0]
        print('Error: missing database client "{}"'.format(missing_command))
        print('Ensure the "{}" command is on your PATH'.format(missing_command))
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    connect_to_database()
