from qms.DBManager import DBManager
import re

class Query:
    EQUAL = " = "
    
    NOT_EQUAL = " != "
    
    LIKE = " LIKE "
    
    UPPER = " > "
    
    UPPER_EQUAL = " >= "
    
    LOWER = " < "
    
    LOWER_EQUAL = " <= "
    
    IS = " IS "
    
    IS_NOT = " IS NOT "
    
    JOIN = " JOIN "
    
    JOIN_NATURAL = " NATURAL JOIN "
    
    JOIN_INNER = " INNER JOIN "
    
    JOIN_OUTER_FULL = " FULL OUTER JOIN "
    
    JOIN_OUTER_LEFT = " LEFT OUTER JOIN "
    
    JOIN_OUTER_RIGHT = " RIGHT OUTER JOIN "
    
    IN = " IN "
    
    MATCH = " MATCH "

    @staticmethod
    def execute(query, handler):
        if isinstance(query, str) is False:
            return False

        handler = DBManager.get(handler)
        if handler is False:
            return False

        rexp = re.compile('^(select|show|describe|explain)', re.IGNORECASE)
        if rexp.match(query) is None:
            return handler.execute(query)
        else:
            return handler.get_result(query)

    @staticmethod
    def select(pFields, pTable):
        return QuerySelect(pFields, pTable)

    @staticmethod
    def insert(values):
        return QueryInsert(values, QueryInsert.UNIQUE)

    @staticmethod
    def insert_multiple(values):
        return QueryInsert(values, QueryInsert.MULTIPLE)

    @staticmethod
    def condition():
        return QueryCondition()

    @staticmethod
    def get_error_message(handler='default'):
        return DBManager.get(handler).last_error_message()

    @staticmethod
    def get_error_number(handler='default'):
        return DBManager.get(handler).last_error_number()

    specials = ['NULL', 'NOW()']

    @staticmethod
    def escape_value(value, escape=True):
        if escape is False:
            return value
        value = str(value)
        try:
            Query.specials.index(value.upper())
            return value.upper()
        except ValueError:
            return "'"+Query.addslashes(value)+"'"

    @staticmethod
    def addslashes(s):
        l = ["\\", '"', "'", "\0", ]
        for i in l:
            if i in s:
                s = s.replace(i, '\\'+i)
        return s



class QueryCondition():
    _and = []
    _or = []
    _havingAnd = []
    _havingOr = []
    _order = ''
    _limit = ''
    _group = ''

    def __init__(self):
        self._and = []
        self._or = []
        self._havingAnd = []
        self._havingOr = []
        self._order = ''
        self._limit = ''
        self._group = ''
    
    def andCondition(self, pCondition):
        print(" AND : "+pCondition.get())
        return self
    
    def orCondition(self, pCondition):
        print(" OR : "+pCondition.get())
        return self

    def andWhere(self, pField, pOperator, value, pEscape = True):
        if pEscape:
            value = Query.escape_value(value)
        self._and.append(pField+pOperator+value)
        return self
    
    def orWhere(self, pField, pOperator, value, pEscape = True):
        if pEscape:
            value = Query.escape_value(value)
        self._or.append(pField+pOperator+value)
        return self
    
    def order(self, pField, pType='ASC'):
        if self._order == '':
            self._order = ' ORDER BY '+pField+' '+pType
        else:
            self._order += ', '+pField+' '+pType
        return self
    
    def limit(self, pFirst, pNumber):
        self._limit = ' LIMIT '+str(pFirst)+','+str(pNumber)
        return self
    
    def groupBy(self, pField):
        self._group = ' GROUP BY '+pField
        return self
    
    def get(self):
        return self.getWhere()+self._group+self._order+self._limit
    
    def getWhere(self):
        where = ""
        _and = " AND ".join(self._and)
        _or = " OR ".join(self._or)
        if _and != "":
            where = " WHERE "+_and
        if _or != "":
            if _and != "":
                where += " OR "+_or
            else:
                where += " WHERE "+_or
        return where
    

class BaseQuery:
    def __init__(self, pTable):
        self.table = pTable
        self._condition = None

    def execute(self, pHandler = 'default'):
        return Query.execute(self.get(), pHandler)

    def get(self):
        raise "La méthode 'get' doit être surchargée."


class QueryInsert(BaseQuery):

    UNIQUE = "UNIQUE"
    MULTIPLE = "MULTIPLE"

    _fields = ""
    _values = []

    def __init__(self, values, query_type):
        super(self.__class__, self).__init__("")
        if query_type == QueryInsert.UNIQUE:
            self.set_fields(values)
            self.set_values([values])
        elif query_type == QueryInsert.MULTIPLE:
            self.set_fields(values[0])
            self.set_values(values)

    def set_fields(self, data):
        self._fields = "("+", ".join(data.keys())+")"

    def set_values(self, data):
        self._values = []
        for tuple in data:
            tuple = map(Query.escape_value, list(tuple.values()))
            self._values.append("("+", ".join(tuple)+")")

    def into(self, table):
        self.table = table
        return self

    def get(self):
        values = ", ".join(self._values)
        return "INSERT INTO "+self.table+" "+self._fields+" VALUES "+values+";"

class QueryWithCondition(BaseQuery):
    _condition = None
    def andWhere(self, pField, pOperator, pValue, pEscape = True):
        self._getCondition().andWhere(pField, pOperator, pValue, pEscape)
        return self
    
    def orWhere(self, pField, pOperator, pValue, pEscape = True):
        self._getCondition().orWhere(pField, pOperator, pValue, pEscape)
        return self
    
    def limit(self, pFirst, pNumber):
        self._getCondition().limit(pFirst, pNumber)
        return self

    def setCondition(self, condition):
        self._condition = condition
        return self

    def _getCondition(self):
        if self._condition == None:
            self._condition = Query.condition()
        return self._condition
    
    

class QuerySelect(QueryWithCondition):
    def __init__(self, pFields, pTable):
        BaseQuery.__init__(self, pTable)
        self.fields = pFields
    
    def get(self):
        return 'SELECT '+self.fields+' FROM '+self.table+self._getCondition().get()+';'
