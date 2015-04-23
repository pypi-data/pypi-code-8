class BaseEngine(object):

    def __init__(self, word):
        self.word = word

    def parse(self):
        '''
        parse word with specefic engine
        '''
        assert NotImplemented

    def parse_normal(self):
        '''
        parse word in normal form
        '''
        assert NotImplemented

    def normal_form(self):
        '''
        generate normal word form
        '''
        assert  NotImplemented

    def lexeme(self):
        '''
        return lexemes of word
        '''
        assert NotImplemented

    def process(self):
        self.parse()
        self.normal_form()
        self.parse_normal()
        self.lexeme()
        if self.lexemes:
            return self.lexemes
        else:
            raise Exception
