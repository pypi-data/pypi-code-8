import pymysql


class MysqlHandler:
    _lastErrNumber = False
    _lastErrMessage = ""

    def __init__(self, pHost, pUser, pPass, pDb):
        self.connexion = pymysql.connect(host=pHost, user=pUser, passwd=pPass, db=pDb)
    
    def execute(self, pQuery):
        cur = self.connexion.cursor()
        try:
            cur.execute(pQuery)
            self.connexion.commit()
        except pymysql.Error as e:
            self._lastErrNumber, self._lastErrMessage = e.args
            return False

    def last_error_number(self):
        return self._lastErrNumber

    def last_error_message(self):
        return self._lastErrMessage

    def get_result(self, query):
        result = []
        cur = self.connexion.cursor()
        cur.execute(query)
        cols = []
        for col in cur.description:
            cols.append(col[0])
        for row in cur:
            line = {}
            for k, v in zip(cols, row):
                line[k] = v
            result.append(line)
        cur.close()
        return result
    
    def close(self):
        self.connexion.close()
