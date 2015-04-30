# ------------------------------------------------------------------------------
import re

# ------------------------------------------------------------------------------
def parseStyleAttribute(value, asDict=False):
    '''Returns a list of CSS (name, value) pairs (or a dict if p_asDict is
       True), parsed from p_value, which holds the content of a HTML "style"
       tag.'''
    if asDict: res = {}
    else:      res = []
    for attr in value.split(';'):
        if not attr.strip(): continue
        name, value = attr.split(':', 1)
        if asDict: res[name.strip()] = value.strip()
        else:      res.append( (name.strip(), value.strip()) )
    return res

# ------------------------------------------------------------------------------
class CssValue:
    '''Represents a CSS value having unit "px" or "%": value and unit are
       extracted in attributes of the same name. If no unit is specified, "px"
       is assumed.'''
    # The list of CSS properties having a unit (px or %)
    withUnit = ('width', 'height')
    valueRex = re.compile('(\d+)(%|px)?')

    def __init__(self, name, value):
        if name in CssValue.withUnit:
            value, unit = CssValue.valueRex.match(value).groups()
            if not unit: unit = 'px'
            self.value = int(value)
            self.unit = unit
        else:
            self.value = value
            self.unit = None
    def __str__(self):
        res = str(self.value)
        if self.unit: res += self.unit
        return res
    def __repr__(self): return self.__str__()

class CssStyles:
    '''This class represents a set of styles collected from:
       * an HTML "style" attribute;
       * other attributes like "width".
    '''
    # The correspondance between xhtml attributes and CSS properties. within
    # CSS property names, dashes have bee removed because they are used as names
    # for Python instance attributes.
    xhtml2css = {'width': 'width', 'height': 'height', 'align': 'textalign'}

    def __init__(self, elem, attrs):
        '''Analyses styles as found in p_attrs and sets, for every found style,
           an attribute on self.'''
        # In priority, parse the "style" attribute if present
        if attrs.has_key('style'):
            styles = parseStyleAttribute(attrs['style'], asDict=True)
            for name, value in styles.iteritems():
                setattr(self, name.replace('-', ''), CssValue(name, value))
        # Parse obsolete XHTML style-related attributes if present. But they
        # will not override corresponding attributes from the "styles"
        # attributes if found.
        for xhtmlName, cssName in self.xhtml2css.iteritems():
            if not hasattr(self, cssName) and attrs.has_key(xhtmlName):
                setattr(self, cssName, CssValue(cssName, attrs[xhtmlName]))

    def __repr__(self):
        res = '<CSS'
        for name, value in self.__dict__.iteritems():
            res += ' %s:%s' % (name, value)
        return res + '>'
# ------------------------------------------------------------------------------
