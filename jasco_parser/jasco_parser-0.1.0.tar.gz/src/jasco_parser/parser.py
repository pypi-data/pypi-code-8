class JASCOParser(object):
    def parse(self, iterable, delimiter=None, translater=float):
        d = []
        datamode = False
        for r in iterable:
            r = r.strip()
            c = r.split(delimiter)
            if datamode and (len(r) == 0 or c[0] == ''):
                break
            if datamode:
                d.append([translater(x) for x in c])
            elif c[0] == 'XYDATA':
                datamode = True
        return d

    def load(self, filename, delimiter=None, translater=float):
        if filename.lower().endswith('.csv') and not delimiter:
            delimiter = ','
        with open(filename, 'r') as fi:
            return self.parse(fi, delimiter, translater)
