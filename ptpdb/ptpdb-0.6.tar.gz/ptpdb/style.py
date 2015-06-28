from __future__ import unicode_literals

from ptpython.style import get_all_ui_styles as _get_all_ui_styles
from pygments.token import Token


def get_all_ui_styles():
    """
    Return mapping {name -> style_dict} of User Interface styles.
    """
    styles = _get_all_ui_styles()

    for name, style in styles.items():
        style.update({
            # Pdb tokens.
            Token.Prompt.BeforeInput:                      'bold #008800',
            Token.PdbCommand:                              'bold',
            Token.CompletionHint.Symbol:                   '#9a8888',
            Token.CompletionHint.Parameter:                '#ba4444 bold',
            Token.Toolbar.Status.Pdb.Filename:             'bg:#222222 #aaaaaa',
            Token.Toolbar.Status.Pdb.Lineno:               'bg:#222222 #ffffff',
            Token.Toolbar.Status.Pdb.Shortcut.Key:         'bg:#222222 #aaaaaa',
            Token.Toolbar.Status.Pdb.Shortcut.Description: 'bg:#222222 #aaaaaa',

            Token.Toolbar.Location:    'underline',
            Token.Toolbar.Location.Filename:    '',
            Token.Toolbar.Location.Lineno:    '',
        })
    return styles
