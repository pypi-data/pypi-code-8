__author__ = 'Stephan Conrad <stephan@conrad.pics>'

_ARRAY_TYES = (
    'memberOf',
)

def parseRecord(lines, accountType = "805306368"):
    if type(lines) == list:
        parse = False
        record = 0
        recs = []
        tmp = {}
        for line in lines:
            line = line.strip()
            if line.startswith("# record"):
                num = line.replace('# record', '').strip()
                parse = True
            if line == '':
                parse = False
            if parse:
                a = line.split(":")
                if len(a) >= 2:
                    key = a[0]
                    value = ("".join(a[1:])).strip()
                    if key in tmp:
                        if type(tmp[key]) == list:
                            tmp[key].append(value)
                        else:
                            tmp[key] = [tmp[key]]
                    else:
                        tmp[key] = value
            else:
                if tmp != {}:
                    if 'sAMAccountType' in tmp:
                        checkKey = accountType
                        if accountType == False:
                            checkKey = tmp['sAMAccountType']
                        if tmp['sAMAccountType'] == checkKey:
                            user=False
                            if 'isCriticalSystemObject' in tmp:
                                user = tmp['isCriticalSystemObject'].lower() in 'false'
                            else:
                                user = True
                            if user:
                                tmp["systemUser"] = False
                            else:
                                tmp["systemUser"] = True
                            recs.append(tmp)
                    elif accountType == False:
                        recs.append(tmp)
                tmp = {}
        return recs

