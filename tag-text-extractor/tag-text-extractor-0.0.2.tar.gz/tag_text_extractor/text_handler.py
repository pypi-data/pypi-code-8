# -*- coding:utf-8 -*-
import re

from xml.sax.handler import ContentHandler

def get_stop_words():
    #TODO: сделать возможность передавать как параметр
    stopwords = u'a|about|all|an|and|any|are|as|at|be|but|by|can|do|for|from|have|i|if|in|is|it|my|no|not|of|on|one|or|so|that|the|there|they|this|to|was|we|what|which|will|with|would|you|а|або|авжеж|аж|але|атож|б|без|би|бо|був|буде|будем|будемо|будет|будете|будеш|будешь|буду|будут|будуть|будь|будьмо|будьте|була|були|було|бути|бы|был|была|были|было|быть|в|вам|вами|вас|ваш|ваша|ваше|вашим|вашими|ваших|вашого|вашому|вашою|вашої|вашу|ваші|вашій|вашім|ввесь|весь|вже|ви|во|воно|вот|все|всего|всей|всем|всеми|всему|всех|всею|всього|всьому|всю|вся|всё|всі|всій|всім|всіма|всіх|всією|всієї|вы|від|він|да|де|для|до|дуже|еге|его|ее|ей|ему|если|есть|еще|ещё|ею|её|ж|же|з|за|зі|и|из|или|им|ими|их|й|його|йому|к|как|кем|кимось|ко|когда|кого|когось|ком|кому|комусь|которая|которого|которое|которой|котором|которому|которою|которую|которые|который|которым|которыми|которых|кто|кім|ледве|лиш|лише|майже|мене|меня|мені|мне|мной|мною|мовби|мог|моги|могите|могла|могли|могло|мого|ой|могу|могут|мое|моего|моей|моем|моему|моею|можем|может|можете|можешь|мои|моим|моими|моих|мой|мочь|мою|моя|моё|моём|моє|моєму|моєю|моєї|мої|моїй|моїм|моїми|моїх|мы|між|мій|на|навіть|над|нам|нами|нас|наче|начебто|наш|наша|наше|нашего|нашей|нашем|нашему|нашею|наши|нашим|нашими|наших|нашого|нашому|нашою|нашої|нашу|наші|нашій|нашім|не|невже|него|нее|ней|нем|немов|нему|неначе|нет|нехай|нею|неё|неї|ним|ними|них|но|ну|нього|ньому|нём|ні|ніби|нібито|ній|ніким|нікого|нікому|нікім|нім|ніхто|нічим|нічого|нічому|ніщо|ніяка|ніяке|ніякий|ніяким|ніяких|ніякого|ніякому|ніякою|ніякої|ніякі|ніякій|о|об|од|один|одна|одни|одним|одними|одних|одно|одного|одной|одном|одному|одною|одну|он|она|они|оно|от|отак|ото|оце|оцей|оцеє|оцим|оцими|оцих|оцього|оцьому|оцю|оцюю|оця|оцяя|оці|оцій|оцім|оцією|оцієї|оції|по|поки|при|про|під|с|сам|сама|саме|самий|самим|самими|самих|само|самого|самому|самою|самої|саму|самі|самій|самім|свого|свое|своего|своей|своем|своему|своею|свои|своим|своими|своих|свой|свою|своя|своё|своём|своє|своєму|своєю|своєї|свої|своїй|своїм|своїми|своїх|свій|се|себе|себя|сей|сими|сих|собой|собою|собі|сього|сьому|сю|ся|сі|сій|сім|сією|сієї|та|так|така|такая|таке|таки|такие|такий|таким|такими|таких|такого|такое|такой|таком|такому|такою|такої|таку|такую|такі|такій|такім|тая|твого|твою|твоя|твоє|твоєму|твоєю|твоєї|твої|твоїй|твоїм|твоїми|твоїх|твій|те|тебе|тебя|тем|теми|тех|теє|ти|тим|тими|тих|то|тобой|тобою|тобі|того|той|только|том|тому|тот|тою|тої|ту|тую|ты|ті|тій|тільки|тім|тією|тієї|тії|у|увесь|уже|усе|усього|усьому|усю|уся|усі|усій|усім|усіма|усіх|усією|усієї|хай|хоч|хто|хтось|хіба|це|цей|цеє|цим|цими|цих|цього|цьому|цю|цюю|ця|цяя|ці|цій|цім|цією|цієї|ції|чего|чем|чему|чи|чий|чийого|чийому|чим|чимось|чимсь|чию|чия|чиє|чиєму|чиєю|чиєї|чиї|чиїй|чиїм|чиїми|чиїх|чого|чогось|чому|чомусь|что|чтобы|чём|чім|чімсь|ще|що|щоб|щось|эта|эти|этим|этими|этих|это|этого|этой|этом|этому|этот|эту|я|як|яка|якась|яке|якесь|який|якийсь|яким|якими|якимись|якимось|якимсь|яких|якихось|якого|якогось|якому|якомусь|якою|якоюсь|якої|якоїсь|якраз|яку|якусь|якщо|які|якій|якійсь|якім|якімось|якімсь|якісь|є|і|із|іякими|їй|їм|їх|їхнього|їхньому|їхньою|їхньої|їхню|їхня|їхнє|їхні|їхній|їхнім|їхніми|їхніх|її|http|www'        
    return set(stopwords.split('|'))

class TextHandler(ContentHandler):
    non_alpha_num_re = re.compile(ur'\W', re.U | re.M)
    trash_text_re = re.compile(ur'[^а-яa-z\d]', re.U | re.I | re.M)
    replace_e_re = re.compile(ur'ё', re.U | re.M)
    whitespace_re = re.compile(ur'[\S]+', re.U | re.M)
    multispaces_re = re.compile(ur'\s+', re.U | re.M)
    stopwords = get_stop_words()
    alpha_num_re = re.compile(ur'\w', re.U | re.M)

    def __init__(self):
        self.result = {
            'title': {'texts': [], 'word_count': 0},
            'h1': {'texts': [], 'word_count': 0},
            'a': {'texts': [], 'word_count': 0},
            'h2h6': {'texts': [], 'word_count': 0},
            'beis': {'texts': [], 'word_count': 0},
            'body': {'texts': [], 'word_count': 0},
            'metadescription': {'texts': [], 'word_count': 0},
            'text': {'texts': [], 'word_count': 0}

        }
        self.current_element = None
        self.path = []
        self.good_tags_path = []
        ContentHandler.__init__(self)

    def startElement(self, name, attrs):
        if not name:
            return
        
        name = name.lower()
        
        self.path.append(name)
        if name == 'meta':
            attr_names = attrs.getNames()
            if not 'content' in attr_names or not 'name' in attr_names:
                return
            name_value = attrs.getValue('name')
            if name_value == 'description':
                content_value = attrs.getValue('content')
                self.result['metadescription']['texts'].append(content_value)
                self.result['metadescription']['word_count'] += self._get_words_count(content_value)
            return

        if self.current_element == 'h1':
            return
        elif self.current_element == 'a' and name != 'h1':
            return
        elif name not in ['b', 'strong', 'em', 'i', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'h1',
                          'title', 'description']:
            return
        else:
            self.current_element = name.lower()

    def endElement(self, name):
        name = name.lower()
        if self.path:
            pop_tag = self.path.pop(-1)
            while pop_tag != name and self.path:
                pop_tag = self.path.pop(-1)

        if self.current_element == 'h1' and name != 'h1':
            return
        elif self.current_element == 'a' and name != 'a':
            return
        elif self.current_element == 'h1' and name == "h1" and 'h1' in self.path:
            return
        elif self.current_element == 'h1' and name == "h1" and 'a' in self.path:
            self.current_element = 'a'
            return
        else:
            if self.path:
                n = -1
                self.current_element = self.path[n]
                while self.current_element not in ['b', 'strong', 'em', 'i', 'h2', 'h3', 'h4', 'h5',
                                                   'h6', 'a', 'h1', 'title', 'description']:
                    n -= 1
                    try:
                        self.current_element = self.path[n]
                    except Exception:
                        self.current_element = None
                        break
            else:
                self.current_element = None

    def characters(self, content):
        content = content.strip()
        
        if not content or u'ï¿½Ã' in content:
            #контента нет или это треш контент
            return

        p = self.current_element
        if p != 'title' and p != 'meta':
            self.result['body']['texts'].append(content)
            self.result['body']['word_count'] += self._get_words_count(content)
        if p == 'h1':
            self.result['h1']['texts'].append(content)
            self.result['h1']['word_count'] += self._get_words_count(content)
        elif p == 'a':
            self.result['a']['texts'].append(content)
            self.result['a']['word_count'] += self._get_words_count(content)
        elif p == 'title':
            self.result['title']['texts'].append(content)
            self.result['title']['word_count'] += self._get_words_count(content)
        elif p in ['b', 'strong', 'em', 'i']:
            self.result['beis']['texts'].append(content)
            self.result['beis']['word_count'] += self._get_words_count(content)
        elif p in ['h2', 'h3', 'h4', 'h5', 'h6']:
            self.result['h2h6']['texts'].append(content)
            self.result['h2h6']['word_count'] += self._get_words_count(content)
        elif p != 'title' and p != 'meta':
            self.result['text']['texts'].append(content)
            self.result['text']['word_count'] += self._get_words_count(content)


    def _get_words_count(self, text):
        text = unicode(text.lower())
        text = self.non_alpha_num_re.sub(' ', text)
        text = self.replace_e_re.sub(u'е', text)

        words = []
        for word in self.whitespace_re.findall(text):
            if word not in self.stopwords:
                words.append(word)
        return len(words)
