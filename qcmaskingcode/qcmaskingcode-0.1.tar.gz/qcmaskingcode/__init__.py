# -*- coding: utf-8 -*-

#  qcmaskingcode -- Quick Corp Code Generator
#
#  Copyright (c) 2011-2020  Jean Machuca  <correojean@gmail.com>
#
import random

MAX_CODE_SUPPORTED = 999900000000000000000000

def verificator(code):
    digitplace = random.randrange(str(code).__len__())
    return '%s%s' % (digitplace,str(code)[digitplace])

def checkVerificator(maskingcode):
    ret = False
    try:
        check = maskingcode.split('-')
        code = check[0]
        verificator = check[1]
        digitplace = int(verificator[:-1])
        digit = verificator[-1]
        ret = True if code[digitplace]==digit else False
    except:
        ret= False
    return ret
    

def generate(code):
    if code < MAX_CODE_SUPPORTED:
        code = '%s-%s' % (str(code),verificator(code))
        letters = [chr(i+65) for i in range(code.__len__())]
        letters.reverse()
        masking = [str(ord(c)) for c in code ]
        masking.reverse()
        newcode = ''.join([ '%s%s' % (letters[i],masking[i]) for i in range(code.__len__())  ])
        newcode = ''.join([a.replace(a,'-'+a) if a.isalpha() else a for a in newcode])[1:]
    else:
        newcode = ''
    return newcode

def revert(newcode):
    newcode = newcode.replace('-','')
    letters = [c for c in newcode if c.isalpha()]
    for l in letters:
        newcode = newcode.replace(l,'-')
    masking = [n for n in newcode.split('-') if not n.__eq__('')]
    masking.reverse()
    maskingcode = ''.join([chr(int(nm)) for nm in masking])
    return int(maskingcode.split('-')[0]) if checkVerificator(maskingcode) else -1


def generate2(code):
    code = str(code)
    v = str(reduce(lambda x,y: x+y,[int(c)+65/code.__len__() for c in code]))
    v = [vv for vv in v]
    v.reverse()
    v = ''.join(v)
    maskingcode = [chr(int(c)+65) for c in code]
    maskingcode.reverse()
    maskingcode = ''.join(maskingcode)
    newcode = '%s-%s'%(v,maskingcode)
    return newcode

def revert2(newcode):
    masking = newcode.split('-')
    v = masking[0]
    v = [vv for vv in v]
    v.reverse()
    v = ''.join(v)
    code = masking[1]
    code = [str(ord(c)-65) for c in code]
    code.reverse()
    code = ''.join(code)
    dv = str(reduce(lambda x,y: x+y,[int(c)+65/code.__len__() for c in code]))
    return int(code) if dv.__eq__(v) else -1