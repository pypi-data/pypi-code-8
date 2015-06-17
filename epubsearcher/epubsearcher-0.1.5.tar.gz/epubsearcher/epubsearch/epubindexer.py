import importlib
from lxml import etree
import re, os

import logging


class EpubIndexer(object):
    epub = False
    engine = False

    def __init__(self, engine_name=False, database_name='indexdir', force_index=False):
        self.force_index = force_index
        self.database_name = database_name

        database_folder_path = "/tmp/epub_worker/databases/"
        if not os.path.exists(database_folder_path):
            os.mkdir(database_folder_path)

        self.database_path = database_folder_path + database_name
        if engine_name:
            mod = importlib.import_module("epubsearcher.epubsearch.search_engines.%sengine" % engine_name)
            # import whooshengine as engine
            self.engine = getattr(mod,'%sEngine' % engine_name.capitalize())(database_name)
            logging.info(self.engine)

    def load(self, epub):
        self.epub = epub
        if os.path.exists(self.database_path) and not self.force_index:
            try:
                self.engine.open()
            except Exception as e:
                print(e)
        else:
            self.engine.create()

            for spineItem in epub.spine:

                path = epub.base + "/" + spineItem['href']

                self.engine.add(path=path, href=spineItem['href'], title=spineItem['title'], cfiBase=spineItem['cfiBase'], spinePos=spineItem['spinePos'])

            self.engine.finished()

    def search(self, q, limit=None):
        rawresults = self.engine.query(q, limit)
        # print len(rawresults)
        r = {}
        r["results"] = []
        q = q.lower()

        for hit in rawresults:
            baseitem = {}
            baseitem['title'] = hit["title"].decode(encoding="UTF-8")
            baseitem['href'] = hit["href"].decode(encoding="UTF-8")
            baseitem['path'] = hit["path"].decode(encoding="UTF-8")

            # find base of cfi
            cfi_base= hit['cfiBase'].decode(encoding="UTF-8") + "!"

            with open(hit["path"], encoding='utf-8') as fileobj:
                tree = etree.parse(fileobj)
                parsedString = etree.tostring(tree.getroot())
                # case-insensitive xpath search
                xpath = './/*[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz") , "'+ q + '")]'
                #xpath = './/*[contains(text(),"'+ q +'")]'

                matchedList = tree.xpath(xpath)
                # print len(matchedList)
                for word in matchedList:
                    # copy the base
                    item = baseitem.copy()

                    # print word
                    # print word.getparent()
                    item['baseCfi'] = cfi_base
                    item['cfi'] = get_cfi(cfi_base, word)
                    #print cfi
                    # Create highlight snippet in try / except
                    # because I'm not convinced its error free for all
                    # epub texts
                    try:
                        item['highlight'] = create_highlight(word.text, q) # replace me with above
                    except Exception as e:
                        print("Exception when creating highlight for query", q)
                        print(e)
                        item['highlight'] = ''

                    r["results"].append(item)

        ## Sort results by chapter
        r['results'] = sorted(r['results'], key=lambda x: get_cfi_chapter(x['baseCfi']))
        return r


def get_cfi(cfiBase, word):
    cfi_list = []
    parent = word.getparent()
    child = word
    while parent is not None:
        i = parent.index(child)
        if 'id' in child.attrib:
            cfi_list.insert(0,str((i+1)*2)+'[' + child.attrib['id'] + ']')
        else:
            cfi_list.insert(0,str((i+1)*2))
        child = parent
        parent = child.getparent()
    cfi = cfiBase + '/' + '/'.join(cfi_list)
    return cfi

def get_cfi_chapter(cfi_base):
    cfi_base = re.sub(r'\[.*\]','',cfi_base)
    chapter_location = cfi_base[cfi_base.rfind('/')+1:cfi_base.find('!')]
    return int(chapter_location)


def create_highlight(text, query):
    tag = "<b class='match'>"
    closetag = "</b>"
    offset = len(query)

    leading_text = trim_length(text[:text.lower().find(query)],-10) + tag
    word = text[text.lower().find(query):text.lower().find(query)+offset]
    ending_text = closetag + trim_length(text[text.lower().find(query)+offset:],10)

    return leading_text + word + end_with_periods(ending_text)

def trim_length(text, words):
    if words > 0:
        text_list = text.split(' ')[:words]
    else:
        text_list = text.split(' ')[words:]

    return ' '.join(text_list)

def end_with_periods(text):
    if text[-1] not in '!?.':
        return text + ' ...'
    else:
        return text