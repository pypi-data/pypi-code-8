








if __name__ == '__main__':

    # import cProfile
    # links = [
    #     {'Wochenende': {'value': '/wiki/fox'}},
    #     {'Samstag': {'value': '/wiki/fox'}},
    #     {'Mannschaften': {'value': '/wiki/fox'}},
    #     {'Mannschaft': {'value': '/wiki/fox'}},
    #     {'belegt': {'value': '/wiki/fox'}},
    #     {'Bereits': {'value': '/wiki/fox'}},
    #     {'der': {'value': '/wiki/fox'}},
    #     {'Spieltag': {'value': '/wiki/fox'}},
    #     {'Vergangene Woche': {'value': '/wiki/fox'}},
    #     {'Spieler': {'value': '/wiki/fox'}},
    #     {u'schön': {'value': '/wiki/fox'}},
    #     {'Spieler': {'value': '/wiki/fox'}},
    #     {'Tor': {'value': '/wiki/fox'}},
    #     {'Tabelle': {'value': '/wiki/fox'}},
    #     {'Ergebnis': {'value': '/wiki/fox'}}
    #     ]

    # text = """Zweite Bundesliga Wunschtrainer Tuchel sagt RB Leipzig ab <p>Mit Thomas Tuchel auf der Trainerbank wollte RB Leipzig nach ganz oben. Doch daraus wird nichts. Der Wunschkandidat sagt dem Klub aus der zweiten Liga ab. Die Begründung liefert Tuchels Berater. Wohin zieht es Thomas Tuchel? Leipzig ist nicht das Ziel des Trainers Wunschkandidat Thomas Tuchel hat Rasenballsport Leipzig eine Absage erteilt. „Thomas Tuchel wird im Sommer definitiv nicht Trainer von RB Leipzig“, sagte Sportdirektor Ralf Rangnick der „Leipziger Volkszeitung“. Tuchels Berater habe dem Klub-Vorstandsvorsitzenden, Oliver Mintzlaff, mitgeteilt, dass der 41-Jährige nicht in die zweiten Fußball-Bundesliga gehe, schrieb die Zeitung am Montag auf ihrer Internetseite. „RB Leipzig ist unabhängig von Herrn Tuchel und anderen Namen auch nicht bereit, finanzielle Grenzen für einen Zweitliga-Trainer zu überschreiten“, sagte Mintzlaff der „Sport Bild“. „Unser Weg bleibt unbeirrt – wir werden mit unserer A-Lösung auf der Trainerposition in die neue Saison gehen.“ Mehr zum Thema Die aktuelle Tabelle der Fußball-Bundesliga Hamburger SV : Ein Nest für Tuchel</p> Vorwürfe von Torwart Müller: „Tuchel ist ein Diktator“ <p>Rangnick hatte Tuchel stets als einen idealen Kandidaten für die kommende Saison bezeichnet, eine bereits vorliegende Einigung aber immer dementiert. Die Trainerfrage hatte sich gestellt, nachdem Alexander Zorniger im Februar vorzeitig aus seinem Vertrag bei RB ausgestiegen war. Nachwuchscoach Achim Beierlorzer war als Interimstrainer bis zum Saisonende verpflichtet worden.</p><p>Die Leipziger haben sieben Spieltage vor dem Saisonende nur noch theoretische Chancen auf den Durchmarsch in die Bundesliga. Nach dem 2:1-Sieg am Ostersonntag über den 1. FC Nürnberg liegen sie acht Zähler hinter dem Relegationsplatz drei.</p><p>Tuchel, dessen ruhender Vertrag zum Saisonende beim Bundesligaverein FSV Mainz 05 ausläuft, ist bei verschiedenen Vereinen im Gespräch. Der 41-Jährige hatte Mainz im vergangenen Sommer verlassen und war seitdem kein neues Engagement eingegangen.</p>"""

    # cProfile.run('add(text, links)')



    links = [{'red fox': {'value': '/wiki/fox'}}, {'fox': {'value': '/wiki/fox'}}, {'dog': {'value': '/wiki/dog'}}]
    # text = "fox The quick brown fox jumps over the lazy <br> dog and fox. dog"
    text = "fox fox red fox Dog <p>dog dog</p> Dog"

    # b = Anchorman(text, links, replaces_per_item=100000)

    # print b.positions()

    # markup_format = {
    #     'replace_match_with_value': True,
    #     'tag': "a",
    #     'value_key': "href", # attribute for the value see _get_entity_item
    #     'attributes': [("class", "taxonomy-entity"),
    #                    # ("xCOLONshow", "embed"),
    #                    # ("xCOLONtype", "simple")
    #                    ]
    # }

    # text = "<p>Foxes are small-to-medium-sized, omnivorous mammals belonging to several genera of the Canidae family. Foxes are slightly smaller than a medium-size domestic dog, with a flattened skull, upright triangular ears,<br> a pointed, slightly upturned snout, and a long bushy tail (or brush).</p>"

    # text = "Foxes are small-to-medium-sized, omnivorous mammals belonging to several genera of the Canidae family. Foxes are slightly smaller than a medium-size domestic dog, with a flattened skull, upright triangular ears, a pointed, slightly upturned snout, and a long bushy tail (or brush)."

    # links = [
    #     {'Fox': {'value': '/fox'}},
    #     {'mammals': {'value': '/mammals'}},
    #     {'red fox': {
    #         'value': '/redfox',
    #         'attributes': [
    #             ('class', 'animal'),
    #             ('style', 'font-size:23px;background:red'),
    #             ('title', 'Fix und Foxi')
    #             ]
    #         }
    #     },
    #     {'a medium-size domestic dog': {'value': '/dog'}}
    # ]


    markup_format = {
        'case_sensitive': False,
        'replace_match_with_value': True,
        'highlighting': {
            'pre': '${{',
            'post': '}}'
            }
    }

    # # replaces_per_item=1
    # # replaces_at_all=1

    a = add(
        text,
        links,
        replaces_per_item=3,
        # replaces_at_all=1,
        markup_format=markup_format
        )
    print a

    # # # markup_format['selector'] = ".//a[contains(@href, '/mammals')]"
    # # # print a.remove(markup_format=markup_format)

    # # print a.remove(selector=".//a[contains(@href, '/mammals')]")

    # # print text
    # print a.positions(case_sensitive=False)
    # # a.remove()
    # # print a


    # # markup_format = {
    # #     'tag': "a",
    #     'value_key': "xCOLONhref", # attribute for the value see _get_entity_item
    #     'attributes': [("class", "taxonomy-entity"),
    #                    ("xCOLONshow", "embed"),
    #                    ("xCOLONtype", "simple")]
    # }
    # anchi = Anchorman(markup_format=markup_format, selector='.//a[@class="taxonomy-entity"]', replaces_per_item=1)
    # print anchi.selector
    # print anchi.replaces_per_item
    # anchi.remove('erewvbrg ew fefe')












# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# from codecs import open
# import json
# import anchorman
# import time

# ALLTIME = []
# ALLTIME_APPEND = ALLTIME.append
# TXTLEN = []
# TXTLEN_APPEND = TXTLEN.append
# RPLACEMENTS = []
# RPLACEMENTS_APPEND = RPLACEMENTS.append

# def timing(f):
#     def wrap(*args, **kwargs):
#         time1 = time.time()
#         ret = f(*args, **kwargs)
#         time2 = time.time()
#         ALLTIME_APPEND((time2-time1)*1000.0)
#         # print '%s function took %0.3f ms' % (f.func_name, (time2-time1)*1000.0)
#         return ret
#     return wrap

# DATADIR = "/Users/rebel/Documents/spark-1.2.1-bin-hadoop2.4/data/texte/Vorbericht-Korpora"
# with open('/Users/rebel/Documents/spark-1.2.1-bin-hadoop2.4/data/texte/Vorbericht-Korpora-filenames.txt', 'r', 'utf-8') as f:
#     FILENAMES = f.read().split('\n')


# def get_json_document(DATADIR, filename):
#     with open('%s/%s' % (DATADIR, filename), 'r', 'utf-8') as f:
#         document = json.loads(f.read())
#     return document



# for i,filename in enumerate((FILENAMES*2)[:1000]):

#     @timing
#     def anchorman_it(text, links, markup_format=None):
#         if markup_format:
#             a = anchorman.add(text, links, markup_format=markup_format)
#         else:
#             a = anchorman.add(text, links)
#         return a.result, a.counts

#     links = [
#         {'Wochenende': {'value': '/wiki/fox'}},
#         {'Samstag': {'value': '/wiki/fox'}},
#         {'Mannschaften': {'value': '/wiki/fox'}},
#         {'Mannschaft': {'value': '/wiki/fox'}},
#         {'belegt': {'value': '/wiki/fox'}},
#         {'Bereits': {'value': '/wiki/fox'}},
#         {'der': {'value': '/wiki/fox'}},
#         {'Spieltag': {'value': '/wiki/fox'}},
#         {'Vergangene Woche': {'value': '/wiki/fox'}},
#         {'Spieler': {'value': '/wiki/fox'}},
#         {u'schön': {'value': '/wiki/fox'}},
#         {'Spieler': {'value': '/wiki/fox'}},
#         {'Tor': {'value': '/wiki/fox'}},
#         {'Tabelle': {'value': '/wiki/fox'}},
#         {'Ergebnis': {'value': '/wiki/fox'}}
#         ]

#     markup_format = {
#             'tag': 'a',
#             'value_key': 'href', # attribute for the value (see links in add)
#             'attributes': [
#                 ('style', 'color:blue;cursor:pointer;'),
#                 ('class', 'anchorman')
#                 ],
#             'rm-identifier': 'anchorman-link', # identifier for specific rm
#         }

#     # markup_format = {
#     #     'highlighting': {
#     #         'pre': '${{',
#     #         'post': '}}'
#     #         }
#     #     }



#     f = get_json_document(DATADIR, filename)
#     text = f['body']*3

#     TXTLEN_APPEND(len(text))
#     r, c = anchorman_it(text, links, markup_format=markup_format)
#     RPLACEMENTS_APPEND(sum([y for (x,y) in c]))

#     # break

# def mean(l):
#     return (reduce(lambda x, y: x + y, l) / len(l))


# print "processed items %s" % len(ALLTIME)

# print "mean txt len %s" % mean(TXTLEN)
# print "mean repl per text %s" % mean(RPLACEMENTS)


# print "min  %.5f s" % (min(ALLTIME)/1000)
# print "max  %.5f s" % (max(ALLTIME)/1000)
# print "mean %.5f s" % (mean(ALLTIME)/1000)




# # # without markup

# # mean txt len 1766
# # mean repl per text 11
# # min  0.00060 s
# # max  0.00891 s
# # mean 0.00152 s
# # [Finished in 1.7s]


# # # with markup

# # processed items 1000
# # mean txt len 1766
# # mean repl per text 11
# # min  0.00061 s
# # max  0.00929 s
# # mean 0.00158 s
# # [Finished in 1.8s]


# # # highlight context

# # processed items 1000
# # mean txt len 1766
# # mean repl per text 11
# # min  0.00057 s
# # max  0.00783 s
# # mean 0.00117 s
# # [Finished in 1.4s]




# # processed items 1000
# # mean txt len 1766
# # mean repl per text 11
# # min  0.00092 s
# # max  0.01398 s
# # mean 0.00253 s
# # [Finished in 2.8s]

# # processed items 1000
# # mean txt len 1766
# # mean repl per text 11
# # min  0.00083 s
# # max  0.01216 s
# # mean 0.00186 s
# # [Finished in 2.1s]


# # processed items 1000
# # mean txt len 1766
# # mean repl per text 11
# # min  0.00062 s
# # max  0.01047 s
# # mean 0.00146 s
# # [Finished in 1.7s]

# # processed items 1000
# # mean txt len 1766
# # mean repl per text 1
# # min  0.00030 s
# # max  0.00406 s
# # mean 0.00069 s
# # [Finished in 0.9s]
