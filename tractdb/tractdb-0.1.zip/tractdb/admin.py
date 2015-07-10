import couchdb
import re


class TractDBAdmin(object):
    """ Supports administration of a TractDB instance.
    """

    def __init__(self, server_url, server_admin, server_password):
        """ Create an administration object for a given server, using the given admin / password.
        """
        self._server_url = server_url
        self._server_admin = server_admin
        self._server_password = server_password

    def create_user(self, account_user, account_password):
        """ Create a database.
        """
        server = couchdb.Server(self._format_server_url())

        # Our databases are defined by the user name plus the suffix '_tractdb'
        dbname = '{:s}_tractdb'.format(account_user)

        # Directly manipulate users database, since it's not meaningfully wrapped
        database_users = server['_users']
        docid_user = 'org.couchdb.user:{:s}'.format(account_user)

        # Confirm the database does not exist
        if dbname in server:
            raise Exception('Database "{:s}" already exists.'.format(dbname))

        # Confirm the user does not exist
        if docid_user in database_users:
            raise Exception('User "{:s}" already exists.'.format(account_user))

        # Create the user
        doc_created_user = {
            '_id': docid_user,
            'type': 'user',
            'name': account_user,
            'password': account_password,
            'roles': [],
        }
        database_users.save(doc_created_user)

        # Create the database
        database_created = server.create(dbname)

        # Give the user access to the database
        security_doc = database_created.security
        security_members = security_doc.get('members', {})
        security_members_names = security_members.get('names', [])
        if account_user not in security_members_names:
            security_members_names.append(account_user)
            security_members_names.sort()
            security_members['names'] = security_members_names
            security_doc['members'] = security_members
            database_created.security = security_doc

    def delete_user(self, account_user):
        """ Delete a database.
        """
        server = couchdb.Server(self._format_server_url())

        # Our databases are defined by the user name plus the suffix '_tractdb'
        dbname = '{:s}_tractdb'.format(account_user)

        # Directly manipulate users database, since it's not meaningfully wrapped
        database_users = server['_users']
        docid_user = 'org.couchdb.user:{:s}'.format(account_user)

        # Confirm the database exists
        if dbname not in server:
            raise Exception('Database "{:s}" does not exist.'.format(dbname))

        # Confirm the user exists
        if docid_user not in database_users:
            raise Exception('User "{:s}" does not exist.'.format(account_user))

        # Delete them
        server.delete(dbname)
        doc_user = database_users[docid_user]
        database_users.delete(doc_user)

    def list_users(self):
        """ List our users.
        """
        couchdb_users = self._list_couchdb_users()
        couchdb_databases = self._list_couchdb_databases()

        # Keep only users who have a corresponding database
        users = []
        for user_current in couchdb_users:
            # Our databases are defined by the user name plus the suffix '_tractdb'
            dbname = '{:s}_tractdb'.format(user_current)

            if dbname in couchdb_databases:
                users.append(user_current)

        return users

    def _format_server_url(self):
        """ Format the base URL we use for connecting to the server.
        """
        return 'https://{:s}:{:s}@{:s}'.format(self._server_admin, self._server_password, self._server_url)

    def _list_couchdb_databases(self):
        """ List what CouchDB databases exist.
        """
        server = couchdb.Server(self._format_server_url())

        # Our databases are defined by the user name plus the suffix '_tractdb'
        pattern = re.compile('.*_tractdb')
        dbnames = [dbname for dbname in server if pattern.match(dbname)]

        return dbnames

    def _list_couchdb_users(self):
        """ List what CouchDB users exist.
        """
        server = couchdb.Server(self._format_server_url())

        # Directly manipulate users database, since it's not meaningfully wrapped
        database_users = server['_users']

        # This is our docid pattern
        pattern = re.compile('org\.couchdb\.user:(.*)')

        # Keep only the users that match our pattern, extracting the user
        users = []
        for docid in database_users:
            match = pattern.match(docid)
            if match:
                account_user = match.group(1)
                users.append(account_user)

        return users
