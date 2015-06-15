# # Imports

# Standard Library:
import copy
import difflib
import hashlib
import itertools
import StringIO

# External Packages:
from lxml import etree
import numpy as np

# Internal Modules
from xmlutils import canonical_xml_repr

from mscx import make_staff, color_element, make_measures_invisible, \
  set_measures_color, nudge_subelements, set_visibility, clean_element, \
  get_measure_lengths

from mscxtags import problematic_spanners

# # Making the diffs
#
# Our ultimate goal is to be able to diff musescore files.
#
# Musescore files are ordinary XML files, and are hierarchical. \
# Without taking linked parts into account, the structure of the file is the \
# following:
# - A *file* contains a *score*
# - A *score* contains one or more *staves*
# - A *staff* contains one or more *measures*
# - A *measure* contains one or more *elements*
#
# Musescore also forces all *staves* to have the same number of *measures*,
# and simultaneous measures to have the same duration, unlike \
# [LilyPond](http://lilypond.org) for example.
#
# As inconvenient as this might be (it disallows polyrhythms withour some hacks), \
# it allows us to use the *group of simultaneous measures* as the fundamental \
# unit of the score.
#
# We will have 

# # Diff of *files*

# # Diff of *scores*

def diff_scores(old_score, new_score):
    old_staves = old_score.findall('Staff')
    new_staves = new_score.findall('Staff')

    staff_groups_map = get_staff_groups(old_score, new_score)

    # old_timesigs are not actually Time Signatures, but it is \
    # shorter than `old_durations_in_fract`, so it will be kept.
    old_durations, old_timesigs = get_measure_lengths(old_score)
    new_durations, new_timesigs = get_measure_lengths(new_score)

    diff = diff_staves((old_staves, new_staves),
                       (old_durations, new_durations),
                       (old_timesigs, new_timesigs),
                       staff_groups_map)

    nr_of_old_staves = len(old_staves)

    old_measures_ = diff[:, :nr_of_old_staves]
    new_measures_ = diff[:, nr_of_old_staves:]

    # Use `numpy.ndarray`'s usefull transpose method \
    # 
    old_staves_ = map(make_staff, old_measures_.T[:])
    new_staves_ = map(make_staff, new_measures_.T[:])

    return make_score_diff((old_score, new_score),
                           (old_staves_, new_staves_))

def make_score_diff(scores, staves):

    old_score, new_score = scores
    old_staves, new_staves = staves

    # We will use 'score_new' as the base
    score_diff = copy.deepcopy(new_score)

    score_diff.find('showInvisible').text = "0"
    # Don't show unprintable objects because otherwise the
    # <vspacerDown> we will insert below would clutter the score.
    score_diff.find('showUnprintable').text = "0"

    # Force continuous view (instead of page view)
    # The user can override this when the score is opened.
    layoutMode = score_diff.find('layoutMode')
    if layoutMode is None:
        layoutMode = etree.Element('layoutMode')
    layoutMode.text = 'line'

    # ---------------------------------
    # Deal with (some) ids of 'score_new'
    # ---------------------------------
    #  We have to add an offset to the ids of some
    # elements in the stavess of 'score_new' so that
    # they don't clash

    # Collect the ids of all elements in the old score
    ids = old_score.xpath('//@id')
    # Don't forget the ids are strings!
    max_id = max(map(int, ids))
    id_offset = max_id + 1
    # With this offset we garantee that there won't be clashes between
    # the elements of the old and new staves.

    # 1 track per voice * 4 potential voices for each staff = number of tracks
    #  (some tracks may be empty)
    track_number_offset = 4 * len(old_staves)

    # Now add this offset to the problematic elements of the new staves.
    # Those are spanners or spanner-like structures that are terminated
    # by an <endSpanner id="id">, where the id must match the id of the
    # element. If we have repeated ids there can be problems in the score.
    for staff in new_staves:
        for elt in staff.iter(problematic_spanners):
            old_id = int(elt.get('id'))
            elt.set('id', str(old_id + id_offset))

    for staff in new_staves:
        for track in staff.iter('track'):
            old_track_number = int(track.text)
            track.text = str(old_track_number + track_number_offset)

    #  Add vertical spacing between the old staves and the new ones;
    #  We do this by adding vertical spacers to the measures of the last
    # staff of the old score.
    old_last_staff = old_staves[-1]
    for measure in old_last_staff.iter('Measure'):
        vspacerDown = etree.Element('vspacerDown')
        # The value of 13 is a compromise between wasting a lot of screen
        # space and ensuring enough separation between the groups of staves
        vspacerDown.text = '13'
        measure.insert(0, vspacerDown)

    #  Some elements that are placed on top of all staves must be nudged
    # vertically so that they don't clash with the former versions of themselves.
    #  A better soluction may be used in the future
    # (for example, only nudge elements that change between scores)
    for staff in old_staves:
        nudge_subelements(staff, ['Tempo', 'Jump', 'RehearsalMark'])

    # ----------------------------------
    #   Merge the 2 score
    # ----------------------------------
    # For this we need to:
    #   1) Handle the Parts
    #   2) Merge the Stavess
    #
    # The process is identical and has been abstracted into
    # a single function that selects the correct elements by tag.

    # Handle Staves:

    nr_of_staves = len(old_staves)
    first_staff = score_diff.find('Staff')
    first_staff_index = score_diff.index(first_staff)
    for staff in score_diff.findall('Staff'):
        score_diff.remove(staff)
    # Insert from the end and not from the beginning!
    # Each item we insert pushes the others forward.
    for staff in reversed(old_staves + new_staves):
        score_diff.insert(first_staff_index, staff)
    # Change the ids according to the new order of the parts
    for index, elt in enumerate(score_diff.findall('Staff')):
        elt.set('id', str(index + 1))

    #  Handle Parts:
    new_parts = score_diff.findall('Part')
    old_parts = old_score.findall('Part')

    nr_of_parts = len(old_parts)

    first_part = score_diff.find('Part')
    first_part_index = score_diff.index(first_part)
    # Insert from the end and not from the beginning!
    # Each item we insert pushes the others forward.
    for part in reversed(old_parts):
        score_diff.insert(first_staff_index, part)
    # Change the ids according to the new order of the parts
    for index, part in enumerate(new_parts):
        part.set('id', str(index + 1))
        for staff in part.iter('Staff'):
            staff_id = int(staff.get('id'))
            staff.set('id', str(staff_id + nr_of_staves))

    return score_diff


# # Diff of *staves* 
#
# Essentially, this is just a thin wrapper around the function `diff_measures`

# # Diff of *measures*







def diff_files(fname_old, fname_new, fname_diff):
    # Parse the files we want to diff into `etree.ElementTree`s
    old_doc = etree.parse(fname_old)
    new_doc = etree.parse(fname_new)
    # Create a new Musescore `ElementTree` to serve as the base
    # for our diffed score. We will base this document on the
    # contents of the new file.
    doc_diff = copy.deepcopy(new_doc)

    old_score = old_doc.getroot().find('Score')
    new_score = new_doc.getroot().find('Score')

    tmp_score_diff = doc_diff.getroot().find('Score')
    score_diff = diff_scores(old_score, new_score)

    doc_diff.getroot().replace(tmp_score_diff, score_diff)

    with open(fname_diff, 'w') as f:
        f.write(etree.tostring(doc_diff, method='c14n'))



# Turns a list of staves into a matrix `M` of measures such that
# `M[k, l]` means the `k`th measure of the `l`th staff.
def transpose_staves(staves, func=lambda x: x):
    matrix = np.array([[m for m in staff if m.tag == 'Measure']
                          for staff in staves])
    flipped = [tuple(map(func, col)) for col in matrix.T]
    return flipped


RED = (200, 0, 0)
GREEN = (0, 200, 0)


_default_colors = {
    'replaced': RED, 'replaces': GREEN,
    'deleted': RED,
    'inserted': GREEN,
}

class DifferentNrOfStavesError(Exception):
    def __init__(self, old_nr, new_nr):
        self.old_nr = old_nr
        self.new_nr = new_nr
    

def handle_measure_lengths(a, bounds_a, bounds_b, timesigs_b, durations_b):
    lower_bound_b, upper_bound_b = bounds_b
    try:
        offset = sum([0] + durations_b[lower_bound_b:upper_bound_b])
    except:
        offset = 0

    for k in xrange(*bounds_a):
        for l in xrange(a.shape[1]):
            for tick in a[k, l].iter('tick'):
                old_tick = int(tick.text)
                tick.text = str(old_tick + offset)


def diff_staves(staves,
                durations,
                timesigs,
                staff_groups_map):

    old_staves, new_staves = staves
    old_durations, new_durations = durations
    old_timesigs, new_timesigs = timesigs

    #  In the  future I plan on using approximate matchings to handle
    # different numbers of staves and reordered staves.
    if len(old_staves) != len(new_staves):
        raise DifferentNrOfStavesError(len(old_staves), len(new_staves))
        
    else:

        cleaned_old_staves = copy.deepcopy(old_staves)
        cleaned_new_staves = copy.deepcopy(new_staves)
        cleaned_old_staves = map(clean_element, cleaned_old_staves)
        cleaned_new_staves = map(clean_element, cleaned_new_staves)

        old_measures = transpose_staves(old_staves)
        new_measures = transpose_staves(new_staves)

        old_strings = transpose_staves(cleaned_old_staves, canonical_xml_repr)
        new_strings = transpose_staves(cleaned_new_staves, canonical_xml_repr)

        matcher = difflib.SequenceMatcher(None, old_strings, new_strings, True)
        opcodes = matcher.get_opcodes()

        measures = diff_measures((old_measures, new_measures),
                                 (old_strings, new_strings),
                                 (old_durations, new_durations),
                                 (old_timesigs, new_timesigs),
                                 opcodes,
                                 staff_groups_map)

        return measures


def reserved_space_for_operation(opcode, durations1, durations2):
    tag, i1, i2, j1, j2 = opcode
    if tag == 'equal':
        return i2 - i1
    elif tag == 'replace':
        if durations1[i1:i2] == durations2[j1:j2]:
            return i2 - i1
        else:
            return (i2 - i1) + (j2 - j1)
    elif tag == 'delete':
        return i2 - i1
    elif tag == 'insert':
        return j2 - j1


# This function is the meat of our program,
# and as such is the most complex.
def diff_measures(measures_pair,
                  strings_pair,
                  durations_pair,
                  timesigs_pair,
                  opcodes,
                  staff_groups_map,
                  color_dict=_default_colors):
    # As in the source code of difflib, sequences are represented by the letters
    # A and B. We use capital letters here because we want to use them as a subscript
    # and writing `timesig_a` instead of `timesigA` is ugly.
    #
    # We already have the opcodes, and from this point on, we can (and will)
    # modify the A and B sequences destructively.  We can do this because
    # once we get the opcodes, there are few equality tests to be made, and
    # the few we will make will use the string representation of the measures,
    # which remains unchanged in this function.
    A, B = map(np.array, copy.deepcopy(measures_pair))

    durationsA, durationsB = durations_pair
    # Once again, not real time signatures, but close enough.
    timesigsA, timesigsB = timesigs_pair

    # The striing tuples, turned into np.arrays.
    # They will be usefull to separate the measures by staff.
    sA, sB = np.array(strings_pair[0]), np.array(strings_pair[1])

    # Width and Height of the `A` and `B` arrays.
    wA, hA = A.shape
    wB, hB = B.shape

    # Dimensions of the `diff` matrix.
    height = hA + hB
    width = sum([reserved_space_for_operation(opcode, durationsA, durationsB)
                 for opcode in opcodes])

    # The array to store our (possibly colored) measures.
    diff = np.zeros((width, height), dtype=object)

    # We will be doing creative things with time signatures, and it's better
    # if each measure stores it's own length, independently of what we do with
    # the time signature symbols, which we will delete and replace at will.
    for seq, timesigs in [(A, timesigsA), (B, timesigsB)]:
        for k in xrange(seq.shape[0]):
            for l in xrange(seq.shape[1]):
                sigN, sigD = timesigs[k]
                seq[k, l].set('len', '{}/{}'.format(sigN, sigD))

    offset = 0
    # The functions `handle_equal`, `handle_replace`, `handle_delete` and
    # `handle_insert` are destructive. They change the variables:
    # `diff`, `A` and `B`, but not the `offset`.
    for opcode in opcodes:
        tag, _, _, _, _ = opcode

        if tag == 'equal':
            handle_equal(diff, opcode, offset, A, B, hA)

        elif tag == 'delete':
            handle_delete(diff, opcode, offset, A, B, hA, hB, wB,
                  timesigsA, durationsA, color_dict)

        elif tag == 'insert':
            handle_insert(diff, opcode, offset, A, B, hA, hB, wA,
                  timesigsB, durationsB,
                  color_dict)

        elif tag == 'replace':
            handle_replace(diff, opcode,  offset, A, B,
                   hA, hB, wA, wB, sA, sB,
                   timesigsA, timesigsB, durationsA, durationsB,
                   color_dict)

        # Update the offset to the current position
        offset += reserved_space_for_operation(opcode, durationsA, durationsB)

    #  Handle measure numbers. We attribute natural numbers from
    # 1 to the number of measures.
    #  We also post-process the measure in other ways, as described near
    # the function definition.
    for k, l in np.ndindex(diff.shape):
        diff[k, l] = post_process_measure(diff[k, l], k, l, staff_groups_map)

    for k in xrange(width):
        timesig = None
        for l in xrange(height):
            _timesig = diff[k,l].find('TimeSig')
            if _timesig is not None:
                timesig = _timesig

        if timesig is not None:
            for l in xrange(height):
                if diff[k, l].find('TimeSig') is None:
                    # Don't know how this works, but let's keep it...
                    new_timesig = copy.deepcopy(timesig)
                    set_visibility(new_timesig, 0)
                    diff[k, l].insert(0, new_timesig)

    return diff

# ### Handle the `equal` tag
def handle_equal(diff, opcode, offset, A, B, hA):
    tag, i1, i2, j1, j2 = opcode
    # All in Black
    diff[offset:offset+i2-i1, :hA] = copy.deepcopy(A[i1:i2])
    diff[offset:offset+j2-j1, hA:] = copy.deepcopy(B[j1:j2])


# ### Handle the `delete` tag
def handle_delete(diff, opcode, offset, A, B, hA, hB, wB,
                  timesigsA, durationsA, color_dict):
    tag, i1, i2, j1, j2 = opcode

    diff[offset:offset+i2-i1, :hA] = copy.deepcopy(A[i1:i2])
    diff[offset:offset+i2-i1, hA:] = copy.deepcopy(A[i1:i2])
    handle_measure_lengths(B, (j2, wB), (i1, i2), timesigsA, durationsA)

    set_measures_color(diff, (offset, offset+i2-i1, 0, hA),
                       color_dict['deleted'])
    make_measures_invisible(diff, (offset, offset+i2-i1, hA, hA+hB))


# ### Handle the `insert` tag
def handle_insert(diff, opcode, offset, A, B, hA, hB, wA,
                  timesigsB, durationsB, color_dict):
    tag, i1, i2, j1, j2 = opcode

    diff[offset:offset+j2-j1, :hA] = copy.deepcopy(B[j1:j2])
    diff[offset:offset+j2-j1, hA:] = copy.deepcopy(B[j1:j2])
    handle_measure_lengths(A, (i2, wA), (j1, j2), timesigsB, durationsB)

    set_measures_color(diff, (offset, offset+j2-j1, hA, hA+hB),
                       color_dict['inserted'])
    make_measures_invisible(diff, (offset, offset+j2-j1, 0, hA))


# ### Handle the `replace` tag
#
# This is the most complex tag to handle, because we want to
# get a diff that is as meaningfull and minimal as possible.
def handle_replace(diff, opcode,  offset, A, B, hA, hB, wA, wB, sA, sB,
                   timesigsA, timesigsB, durationsA, durationsB,
                   color_dict):

    tag, i1, i2, j1, j2 = opcode
    if i2 - i1 == j2 - j1 and durationsA[i1:i2] == durationsB[j1:j2]:

        diff[offset:offset+i2-i1, :hA] = copy.deepcopy(A[i1:i2])
        diff[offset:offset+j2-j1, hA:] = copy.deepcopy(B[j1:j2])

        for k in xrange(0, i2-i1):
            for l in xrange(0, hA):
                if sA[i1+k, l] != sB[j1+k, l]:
                    # Only change the color in the staves in which the measure
                    # is actually different, to direct the user to where the
                    # change is. In the future, we might compare the elements
                    # themselves and color only the tuplets, chords or notes.
                    color_element(diff[offset+k, l], color_dict['replaced'], recursive=True)
                    color_element(diff[offset+k, l+hA], color_dict['replaces'], recursive=True)

    # If we can't line the replaced measures with the ones that replace them,
    # we render the measures as if it were a deletion followed by an insertion.
    else:
        diff[offset:offset+(i2-i1), :hA] = copy.deepcopy(A[i1:i2])
        diff[offset:offset+(i2-i1), hA:] = copy.deepcopy(A[i1:i2])
        handle_measure_lengths(B, (j1, wB), (i1, i2), timesigsA, durationsA)

        diff[offset+(i2-i1):offset+(i2-i1)+(j2-i1), :hA] = copy.deepcopy(B[j1:j2])
        diff[offset+(i2-i1):offset+(i2-i1)+(j2-j1), hA:] = copy.deepcopy(B[j1:j2])
        handle_measure_lengths(A, (i2, wA), (j1, j2), timesigsB, durationsB)

        set_measures_color(diff,
                           (offset, offset+i2-i1, 0, hA),
                           color_dict['replaced'])

        set_measures_color(diff,
                           (offset+(i2-i1), offset+(i2-i1)+(j2-j1), hA, hA+hB),
                           color_dict['replaces'])

        make_measures_invisible(diff, (offset, offset+i2-i1, hA, hA+hB))
        make_measures_invisible(diff, (offset+(i2-i1), offset+(i2-i1)+(j2-j1), 0, hA))


def get_staff_groups(top_score, bottom_score):
    top_parts = top_score.findall('Part')
    bottom_parts = bottom_score.findall('Part')
    staff_groups_map = dict()
    # indexing is 0-based, unlike the staff.ids
    # This is because this will be used in diff_measures
    staff_nr = 0
    for part_nr, part in enumerate(top_parts + bottom_parts):
        staffs = part.findall('Staff')
        staff_groups_map[staff_nr] = {'has_barline': True,
                                       'span': len(staffs)}
        staff_nr += 1
        for staff in staffs[1:]:
            staff_groups_map[staff_nr] = {'has_barline': False,
                                          'span': None}
            staff_nr += 1
    return staff_groups_map


def post_process_measure(measure, k, l, staff_groups_map):
    measure.set('number', str(k+1))
    barlines = measure.findall('BarLine')

    # Setting to 0 the visibility of the staff that has the barline
    # (usually the top one) hides the barlines, which we don't want
    # We will have to manually add barlines to all all staves.
    # The `staff_group_map` tells us when to add a barline
    # (`staff_group_map[l]['has_lines']`) and the span of the bar to add
    # (`staff_group_map[l]['span']`).

    if not barlines and staff_groups_map[l]['has_barline']:
        subtype = etree.Element('subtype')
        subtype.text = 'normal'

        customSubtype = etree.Element('customSubtype')
        customSubtype.text = "1"

        # How many staves the bar spans (or crosses)?
        # This is usually 1 for a voice part, 2 for a piano part
        # and 3 for an organ part, for example.
        span = etree.Element('span')
        span.text = str(staff_groups_map[l]['span'])

        barline = etree.Element('BarLine')
        barline.extend([subtype, customSubtype, span])

        measure.append(barline)

    else:
        for barline in barlines:
            customSubtype = etree.Element('customSubtype')
            customSubtype.text = "1"

            subtype = barline.find('subtype')
            barline.insert(barline.index(subtype)+1, customSubtype)

    return measure
