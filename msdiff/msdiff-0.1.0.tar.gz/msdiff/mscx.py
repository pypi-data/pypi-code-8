# # Introduction

# # Imports

# Standard Library
from fractions import Fraction

# External Package
from lxml import etree

# Internal Module
from mscxtags import problematic_spanners, problematic_invisible, \
  simple_colorable_tags

# # Coloring Elements

# We accept tuples with either 3 or 4 elements.
# Test mathjax: $a^2 + b^2 = c^2$
def set_color(elt, color, index=0):
    try:
        red, green, blue, alpha = color
    except:
        red, green, blue = color
        alpha = 255

    color_elt = elt.find('color')
    if color_elt is None:
        color_elt = etree.Element('color')
        elt.insert(index, color_elt)

    color_elt.set('r', str(red))
    color_elt.set('g', str(green))
    color_elt.set('b', str(blue))
    color_elt.set('a', str(alpha))


# Some elements need to have both the <color> and <foregroundColor>
# subelements for their color to be set correctly.
def set_foregroundColor(elt, color, index=0):
    try:
        red, green, blue, alpha = color
    except:
        red, green, blue = color
        alpha = 255

    foregroundColor_elt = elt.find('foregroundColor')
    if foregroundColor_elt is None:
        foregroundColor_elt = etree.Element('foregroundColor')
        foregroundColor_elt.tail = best_xml_tail(elt)
        elt.insert(index, foregroundColor_elt)

    foregroundColor_elt.set('r', str(red))
    foregroundColor_elt.set('g', str(green))
    foregroundColor_elt.set('b', str(blue))
    foregroundColor_elt.set('a', str(alpha))

    return None

# # Nudging Elements

# Nudge an element vertically.
# As in musescore, a negative offset points up.
def nudge_element(elt, extra_y_offset=-3):
    pos = elt.find('pos')
    if pos is None:
        pos = etree.Element('pos')
        pos.set('x', '0')
        pos.set('y', '0')
        elt.insert(0, pos)

    original_y_offset = float(pos.get('y'))
    pos.set('y', str(original_y_offset + extra_y_offset))


def nudge_subelements(elt, tags, extra_y_offset=-3):
    for e in elt.iter(tags):
        if e.find('color') is None:
            e.getparent().remove(e)
        else:
            nudge_element(e, extra_y_offset)

# # Control Visibility

def make_measures_invisible(array, bounds):
    kmin, kmax, lmin, lmax = bounds
    for k in xrange(kmin, kmax):
        for l in xrange(lmin, lmax):
            make_measure_invisible(array[k, l])


def set_measures_color(vec, bounds, color):
    kmin, kmax, lmin, lmax = bounds
    for k in xrange(kmin, kmax):
        for l in xrange(lmin, lmax):
            color_subelements(vec[k, l], color)


#  This function has to handle a lot of cases, depending on the element
# to be colored, because their representations in the `.mscx` file seem
# to be somewhat inconsistent.
#
#  I don't think I'll be able to be able to color the beams
# or hooks, so it's better to leave the stems black,
# at least for now
def color_element(elt, color, recursive=False):
    if elt.tag in simple_colorable_tags:
        set_color(elt, color)

    elif elt.tag == 'Fingering':
        try:
            style = elt.find('style')
            set_color(elt, color, elt.index(style))
            set_foregroundColor(elt, color, elt.index(style) + 1)
        except:
            set_foregroundColor(elt, color)
            set_color(elt, color)
    
    elif elt.tag == 'Tempo':
        set_color(elt, color)
        set_foregroundColor(elt, color)

    elif elt.tag == 'RehearsalMark':
        set_foregroundColor(elt, color)
        set_color(elt, color)

    elif elt.tag == 'Marker':
        style = elt.find('style')
        set_color(elt, color, elt.index(style))
        set_foregroundColor(elt, color, elt.index(style) + 1)

    elif elt.tag == 'Jump':
        style = elt.find('style')
        set_color(elt, color, elt.index(style))
        set_foregroundColor(elt, color, elt.index(style) + 1)
    
    elif elt.tag == 'Slur':
        if elt.find('SlurSegment') is not None:
            set_color(elt, color, 0)
            set_color(elt.find('SlurSegment'), color)

        elif elt.get('type') is None:
            set_color(elt, color)
            slur_segment = etree.Element('SlurSegment')
            #slur_segment.tail = best_xml_tail(elt)
            set_color(slur_segment, color)
            elt.insert(1, slur_segment)

    elif elt.tag == 'Tie':
        if elt.find('SlurSegment') is not None:
            set_color(elt, color, 0)
            set_color(elt.find('SlurSegment'), color)

        else:
            set_color(elt, color)
            slur_segment = etree.Element('SlurSegment')
            #slur_segment.tail = best_xml_tail(elt)
            set_color(slur_segment, color)
            elt.insert(0, slur_segment)
    
    if recursive:
        color_subelements(elt, color)


def color_subelements(elt, color):
    for e in elt.iter():
        color_element(e, color)
    

def make_staff(children):
    staff = etree.Element('Staff')
    staff.extend(children)
    return staff


def clean_element(elt, recursive=True):
    if elt.get('id') is not None:
        elt.set('id', '0')
    if elt.get('number') is not None:
        elt.set('number', '0')
    if elt.tag == 'lid':
        elt.text = '0'
    if elt.tag == 'Tuplet':
        elt.text = '0'
    if recursive:
        # Removing these is controversial, but some of these elements
        # change unpredictably between saves (o1, o2, o3, o4, pos and tick),
        # and the TimeSig might change if a segment of measures in a different
        # timesig is inserted before.
        #
        # Maybe a better option would be to clean the attributes of the
        # o1, o2, o3 and o4 elements...
        for e in elt.iter('o1', 'o2', 'o3', 'o4', 'pos', 'tick', 'TimeSig'):
            e.getparent().remove(e)
        # Barlines marked 'end' are removed because they are usually in
        # the last measure and the last measure changes often, which would
        # mean it would be needlessly highlighted.
        #  TODO: fix this in a better way
        for e in elt.iter('BarLine'):
            if e.find('subtype').text == 'end':
                e.getparent().remove(e)
        for e in elt.iter():
            clean_element(e, recursive=False)
    return elt


def get_measure_lengths(score):
    division = int(score.find('Division').text)

    upper_staff = score.find('Staff')
    measures = upper_staff.findall('Measure')
    current_sigN = None
    current_sigD = None

    in_ticks = []
    in_fracts = []

    # Reads the measures one by one, and storing the either:
    #  1) the measure length, stored as the `len` attribute
    #     of the `Measure` element. 
    #
    #  2) the Time Signature currently in scope.
    #
    # I think musescore handling of time signatures and lengths is
    # simple enough for this to work.
    for index, measure in enumerate(measures):
        timesig = measure.find('TimeSig')
        if timesig is not None:
            current_sigN = int(timesig.find('sigN').text)
            current_sigD = int(timesig.find('sigD').text)

        measure_len = measure.get('len')
        if measure_len is None:
            in_ticks.append(division * 4 * current_sigN / current_sigD)
            in_fracts.append((current_sigN, current_sigD))
        else:
            frac = Fraction(measure_len)
            length_in_ticks = int(frac * 4 * division)
            in_ticks.append(length_in_ticks)
            in_fracts.append((frac.numerator, frac.denominator))

    return in_ticks, in_fracts


# Set the visibility of an element.
# - `True` = `1` = visible
# - `False` = `2` = invisible
def set_visibility(elt, value, index=0):
    if value:
        val = "1"
    # else, if `val` is either `False`, `None` or `0`
    else:
        val = "0"

    visible = elt.find('visibility')
    try:
        visible.text = val
    except:
        visible = etree.Element('visible')
        visible.text = val
        elt.insert(index, visible)


# Makes a whole measure and its contents invisible.
# This includes making the staff lines disappear.
def make_measure_invisible(measure):
    for elt in measure.iter('Marker', 'Tie'):
        set_visibility(elt, 0)

    for elt in measure.iter(problematic_invisible):
        elt.getparent().remove(elt)

    barline = etree.Element('BarLine')
    subtype = etree.Element('subtype')
    subtype.text = 'normal'
    span = etree.Element('span')
    span.text = '1'

    barline.extend([subtype, span])
    set_visibility(barline, 0, 2)

    measure.append(barline)
    set_visibility(measure, 0)

