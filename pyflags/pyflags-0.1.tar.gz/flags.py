__all__ = ['Flags']
__version__ = 0.1

import sys

class Flag(object):
    def __init__(self, flag, help, value, opt, coll):
        self.flag = flag
        self.help = help
        self.value = value
        self.opt = opt
        self.coll = coll

class Positional(object):
    def __init__(self, name, help, opt, coll):
        self.name = name
        self.help = help
        self.opt = opt
        self.coll = coll

class Flags(object):
    def __init__(self, help=True, help_start=None, help_end=None):
        '''
        Arguments:

        help: Whether or not to automatically add a help flag.
        help_start: Show this text preceding the help info.
        help_end: Show this text after the help info.
        '''
        self.flags = {}
        self.pos = []
        self.help = help
        if help:
            self.add('h', help='Show this screen')
            self.help_start = help_start
            self.help_end = help_end
        else:
            assert help_start is None, 'cannot have help_start without help'
            assert help_end is None, 'cannot have help_start without help'

    def add(self, flag, help='', value=False, opt=False, coll=False):
        '''
        Add a flag.

        Arguments:

        flag: The flag to add.
        help: The help string associated with the flag.
        value: Whether or not the flag is a value flag (takes a value).
        opt: Whether or not the flag is optional.
        coll: Whether or not the flag can be given multiple times.
        '''
        assert len(flag) == 1, 'flag must be 1 character long'
        assert not value or not opt, 'only value flags can have optional values'
        if value == True:
            value = 'value'
        self.flags[flag] = Flag(flag, help, value, opt, coll)

    def add_positional(self, name, help='', opt=False, coll=False):
        '''
        Add a positional argument.

        Arguments:

        name: The name of the positional argument.
        help: The help string associated with the argument.
        opt: Whether or not it is optional.
        coll: If True, any excess arguments will be labeled under this one.
        '''
        assert not self.pos or not self.pos[-1].coll,\
               'only last positional can be collective'
        assert opt or (not self.pos or self.pos[-1].opt),\
               'non-optional positional cannot follow optional positionals'
        assert len(name) > 1, 'positional ids must have a length greater than 1'
        self.pos.append(Positional(name, help, opt, coll))

    def _usage(self, this):
        flags = []
        posx = []
        for flag in self.flags.values():
            if flag.value:
                s = '[-%s<%s>]' % (flag.flag, flag.value)
            else:
                s = '[-%s]' % flag.flag
            if flag.coll:
                s += '...'
            flags.append(s)
        for pos in self.pos:
            s = '<%s>' % pos.name
            if pos.coll:
                s += '...'
            if pos.opt:
                s = '[%s]' % s
            posx.append(s)
        usage = 'usage: %s ' % this
        if posx:
            usage += ' '.join(posx)
            if flags:
                usage += ' '
        if flags:
            usage += ' '.join(flags)
        return usage

    def _show_help(self, this):
        print(self._usage(this))
        if self.help_start is not None:
            print(self.help_start)
        if self.pos:
            print('')
            print('Positional arguments:')
            print('')
            lng = max(len(pos.name) for pos in self.pos)
            for pos in self.pos:
                print('  %s   %s' % (pos.name.ljust(lng), pos.help))
        if self.flags:
            print('')
            print('Flags:')
            print('')
            lng = max(len(flag.value or '') for flag in self.flags.values())
            if lng:
                lng += 4
            for flag in self.flags.values():
                fl = flag.flag
                if flag.value:
                    fl += ('<%s>' % flag.value)
                print('  -%s   %s' % (fl.ljust(lng), flag.help))
        if self.help_end is not None:
            print('')
            print(self.help_end)

    def _err_need_value(self, flag):
        sys.exit('flag %s needs a value' % flag)

    def parse(self, args=None):
        '''
        Parse an arguments list.

        Arguments:

        args: A list of arguments to parse. Defaults to sys.argv.

        This function is an iterator, returning a sequence of pairs
        ``(type, argument, value)``:

        type: A string specifying the type of argument (flag or positional).
        argument: If ``type`` is ``flag``, then this is the single-character flag.
                  If it is ``positional``, then this is the positional argument
                  name.
        value: If the argument takes a value, then this is the value. If the
               argument takes no value, or if the value is optional and not given,
               then it is ``None``.
        '''
        if args is None:
            args = sys.argv

        args = args[:]

        this = args.pop(0)
        passed = set()
        poscount = 0
        get_value = None
        ponly = False
        gotcoll = False

        req = 0
        for p in self.pos:
            if not p.opt:
                req += 1
            else:
                break

        for piece in args:
            if piece[0] == '-' and not ponly:
                if get_value is not None:
                    self._err_need_value(get_value)
                if piece == '--':
                    ponly = True
                    continue
                piece = piece[1:]
                for i, fl in enumerate(piece):
                    if self.help and fl == 'h':
                        self._show_help(this)
                        sys.exit()
                    try:
                        flag = self.flags[fl]
                    except:
                        sys.exit('unknown flag: -%s' % fl)
                    if flag in passed:
                        sys.exit('duplicate flag: -%s' % flag.flag)
                    if flag.value:
                        if i+1 == len(piece):
                            if flag.opt:
                                yield ('flag', fl, None)
                            else:
                                get_value = flag.flag
                        else:
                            yield ('flag', fl, piece[i+1:])
                            break
                    else:
                        yield ('flag', fl, None)
                    if not flag.coll:
                        passed.add(fl)
            else:
                if get_value is not None:
                    yield ('flag', get_value, piece)
                    get_value = None
                else:
                    if poscount >= len(self.pos) and not self.pos[-1].coll:
                        sys.exit('too many positional arguments')
                    yield ('positional', self.pos[poscount].name, piece)
                    if not self.pos[poscount].coll:
                        poscount += 1
                    else:
                        gotcoll = True
        if get_value is not None:
            self._err_need_value(get_value)
        if self.pos[-1].coll and gotcoll:
            poscount += 1
        if poscount < req:
            sys.exit('too few positional arguments')

    def parse_dict(self, *args, **kw):
        '''
        Parse an argument list into a dictionary. Takes the same arguments as
        ``parse``.

        Returns a dictionary of arguments, formatted ``{flag: flaginfo}``. See
        the included examples for more info.
        '''
        res = {}
        for flag in self.flags.values():
            if flag.coll:
                if flag.value:
                    res[flag.flag] = []
                else:
                    res[flag.flag] = 0
            elif flag.value:
                res[flag.flag] = None
            else:
                res[flag.flag] = False
        for pos in self.pos:
            if pos.coll:
                res[pos.name] = []
            else:
                res[pos.name] = None
        posi = 0
        for tp, x, value in self.parse(*args, **kw):
            if tp == 'flag':
                if self.flags[x].coll:
                    if self.flags[x].value:
                        res[x].append(value)
                    else:
                        res[x] += 1
                else:
                    res[x] = value if self.flags[x].value else True
            else:
                if self.pos[posi].coll:
                    res[x].append(value)
                else:
                    res[x] = value
                    posi += 1
        if self.help:
            res.pop('h')
        return res
