from qms.MysqlHandler import MysqlHandler
import atexit


class DBManager:
    _stash = {}

    @staticmethod
    def set(pName, pHandler, pDetails):
        if pHandler == "MysqlHandler":
            print("qms.DBManager - connexion opened : "+pName+" "+pDetails['user']+'@'+pDetails['host']+':'+pDetails['password']+" using database '"+pDetails['db'])
            DBManager._stash[pName] = MysqlHandler(pDetails['host'], pDetails['user'], pDetails['password'], pDetails['db'])

    @staticmethod
    def get(pName):
        return DBManager._stash[pName]

    @staticmethod
    @atexit.register
    def dispose():
        for name in DBManager._stash:
            print('qms.DBManager - connexion closed : '+name)
            DBManager.get(name).close()