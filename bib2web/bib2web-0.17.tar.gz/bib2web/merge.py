# coding=utf-8

from bibtexparser import load, loads, dump, dumps
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from pybtex.database import Person
from normalize import normalize_title, normalize_author
import errno
import re
import unicodedata
import latexcodec
import normalize
from glob import glob
from fuzzywuzzy.fuzz import ratio
import logging
import logging.config

logger = logging.getLogger(__name__)

def get_keycount(lst, key):
    matching = [s for s in lst if key in s]
    if len(matching) - 1 <= 0:
        return key 
    
    return str(key) + str(len(matching))

def merge_name_record(record1, record2):
    result = []
    if record1 == record2 or len(record2) == 0:
        return record1
    elif len(record1) == 0:
        return record2
    else:
        for i in range(len(record1)):
            if len(record1[i]) >= len(record2[i]):
                result.append(record1[i])
            elif len(record1[i]) <= len(record2[i]):
                result.append(record2[i])
            else:
                pass

        return result

def merge_name(name1, name1_norm, name2, name2_norm):
    if (name1_norm.first() == name2_norm.first() or name1_norm.first()[0][0] == name2_norm.first()[0][0]) and \
        (name1_norm.middle() == name2_norm.middle() or name1_norm.middle()[0][0] == name2_norm.middle()[0][0]) and\
        name1_norm.last() == name2_norm.last() and name1_norm.prelast() == name2_norm.prelast():
        first = ' '.join(merge_name_record(name1.first(), name2_norm.first()))
        middle = ' '.join(merge_name_record(name1.middle(), name2.middle()))
        lineage = ' '.join(merge_name_record(name1.lineage(), name2.lineage()))
        result = Person(first=first, middle=middle, prelast=' '.join(name1.prelast()), last=' '.join(name1.last()), lineage=lineage)
    else:
        return -1

    return result

def merge_names(name1, name1_norm, name2, name2_norm):
    result = -1
    if  len(name1_norm.first()) == len(name2_norm.first()) and \
        len(name1_norm.middle()) == len(name2_norm.middle()) and \
        len(name1_norm.last()) == len(name2_norm.last()):
        result = merge_name(name1, name1_norm, name2, name2_norm)

    return result

def not_intersection(union, intersection):
    return list(set(union) - set(intersection))

def intersect(a, b):
    """ return the intersection of two lists """
    return list(set(a) & set(b))

def get_union(a, b):
    """ return the union of two lists """
    return list(set(a) | set(b))

def add_field(entries, field, to_add):
    entries[field] = str(to_add)
    return entries

def split_name_to_person_list(author):
    authors = author.split(' and ')
    a = []
    for author in authors:
        a.append(Person(author))
    return a

def merge_author(author1, author1_norm, author2, author2_norm):
    merged = []
    authors1 = split_name_to_person_list(author1)
    authors2 = split_name_to_person_list(author2)
    authors1_norm = split_name_to_person_list(author1_norm)
    authors2_norm = split_name_to_person_list(author2_norm)
    if len(authors1) != len(authors1_norm) or len(authors2) != len(authors2_norm):
        print "Something wrong with author"
        return author1
    
    for i, author1 in enumerate(authors1):
        for j, author2 in enumerate(authors2):
            result = merge_names(author1, authors1_norm[i], author2, authors2_norm[j])
            if result != -1:
               merged.append(result) 

    return ' and '.join(unicode(person) for person in merged)

def merge_keywords(keywords1, keywords2):
    return set(keywords1 + keywords2)

def merge(entry1, entry2):
    db = BibDatabase()
    entries = {}
    keys1 = entry1.keys()
    keys2 = entry2.keys()
    intersection = intersect(keys1, keys2)
    union = get_union(keys1, keys2)
    not_intersect = not_intersection(union, intersection)

    #The two entries have the same keys, so everything needs to be merged
    if not not_intersect:
        for key in keys1:
            if key == 'author':
                author = merge_author(entry1[key], entry1['author_norm'], entry2[key], entry2['author_norm'])
                author_norm = normalize_author(str(author))
                entries = add_field(entries, key, author)
                entries = add_field(entries, 'author_norm', author_norm)
            if key == 'editor':
                editor = merge_author(entry1[key], entry1['editor_norm'], entry2[key], entry2['editor_norm'])
                editor_norm = normalize_author(str(editor))
                entries = add_field(entries, key, editor)
                entries = add_field(entries, 'editor_norm', editor_norm)
            elif key == 'keywords' or key == 'topics':
                entries = add_field(entries, key, merge_keywords(entry1[key], entry2[key]))
            elif key == 'month':
                entries = add_field(entries, key, entry1[key])
            elif len(entry1[key]) == len(entry2[key]) or len(entry1[key]) < len(entry2[key]):
                entries = add_field(entries, key, entry2[key])
            else:
                entries = add_field(entries, key, entry1[key])
    else:
        #All the keys in the two entries aren't the same, so some need to be merged
        #some can just be written
        #print "Entries are not the same!"
        #print keys1, keys2
        for key in intersection:
            if key == 'author':
                author = merge_author(entry1[key], entry1['author_norm'], entry2[key], entry2['author_norm'])
                entries = add_field(entries, key, author)
            if key == 'editor':
                editor = merge_author(entry1[key], entry1['editor_norm'], entry2[key], entry2['editor_norm'])
                entries = add_field(entries, key, editor)
            elif key == 'keywords' or key == 'topics':
                entries = add_field(entries, key, merge_keywords(entry1[key], entry2[key]))
            elif key == 'month':
                entries = add_field(entries, key, entry1[key])
            elif key == 'doi':
                entries = add_field(entries, get_keycount(intersection, key), entry1[key])
            elif len(entry1[key]) == len(entry2[key]) or len(entry1[key]) < len(entry2[key]):
                entries = add_field(entries, key, entry2[key])
            else:
                entries = add_field(entries, key, entry1[key])
        for key in not_intersect:
            if key in keys1:
                entries = add_field(entries, key, entry1[key])
            elif key in keys2:
                entries = add_field(entries, key, entry2[key])
    
    db.entries = [entries]
    return db
