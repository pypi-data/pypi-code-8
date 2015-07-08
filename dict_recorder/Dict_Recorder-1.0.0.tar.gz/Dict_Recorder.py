####################################################################
# save in-memory database object to a file with custom formatting;
# assume 'endrec.', 'enddb.', and '=>' are not used in the data; 
# assume db is dict of dict;  warning: eval can be dangerous - it
# runs strings as code;  could also eval() record dict all at once
####################################################################

dbfilename = 'people-file'
ENDDB  = 'enddb.'
ENDREC = 'endrec.'
RECSEP = '=>'

def storeDbase(db, dbfilename=dbfilename):
    "formatted dump of database to flat file"
    dbfile = open(dbfilename, 'w')
    for key in db:
        print >> dbfile, key
        for (name, value) in db[key].items():
            print >> dbfile, name + RECSEP + repr(value)
        print >> dbfile, ENDREC
    print >> dbfile, ENDDB
    dbfile.close()

def loadDbase(dbfilename=dbfilename):
    "parse data to reconstruct database"
    dbfile = open(dbfilename)
    import sys
    sys.stdin = dbfile
    db = {}
    key = raw_input()
    while key != ENDDB:
        rec = {}
        field = raw_input()
        while field != ENDREC:
            name, value = field.split(RECSEP)
            rec[name] = eval(value)
            field = raw_input()
        db[key] = rec
        key = raw_input()
    return db            

if __name__ == '__main__':
    from initdata import db
    storeDbase(db)
