# -*- coding: utf-8 -*-

from mistune import Renderer as RendererBase

from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import get_formatter_by_name


class HiliteRenderer(RendererBase):
    def block_code(self, text, lang):
        try:
            lexer = get_lexer_by_name(lang)
        except ValueError:
            try:
                if self.options.get('guess_lang', True):
                    lexer = guess_lexer(text)
                else:
                    lexer = get_lexer_by_name('text')
            except ValueError:
                lexer = get_lexer_by_name('text')

        formatter = get_formatter_by_name(
            'html',
            linenos=self.options.get('linenos', False),
            cssclass=self.options.get('cssclass', 'codehilite'),
            style=self.options.get('style', 'default'),
            noclasses=self.options.get('noclasses', False),
        )

        return highlight(text, lexer, formatter)
