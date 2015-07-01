from django.db import connection
from django.core.management.base import BaseCommand
from django.core.management import call_command
from optparse import make_option


class Command(BaseCommand):
    __OPTION_NAME_DEFAULT_MAIL = 'email'
    __OPTION_NAME_DEFAULT_PW = 'password'
    __OPTION_NAME_NOSYNC = 'nosync'

    help = 'Drops all database tables.'
    option_list = BaseCommand.option_list + (
        make_option('--' + __OPTION_NAME_DEFAULT_MAIL, action='store', help='Mail of user to create', default=None),
        make_option('--' + __OPTION_NAME_DEFAULT_PW, action='store', help='Password of user to create', default=None),
        make_option('--' + __OPTION_NAME_NOSYNC, action='store_true',
                    help='Option to skip calling syncdb after resetdb', default=False))

    def handle(self, *args, **options):
        cursor = connection.cursor()
        cursor.execute('SHOW TABLES')
        tables = cursor.fetchall()
        cursor.execute('START TRANSACTION; SET FOREIGN_KEY_CHECKS = 0')

        sqlCommand = "DROP TABLE IF EXISTS {}"

        print('Dropping tables...')
        counter = 0
        for table in tables:
            print('Dropping table {}'.format(table[0]))
            cursor.execute(sqlCommand.format(table[0]))
            counter += 1

        cursor.execute('SET FOREIGN_KEY_CHECKS = 1; COMMIT')
        cursor.close()
        connection.close()

        print('\nDropped {} tables'.format(counter))

        if not options[self.__OPTION_NAME_NOSYNC]:
            call_command('migrate')

        if options[self.__OPTION_NAME_DEFAULT_MAIL] and options[self.__OPTION_NAME_DEFAULT_PW]:
            call_command('createtestuser', options[self.__OPTION_NAME_DEFAULT_MAIL], options[self.__OPTION_NAME_DEFAULT_PW],
                         superuser=True, staff=True, email=options[self.__OPTION_NAME_DEFAULT_MAIL])
