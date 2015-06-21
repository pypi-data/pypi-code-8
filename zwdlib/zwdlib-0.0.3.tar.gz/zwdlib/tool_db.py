# encoding: utf-8
'''
Created on 2014-7-18

@author: Winston Zhong
'''
import datetime
import os
import re
import sqlite3
import time

samples =[ '''
CREATE TABLE proxies (
    "ip_port" TEXT primary key,
    "last_time" INTEGER,
    "type" TEXT DEFAULT ('http'),
''',
'''
CREATE TABLE "table_with_pk" (
    "pk" INTEGER PRIMARY KEY,
    "f1" TEXT,
    "f2" TEXT
)
''',
'''
CREATE TABLE proxies (
    "ip_port" TEXT primary key,
    "last_time" INTEGER,
    "type" TEXT DEFAULT ('http'),
    "ok" INTEGER DEFAULT (0),
    "failed" INTEGER DEFAULT (0),
    "rate" REAL DEFAULT (0)
    , "is_anonymous" INTEGER   DEFAULT (0))

''',
    '''
    CREATE TABLE "think_articletrainingrecord" (
        "id" integer NOT NULL PRIMARY KEY,
        "article_id" integer NOT NULL REFERENCES "think_articlerecord" ("id"),
        "html" text,
        "json_data" text,
        "created_time" datetime NOT NULL,
        "modified_time" datetime NOT NULL,
        "is_title" bool NOT NULL,
        "is_content" bool NOT NULL,
        "is_date" bool NOT NULL
    )
    '''

]


ptn_table_dict = re.compile('^[\s,]+"(\w+)"', re.MULTILINE)
ptn_table_name = re.compile('CREATE TABLE\s+"?(.+?)"?\s+\(', re.IGNORECASE)
ptn_primary_key = re.compile('"(\w+)"\s*.*?\s+primary\s+key', re.IGNORECASE)

def get_primary_key(table_description):
    '''
    Return primary key from table description
    >>> get_primary_key(samples[0])
    'ip_port'
    >>> get_primary_key('')
    >>> get_primary_key(samples[1])
    'pk'
    >>> get_primary_key(samples[3])
    'id'
    '''
    m = ptn_primary_key.search(table_description)
    if m:
        return ptn_primary_key.search(table_description).groups()[0]
    

def get_table_name(table_description):
    '''
    Return table name from description
    >>> get_table_name(samples[0])
    'proxies'
    >>> get_table_name('')# doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    AttributeError: 'NoneType' object has no attribute 'groups'
    >>> get_table_name('CREATE TABLE "table_without_pk" (')
    'table_without_pk'
    '''
    return ptn_table_name.search(table_description).groups()[0]

def get_table_dict(table_description):
    '''
    Return table field dictionary from description
    >>> a = get_table_dict(samples[0])
    >>> len(a)
    3
    >>> a.get('ip_port')

    >>> a['ip'] # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    KeyError: message
    >>> a = get_table_dict(samples[1])
    >>> len(a)
    3
    >>> a = get_table_dict(samples[2])
    >>> len(a)
    7
    '''
    return dict([(x,None) for x in ptn_table_dict.findall(table_description)])

def get_table_fields(table_description):
    return get_table_dict(table_description).keys()


class NoSuchFieldError(Exception):
    pass
class BaseDatabase(object):
    def connect(self):
        return sqlite3.connect(self.db_path, timeout=24*3600)
    
    def get_time_string(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", 
              datetime.datetime.now().timetuple())

    def get_conditions(self, fields, record_dict):
        '''
        >>> BaseDatabase().get_conditions(['pk','f1','f2','f3'], {'pk':1, 'f1':'f1'})
        ['pk = ?', 'f1 = ?']
        >>> BaseDatabase().get_conditions(['pk','f1','f2','f3'], {'pk>':1, 'f1 like':'f%'})
        ['pk> ?', 'f1 like ?']
        >>> BaseDatabase().get_conditions(['pk','f1','f2','f3'], {'pk2>':1}) # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        NoSuchFieldError: no such field:pk2>        
        '''
        ptn = re.compile(r'^(%s)\W+' % '|'.join(fields))
        conditions = []
        for k in record_dict.keys():
            if k not in fields:
                if ptn.search(k):
                    conditions.append('%s ?' % k)
                else:
                    raise NoSuchFieldError, 'no such field:%s' % k
            else:
                conditions.append('%s = ?' % k)
        return conditions
    
    def __fetch(self, record_dict=None, fetchone=False, order_dict=None,limit=None, result_column=[]):
        keys = get_table_fields(self.__class__.__doc__)
#         c = self.conn.cursor()
        values = []
        
        result_column = result_column or keys
        
        sql = '''select %s from %s''' % (','.join(result_column) or ','.join(keys), get_table_name(self.__class__.__doc__))
        
        if record_dict:
            
            sql = '''%s where %s''' % (sql, 
                                      ' and '.join(self.get_conditions(keys, record_dict))
                                      )
            values = record_dict.values()
        
        if order_dict:
            sql = '''%s order by %s''' % (sql,
                                      ','.join(["%s %s" % (k,order_dict[k]) for k in order_dict.keys()])
                                      )

        if limit:
            sql += ' limit %s' % limit 
        
        with self.connect() as con:
            c = con.cursor()
#             print sql
            c.execute(sql, values)

            if fetchone:
                x = c.fetchone()
                if x:
                    return dict(zip(result_column, x))
            else:
                return [dict(zip(result_column, x)) for x in c.fetchall()]
    
    def fetchone(self, record_dict=None, order_dict=None,limit=None, result_column=[]):
        '''
        >>> TestTableWithOutPK().delete()
        >>> TestTableWithOutPK().insert({'pk':1, 'f1':'0abcd', 'f2':'2'})
        >>> TestTableWithOutPK().insert({'pk':2, 'f1':'1efgh', 'f2':'3'})
        >>> TestTableWithOutPK().insert({'pk':3, 'f1':'2ijkl', 'f2':'4'})
        >>> TestTableWithOutPK().count()
        3
        >>> TestTableWithOutPK().fetchone({'pk<':2}).get('pk')
        1
        >>> TestTableWithOutPK().fetchone({'f1 like':'2i%'}).get('pk')
        3
        >>> TestTableWithOutPK().fetchone({'f4 like':'2i%'}) # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        NoSuchFieldError: no such field:f4 like
        >>> TestTableWithOutPK().fetchone({'f1 like':'2i%','pk':3}).get('pk')
        3
        '''
        return self.__fetch(record_dict, fetchone=True, order_dict=order_dict,limit=limit,result_column=result_column)
    
    def fetchall(self, record_dict=None,order_dict=None,limit=None, result_column=[]):
        '''
        >>> TestTableWithPK().delete()
        >>> TestTableWithPK().upsert({'pk':1, 'f1':'0', 'f2':'2'})
        True
        >>> TestTableWithPK().upsert({'pk':2, 'f1':'1', 'f2':'3'})
        True
        >>> TestTableWithPK().upsert({'pk':3, 'f1':'1', 'f2':'4'})
        True
        >>> len(TestTableWithPK().fetchall())
        3
        >>> len(TestTableWithPK().fetchall({'pk':1}))
        1
        >>> len(TestTableWithPK().fetchall({'f1':1}))
        2
        >>> len(TestTableWithPK().fetchall({'f2':4}))
        1
        '''
        return self.__fetch(record_dict, fetchone=False, order_dict=order_dict,limit=limit,result_column=result_column)
    
    def count(self, record_dict=None):
        '''
        >>> TestTableWithPK().delete()
        >>> TestTableWithPK().count()
        0
        >>> TestTableWithPK().upsert({'pk':1, 'f1':'f1', 'f2':'f2'})
        True
        >>> TestTableWithPK().count()
        1
        >>> TestTableWithPK().insert({'pk':1, 'f1':'f1', 'f2':'f2'}) # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        IntegrityError: PRIMARY KEY must be unique
        >>> TestTableWithOutPK().delete()
        >>> TestTableWithOutPK().count()
        0
        >>> TestTableWithOutPK().insert({'pk':1, 'f1':'f1', 'f2':'f2'})
        >>> TestTableWithOutPK().count()
        1
        >>> TestTableWithOutPK().insert({'pk':1, 'f1':'f1', 'f2':'f2'})
        >>> TestTableWithOutPK().count()
        2
        '''
        return self.__fetch(record_dict, fetchone=True, result_column=['count(*)']).get('count(*)')
    
    def delete(self,record_dict=None):
        '''
        >>> TestTableWithPK().delete()
        >>> TestTableWithPK().insert({'pk':1, 'f1':'f1', 'f2':'f2'})
        >>> TestTableWithPK().insert({'pk':2, 'f1':'f1', 'f2':'f2'})
        >>> TestTableWithPK().insert({'pk':3, 'f1':'f1', 'f2':'f3'})
        >>> TestTableWithPK().insert({'pk':4, 'f1':'f1', 'f2':'f2'})
        >>> TestTableWithPK().count()
        4
        >>> TestTableWithPK().delete({'pk':1})
        >>> TestTableWithPK().count()
        3
        >>> TestTableWithPK().delete({'f2':'f2'})
        >>> TestTableWithPK().count()
        1
        >>> TestTableWithPK().delete({'pk':'3', 'f1':'f1'}) 
        >>> TestTableWithPK().count()
        0
        '''
        
        sql = '''delete from %s''' % (get_table_name(self.__class__.__doc__))
        values = []
        if record_dict:
            sql = '''%s where %s''' % (sql, 
                                      'and'.join([" %s = ? " % k for k in record_dict.keys()])
                                      )
            values = record_dict.values()
        
        with self.connect() as con:
            con.execute(sql, values)
        
    
    def __insert_or_update(self, record_dict, keys, template):
        assert len(record_dict) > 0

        sql = template % (get_table_name(self.__class__.__doc__),
                     ','.join(keys),
                     ','.join(['?']* len(keys))
                     )
#         print sql, keys
        values = [record_dict.get(k) for k in keys]
        with self.connect() as con:
            con.execute(sql,                     
                      values
                      )
    
    
    def insert(self, record_dict):
        '''
        >>> TestTableWithPK().insert({}) # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        AssertionError
        >>> TestTableWithPK().delete()
        >>> TestTableWithPK().insert({'pk':1, 'f1':'f1'})
        >>> TestTableWithPK().fetchone().get('pk')
        1
        >>> TestTableWithPK().fetchone().get('f1')
        u'f1'
        '''
        assert record_dict
        return self.__insert_or_update(record_dict, record_dict.keys(), '''INSERT INTO %s (%s)  VALUES (%s);''')
        
    
    def upsert(self, record_dict):
        '''
        >>> TestTableWithOutPK().upsert({'pk':1, 'f1':'f1_update', 'f2':'f2_update'}) # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        AssertionError
        >>> TestTableWithPK().upsert({})
        Traceback (most recent call last):
        AssertionError
        >>> TestTableWithPK().upsert({'f1':'f1_update', 'f2':'f2_update'})
        Traceback (most recent call last):
        AssertionError
        >>> TestTableWithPK().delete()
        >>> TestTableWithPK().upsert({'pk':1, 'f1':'f1_update', 'f2':'f2_update'})
        True
        >>> TestTableWithPK().upsert({'pk':1, 'f1':'f1_update'})
        False
        >>> TestTableWithPK().upsert({'pk':1, 'f1':'f1_updated_again'})
        True
        >>> TestTableWithPK().fetchone({'pk':1}).get('f1')
        u'f1_updated_again'
        >>> TestTableWithPK().fetchone({'pk':1}).get('f2')
        u'f2_update'
        >>> TestTableWithPK().count()
        1
        '''
        assert record_dict
        pk = get_primary_key(self.__class__.__doc__)
        assert pk
        assert record_dict.get(pk)
        
        keys = get_table_fields(self.__class__.__doc__)
#         print len(keys), len(record_dict.keys())
        if len(keys) != len(record_dict.keys()): #if the record_dict is not full size
            tmp = self.fetchone({pk:record_dict.get(pk)})
            if tmp: #if has that record with pk
                if not [v for k, v in record_dict.items() if v != tmp.get(k)]:
                    return False #same, should not update
                tmp.update(record_dict) #update record
                record_dict = tmp
            else:
                keys = record_dict.keys()
        
        
        template = '''INSERT OR REPLACE INTO %s (%s)  VALUES (%s);'''
        
        self.__insert_or_update(record_dict, keys, template)
        return True


if __name__ == "__main__":
    import doctest

    class TestTable(BaseDatabase):
        db_path = os.path.join(os.path.dirname(__file__), 'test.db').replace('\\','/')
    class TestTableWithPK(TestTable):
        '''
        CREATE TABLE "table_with_pk" (
            "pk" INTEGER PRIMARY KEY,
            "f1" TEXT,
            "f2" TEXT
        )
        '''
        
    class TestTableWithOutPK(TestTable):
        '''
        CREATE TABLE "table_without_pk" (
            "pk" INTEGER,
            "f1" TEXT,
            "f2" TEXT
        )
        '''
#     TestTableWithPK().upsert({'pk':1, 'f1':'f1', 'f2':'f2'})
    doctest.testmod(verbose=True, report=True)
    
    print BaseDatabase().__class__.__doc__
