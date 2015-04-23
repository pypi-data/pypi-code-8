
import pyparsing
import re
from optparse import make_option


from shlex import split as _split
# shlex's split is broken in regards to Unicode in late Python 2.5 and
# most of Python 2.6.x.  It will turn everyting into UCS-4 regardless of
# input, so we need to specifically encode all the results to avoid this
# bug.  Python 2.7 doesn't have this problem.
safe_split = lambda a: [
    b.decode('utf-8') for b in _split(a.encode('utf-8'))
]


options_defined = [] # used to distinguish --options from SQL-style --comments

pyparsing.ParserElement.setDefaultWhitespaceChars(' \t')


class ParsedString(str):
    def full_parsed_statement(self):
        new = ParsedString('%s %s' % (self.parsed.command, self.parsed.args))
        new.parsed = self.parsed
        new.parser = self.parser
        return new
    def with_args_replaced(self, newargs):
        new = ParsedString(newargs)
        new.parsed = self.parsed
        new.parser = self.parser
        new.parsed['args'] = newargs
        new.parsed.statement['args'] = newargs
        return new

def remaining_args(oldArgs, newArgList):
    '''
    Preserves the spacing originally in the argument after
    the removal of options.

    >>> remaining_args('-f bar   bar   cow', ['bar', 'cow'])
    'bar   cow'
    '''
    pattern = '\s+'.join(re.escape(a) for a in newArgList) + '\s*$'
    matchObj = re.search(pattern, oldArgs)
    return oldArgs[matchObj.start():]

class OptionParser(optparse.OptionParser):
    def exit(self, status=0, msg=None):
        self.values._exit = True
        if msg:
            print (msg)

    def print_help(self, *args, **kwargs):
        try:
            print (self._func.__doc__)
        except AttributeError:
            pass
        optparse.OptionParser.print_help(self, *args, **kwargs)

def options(option_list, arg_desc="arg"):
    """
    Used as a decorator and passed a list of optparse-style options,
    alters a cmd2 method to populate its ``opts`` argument from its
    raw text argument.

    Example: transform
    def do_something(self, arg):

    into
    @options([make_option('-q', '--quick', action="store_true",
              help="Makes things fast")],
              "source dest")
    def do_something(self, arg, opts):
        if opts.quick:
            self.fast_button = True
    """

    if not isinstance(option_list, list):
        option_list = [option_list]
    for opt in option_list:
        options_defined.append(pyparsing.Literal(opt.get_opt_string()))

    def option_setup(func):
        optionParser = OptionParser()
        for opt in option_list:
            optionParser.add_option(opt)
        optionParser.set_usage(
            "%s [options] %s"
            .format(func.__name__[3:].replace('_', '-'), arg_desc, )
        )
        optionParser._func = func

        def new_func(instance, arg):
            try:
                opts, newArgList = optionParser.parse_args(safe_split(arg))
                """
                 Must find the remaining args in the original argument list,
                 but mustn't include the command itself
                if hasattr(arg, 'parsed') and newArgList[0] == arg.parsed.command:
                    newArgList = newArgList[1:]
                """
                newArgs = remaining_args(arg, newArgList)
                if isinstance(arg, ParsedString):
                    arg = arg.with_args_replaced(newArgs)
                else:
                    arg = newArgs
            except optparse.OptParseError, e:
                print (e)
                optionParser.print_help()
                return
            if hasattr(opts, '_exit'):
                return None
            result = func(instance, arg, opts)
            return result
        new_func.__doc__ = '%s\n%s'.format(
            func.__doc__, optionParser.format_help(),
        )
        return new_func
    return option_setup
