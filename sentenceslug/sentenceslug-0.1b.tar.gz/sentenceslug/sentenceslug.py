import random

from wordlists import WordLists as WL

class SentenceSlug:

    def __init__(self, withint=False):
        self.adjective = WL.randomAdjective().title()
        self.determiner = WL.randomDeterminer().title()
        self.noun = WL.randomNoun().title()
        self.verb = WL.randomVerb().title()

        if self.determiner == 'A' and self.adjective[0] in ['A', 'E', 'I', 'O', 'U']:
            self.determiner = 'An'
        self.slug = "%s%s%s%s" % (self.verb, self.determiner, self.adjective, self.noun)
        if withint:
            self.slug = "%s%03d" % (self.slug, random.randint(1,999))

class SimpleSlug:
    def __init__(self, withint=False):
        self.adjective = WL.randomAdjective().title()
        self.noun = WL.randomNoun().title()

        self.slug = "%s%s" % (self.adjective, self.noun)
        if withint:
            self.slug = "%s%03d" % (self.slug, random.randint(1,999))

if __name__ ==  '__main__':

    combos = len(WL.verbs) * len(WL.determiners) * len(WL.adjectives) * len(WL.nouns)
    print "Examples of sentence slugs without integer postfix: (%s combos)" % combos
    for i in range(10):
        ss = SentenceSlug()
        print ss.slug

    print ""

    combos = combos * 999
    print "Examples of sentence slugs with integer postfix: (%s combos)" % combos
    for i in range(10):
        ss = SentenceSlug(withint=True)
        print ss.slug

    print ""

    combos = len(WL.adjectives) * len(WL.nouns)
    print "Examples of simple slugs without integer postfix: (%s combos)" % combos
    for i in range(10):
        ss = SimpleSlug()
        print ss.slug

    print ""

    combos = combos * 999
    print "Examples of simple slugs with integer postfix: (%s combos)" % combos
    for i in range(10):
        ss = SimpleSlug(withint=True)
        print ss.slug