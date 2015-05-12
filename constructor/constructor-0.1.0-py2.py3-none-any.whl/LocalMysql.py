import os

class LocalMysql(object):
    
    def __init__(self, instance, password):
        self.instance = instance
        self.password = password
        
    def create_db(self, dbname):
        self.run_sql(
           "CREATE DATABASE \\`" + dbname + "\\` DEFAULT CHARACTER SET \\`utf8\\`;"
        )
    
    def create_user(self, username, password):
        self.run_sql(
            "CREATE USER " + username + "@localhost IDENTIFIED BY \\\"" + password + "\\\";"
        )
        
    def grant_full_db_access(self, dbname, username):
        self.run_sql(
            "GRANT CREATE ROUTINE, CREATE VIEW, ALTER, SHOW VIEW, CREATE, ALTER ROUTINE, " +
            "EVENT, INSERT, SELECT, DELETE, TRIGGER, GRANT OPTION, REFERENCES, UPDATE, DROP, " +
            "EXECUTE, LOCK TABLES, CREATE TEMPORARY TABLES, INDEX ON " + dbname + ".* TO " + username + "@localhost;"
        )
    
    def create_db_with_user(self, dbname, username, password):
        self.create_db(dbname)
        self.create_user(username, password)
        self.grant_full_db_access(dbname, username)
    
    def run_sql_file(self, dbname, sqlfile):
        scriptname = os.path.basename(sqlfile)
        self.instance.upload_file(sqlfile, destination = '~/' + scriptname)
        self.instance.run_command(
            'mysql -u root -p' + self.password + ' ' + dbname + ' < ~/' + scriptname
        )
        self.instance.run_command('rm ~/' + scriptname)
        
    def run_sql(self, sql):
        self.instance.run_command(
            'echo "' + sql + '" | mysql -u root -p' + self.password
        )