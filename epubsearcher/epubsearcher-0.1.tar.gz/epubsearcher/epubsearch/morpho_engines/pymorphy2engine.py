from .baseengine import BaseEngine
import pymorphy2


class Pymorphy2Engine(BaseEngine):
    """docstring for PyMorphy2"""
    def parse(self):
        self.morph = pymorphy2.MorphAnalyzer()
        self.parsed_word = self.morph.parse(self.word)[0]

    def normal_form(self):
        self.normal_form_word = self.parsed_word.normal_form

    def parse_normal(self):
        self.parsed_normal_word = self.morph.parse(self.normal_form_word)[0]

    def lexeme(self):
        lexemes = self.parsed_normal_word.lexeme
        self.lexemes = [lexeme.word for lexeme in lexemes if len(lexeme.word)>2]

