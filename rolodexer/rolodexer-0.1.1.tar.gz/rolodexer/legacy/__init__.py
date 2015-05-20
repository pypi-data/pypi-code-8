
from __future__ import print_function

import re
import phonenumbers

from copy import copy
# from pprint import pprint
from rolodexer.histogram import Histogram

class RolodexerError(Exception): pass
class RDAmbiguousTerms(RolodexerError): pass
class RDAmbiguousNames(RolodexerError): pass
class RDAmbiguousNumber(RolodexerError): pass
class RDPhoneNumberError(RolodexerError): pass
class RDZipCodeError(RolodexerError): pass

# simple line assumptions
SEP     = ','
SEP_WS  = ', '
D = re.compile(r'\D+') # kill non-digits
digify = lambda term: D.subn('', term)[0]

# simple term assumptions
is_zip          = lambda term: len(digify(term)) == 5
is_phone        = lambda term: len(digify(term)) == 10
is_color        = lambda term: term.islower()

# format according to standards
def phone_format(term):
    return phonenumbers.format_number(
        phonenumbers.parse(term, 'US'),
        phonenumbers.PhoneNumberFormat)

def tokenize(line_input):
    """ basically: r"(name), (zip|phone|color),
                             (zip|phone|color),
                             (zip|phone|color)"
    """
    terms  = []
    line    = unicode(line_input)
    
    while True:
        partition   = line.rpartition(',')
        first       = partition[:-2][0].strip()
        last        = partition[-1:][0].strip()
        if not first and not last:
            break
        line = first
        terms.append(last)
    return terms

def reconstruct(terms):
    return SEP_WS.join(reversed(terms))

def classify(orig_terms):
    out = dict()
    terms = copy(orig_terms)
    
    # first, sanity-check the digified terms --
    # if more than one can pass for a phone number, a color,
    # or a zip code (that is to say, the input is ambiguous),
    # we bail:
    for term in terms:
        # check each term against all test funcs --
        # if more than one bucket is nonzero, it's a problem
        h = Histogram()
        if is_zip(term):
            h.inc('zip')
        if is_phone(term):
            h.inc('phone')
        if is_color(term):
            h.inc('color')
        if len(h) > 1:
            # ERROR: couldn't distinguish one thing
            # from another... BAIL
            raise RDAmbiguousTerms("Term '%s' parsed ambiguously\n"
                                   "Passed multiple tests: %s" % (
                                       term, SEP_WS.join(h.iterkeys())
                                   ))
    
    # next, recurse and grab the phone number and color
    # ... they are the easiest to find:
    for idx, term in enumerate(copy(terms)):
        # tref = terms[idx] # I do miss C++ sometimes
        if is_phone(term):
            out.update({ u'phonenumber': u"%s" % phone_format(term) })
            terms.remove(term)
            continue
        elif is_color(term):
            out.update({ u'color': u"%s" % term })
            terms.remove(term)
            continue
        elif is_zip(term):
            out.update({ u'zipcode': u"%s" % term })
            terms.remove(term)
            continue
    
    if not out.has_key(u'phonenumber'):
        # ERROR: NO PHONE / BAD PHONE!
        raise RDPhoneNumberError("No valid phone number in %d-term list\n"
                                 "Reconstructed original line:\n"
                                 "\t%s" % (len(terms), reconstruct(orig_terms)))
    
    if not out.has_key(u'zipcode'):
        # ERROR: NO ZIPCODE / BAD ZIPCODE!
        raise RDZipCodeError("No valid zip code in %d-term list\n"
                             "Reconstructed original line:\n"
                             "\t%s" % (len(terms), reconstruct(orig_terms)))
    
    if not out.has_key(u'color'):
        # LESS DISCONCERTING ERROR: NO COLOR / BAD COLOR!
        pass
    
    # what is left "should" be the pieces of the name,
    # e.g. ['Washington', 'Booker T.'], ['James Murphy'], &c
    if len(terms) > 2:
        # ERROR: wtf is going on
        pass
    elif len(terms) == 2:
        out.update({ 
            u'firstname':    u"%s" % terms[-1],
            u'lastname':     u"%s" % terms[0]
        })
    elif len(terms) == 1:
        names = terms[0].split()
        if len(names) > 1:
            out.update({
                u'firstname':    u"%s" % names[0],
                u'lastname':     u"%s" % names[-1]
            })
        else:
            # ERROR: only one name -- `raise MadonnaError()` ?
            # ... use it as the *last* name for now, maybe
            # ... naw, f that: ERROR.
            raise RDAmbiguousNames("Only one name present: '%s'\n"
                                   "Reconstructed original line:\n"
                                   "\t%s" % (names.pop(), reconstruct(orig_terms)))
        
    else:
        # WHY ARE WE HERE. No names... really??
        raise RDAmbiguousNames("No names present!"
                               "Reconstructed original line:\n"
                               "\t%s" % reconstruct(orig_terms))
        
    # pprint(out, indent=4)
    return out
