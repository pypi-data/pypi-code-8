import hashlib
from lxml import etree


# The canonical string representation of an XML element.
# This is useful to compare XML elements.
# Strings are hashable, so they are also perfect to use with difflib.
def canonical_xml_repr(elt):
    return etree.tostring(elt, method='c14n')


# Using the canonical representation of XML elements, we can define functions
# that tests XML elements for equality. **Not actually used in msdiff**
def elements_equal(e1, e2):
    return canonical_xml_repr(e1) == canonical_xml_repr(e2)

    
def elements_seq_equal(s1, s2):
    return all(elements_equal(e1, e2) for e1, e2 in zip(s1, s2))

# We can also hash the canonical representations to get
# a good hash for an element. **Not actually used in msdiff**
def hash_element(elt):
    return hashlib.sha1(canonical_xml_repr(elt)).hexdigest()
