
import re
import phonenumbers

from copy import copy
# from pprint import pprint
from histogram import Histogram

SEP     = ','
SEP_WS  = ', '
D = re.compile(r'\D+')
FIELD_DMV = []

class RolodexerError(Exception): pass
class RDAmbiguousTerms(RolodexerError): pass
class RDAmbiguousNames(RolodexerError): pass
class RDAmbiguousNumber(RolodexerError): pass
class RDPhoneNumberError(RolodexerError): pass
class RDZipCodeError(RolodexerError): pass

def reconstruct(tokens):
    return SEP_WS.join(reversed(tokens))

class fieldtype(type):
    def __new__(cls, name, bases, attrs):
        # super_new bit cribbed from Django:
        super_new = super(fieldtype, cls).__new__
        # parents = [b for b in bases if isinstance(b, fieldtype)]
        newcls = super_new(cls, name, bases, attrs)
        if newcls.json_name != 'field':
            FIELD_DMV.append(newcls)
        return newcls
    
    def digify(cls, token):
        return D.subn('', token)[0]
    
    def check(cls, token):
        raise NotImplementedError()


class FieldBase(object):
    json_name = u'field'
    
    @property
    def name(self):
        return self.json_name
    
    def format(self, token):
        return u"%s" % token
    
    def value_for_token(self, token):
        return { self.name: self.format(token) }


class Field(FieldBase):
    __metaclass__ = fieldtype
    
    def unfound(self, token_list):
        pass # Specifically, do not raise here


class ZipcodeField(Field):
    json_name = 'zipcode'
    
    class __metaclass__(fieldtype):
        def check(cls, token):
            return len(cls.digify(token)) == 5
    
    def unfound(self, token_list):
        raise RDZipCodeError("No valid zip code in %d-term list\n"
                             "Reconstructed original line:\n"
                             "\t%s" % (len(token_list), reconstruct(token_list)))


class ColorField(Field):
    
    json_name = 'color'
    
    class __metaclass__(fieldtype):
        def check(cls, token):
            return token.islower()


class PhoneNumberField(Field):
    json_name = 'phonenumber'
    
    class __metaclass__(fieldtype):
        def check(cls, token):
            return len(cls.digify(token)) == 10
    
    def format(self, token):
        return u"%s" % phonenumbers.format_number(
            phonenumbers.parse(token, 'US'),
            phonenumbers.PhoneNumberFormat)
    
    def unfound(self, token_list):
        raise RDPhoneNumberError("No valid phone number in %d-term list\n"
                                 "Reconstructed original line:\n"
                                 "\t%s" % (len(token_list), reconstruct(token_list)))

class NameField(FieldBase):
    def unfound(self, token_list):
        raise RDAmbiguousNames("Only one name present!\n"
                               "Reconstructed original line:\n"
                               "\t%s" % reconstruct(token_list))

class FirstNameField(NameField):
    """ Special case for first-name fields """
    json_name = u'firstname'

class LastNameField(NameField):
    """ Special case for last-name fields """
    json_name = u'lastname'


def tokenize(line_input):
    tokens  = []
    line    = unicode(line_input)
    
    while True:
        partition   = line.rpartition(',')
        first       = partition[:-2][0].strip()
        last        = partition[-1:][0].strip()
        if not first and not last:
            break
        line = first
        tokens.append(last)
    return tokens


def classify(token_list):
    out = dict()
    tokens = copy(token_list)
    
    # pprint(FIELD_DMV)
    
    # first, sanity-check the digified tokens --
    # if more than one can pass for a phone number, a color,
    # or a zip code (that is to say, the input is ambiguous),
    # we bail:
    for token in tokens:
        # check each term against all test funcs --
        # if more than one bucket is nonzero, it's a problem
        h = Histogram()
        for FieldType in FIELD_DMV:
            if FieldType.check(token):
                h.inc(FieldType.json_name)
        if len(h) > 1:
            # ERROR: couldn't distinguish one thing
            # from another... BAIL
            raise RDAmbiguousTerms("Token '%s' parsed ambiguously\n"
                                   "Passed multiple field checks: %s" % (
                                       token, SEP_WS.join(h.iterkeys())
                                   ))
    
    # update `out` with the classified tokens
    for idx, token in enumerate(copy(tokens)):
        for FieldType in FIELD_DMV:
            if FieldType.check(token):
                field = FieldType()
                out.update(field.value_for_token(token))
                tokens.remove(token)
            continue
    
    # raise appropriate errors when we don't find what we need
    for FieldType in FIELD_DMV:
        field = FieldType()
        if not out.has_key(field.name):
            field.unfound(token_list) # this may raise
    
    # what is left "should" be the pieces of the name,
    # e.g. ['Washington', 'Booker T.'], ['James Murphy'], &c
    first_field = FirstNameField()
    last_field = LastNameField()
    if len(tokens) > 2:
        # ERROR: wtf is going on
        pass
    elif len(tokens) == 2:
        out.update(first_field.value_for_token(tokens[-1]))
        out.update(last_field.value_for_token(tokens[0]))
    elif len(tokens) == 1:
        names = tokens[0].split()
        if len(names) > 1:
            out.update(first_field.value_for_token(names[0]))
            out.update(last_field.value_for_token(names[-1]))
        else:
            NameField().unfound(token_list)
    else:
        # WHY ARE WE HERE. No names... really??
        raise RDAmbiguousNames("No names present!"
                               "Reconstructed original line:\n"
                               "\t%s" % reconstruct(token_list))
    
    # pprint(out, indent=4)
    return out


