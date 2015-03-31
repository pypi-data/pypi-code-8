"""
The Bookkeeper class.
"""

from __future__ import absolute_import

import sys, types, inspect, weakref

from rpython.flowspace.model import Constant
from rpython.annotator.model import (SomeOrderedDict,
    SomeString, SomeChar, SomeFloat, unionof, SomeInstance, SomeDict,
    SomeBuiltin, SomePBC, SomeInteger, TLS, SomeUnicodeCodePoint,
    s_None, s_ImpossibleValue, SomeBool, SomeTuple,
    SomeImpossibleValue, SomeUnicodeString, SomeList, HarmlesslyBlocked,
    SomeWeakRef, SomeByteArray, SomeConstantType, SomeProperty)
from rpython.annotator.classdef import InstanceSource, ClassDef
from rpython.annotator.listdef import ListDef, ListItem
from rpython.annotator.dictdef import DictDef
from rpython.annotator import description
from rpython.annotator.signature import annotationoftype
from rpython.annotator.argument import simple_args
from rpython.rlib.objectmodel import r_dict, r_ordereddict, Symbolic
from rpython.tool.algo.unionfind import UnionFind
from rpython.rtyper import extregistry


BUILTIN_ANALYZERS = {}

def analyzer_for(func):
    def wrapped(ann_func):
        BUILTIN_ANALYZERS[func] = ann_func
        return ann_func
    return wrapped

class Bookkeeper(object):
    """The log of choices that have been made while analysing the operations.
    It ensures that the same 'choice objects' will be returned if we ask
    again during reflowing.  Like ExecutionContext, there is an implicit
    Bookkeeper that can be obtained from a thread-local variable.

    Currently used for factories and user-defined classes."""

    def __setstate__(self, dic):
        self.__dict__.update(dic) # normal action
        self.register_builtins()

    def __init__(self, annotator):
        self.annotator = annotator
        self.policy = annotator.policy
        self.descs = {}          # map Python objects to their XxxDesc wrappers
        self.methoddescs = {}    # map (funcdesc, classdef) to the MethodDesc
        self.classdefs = []      # list of all ClassDefs
        self.seen_mutable = {}
        self.listdefs = {}       # map position_keys to ListDefs
        self.dictdefs = {}       # map position_keys to DictDefs
        self.immutable_cache = {}

        self.classpbc_attr_families = {} # {'attr': UnionFind(ClassAttrFamily)}
        self.frozenpbc_attr_families = UnionFind(description.FrozenAttrFamily)
        self.pbc_maximal_call_families = UnionFind(description.CallFamily)

        self.emulated_pbc_calls = {}
        self.all_specializations = {}       # {FuncDesc: specialization-info}
        self.pending_specializations = []   # list of callbacks
        self.external_class_cache = {}      # cache of ExternalType classes

        self.needs_generic_instantiate = {}
        self.thread_local_fields = set()

        self.register_builtins()

    def register_builtins(self):
        import rpython.annotator.builtin  # for side-effects
        from rpython.annotator.exception import standardexceptions
        for cls in standardexceptions:
            self.getuniqueclassdef(cls)

    def enter(self, position_key):
        """Start of an operation.
        The operation is uniquely identified by the given key."""
        assert not hasattr(self, 'position_key'), "don't call enter() nestedly"
        self.position_key = position_key
        TLS.bookkeeper = self

    def leave(self):
        """End of an operation."""
        del TLS.bookkeeper
        del self.position_key

    def compute_at_fixpoint(self):
        # getbookkeeper() needs to work during this function, so provide
        # one with a dummy position
        self.enter(None)
        try:
            def call_sites():
                newblocks = self.annotator.added_blocks
                if newblocks is None:
                    newblocks = self.annotator.annotated  # all of them
                annotation = self.annotator.annotation
                for block in newblocks:
                    for op in block.operations:
                        if op.opname in ('simple_call', 'call_args'):
                            yield op

                        # some blocks are partially annotated
                        if annotation(op.result) is None:
                            break   # ignore the unannotated part

            for call_op in call_sites():
                self.consider_call_site(call_op)

            for pbc, args_s in self.emulated_pbc_calls.itervalues():
                args = simple_args(args_s)
                pbc.consider_call_site(args, s_ImpossibleValue, None)
            self.emulated_pbc_calls = {}
        finally:
            self.leave()

    def check_no_flags_on_instances(self):
        # sanity check: no flags attached to heap stored instances
        seen = set()

        def check_no_flags(s_value_or_def):
            if isinstance(s_value_or_def, SomeInstance):
                assert not s_value_or_def.flags, "instance annotation with flags escaped to the heap"
                check_no_flags(s_value_or_def.classdef)
            elif isinstance(s_value_or_def, SomeList):
                check_no_flags(s_value_or_def.listdef.listitem)
            elif isinstance(s_value_or_def, SomeDict):
                check_no_flags(s_value_or_def.dictdef.dictkey)
                check_no_flags(s_value_or_def.dictdef.dictvalue)
            elif isinstance(s_value_or_def, SomeTuple):
                for s_item in s_value_or_def.items:
                    check_no_flags(s_item)
            elif isinstance(s_value_or_def, ClassDef):
                if s_value_or_def in seen:
                    return
                seen.add(s_value_or_def)
                for attr in s_value_or_def.attrs.itervalues():
                    s_attr = attr.s_value
                    check_no_flags(s_attr)
            elif isinstance(s_value_or_def, ListItem):
                if s_value_or_def in seen:
                    return
                seen.add(s_value_or_def)
                check_no_flags(s_value_or_def.s_value)

        for clsdef in self.classdefs:
            check_no_flags(clsdef)

    def consider_call_site(self, call_op):
        from rpython.rtyper.llannotation import SomeLLADTMeth, lltype_to_annotation
        annotation = self.annotator.annotation
        s_callable = annotation(call_op.args[0])
        args_s = [annotation(arg) for arg in call_op.args[1:]]
        if isinstance(s_callable, SomeLLADTMeth):
            adtmeth = s_callable
            s_callable = self.immutablevalue(adtmeth.func)
            args_s = [lltype_to_annotation(adtmeth.ll_ptrtype)] + args_s
        if isinstance(s_callable, SomePBC):
            s_result = annotation(call_op.result)
            if s_result is None:
                s_result = s_ImpossibleValue
            args = call_op.build_args(args_s)
            s_callable.consider_call_site(args, s_result, call_op)

    def getuniqueclassdef(self, cls):
        """Get the ClassDef associated with the given user cls.
        Avoid using this!  It breaks for classes that must be specialized.
        """
        assert cls is not object
        desc = self.getdesc(cls)
        return desc.getuniqueclassdef()

    def getlistdef(self, **flags_if_new):
        """Get the ListDef associated with the current position."""
        try:
            listdef = self.listdefs[self.position_key]
        except KeyError:
            listdef = self.listdefs[self.position_key] = ListDef(self)
            listdef.listitem.__dict__.update(flags_if_new)
        return listdef

    def newlist(self, *s_values, **flags):
        """Make a SomeList associated with the current position, general
        enough to contain the s_values as items."""
        listdef = self.getlistdef(**flags)
        for s_value in s_values:
            listdef.generalize(s_value)
        if flags:
            assert flags.keys() == ['range_step']
            listdef.generalize_range_step(flags['range_step'])
        return SomeList(listdef)

    def getdictdef(self, is_r_dict=False, force_non_null=False):
        """Get the DictDef associated with the current position."""
        try:
            dictdef = self.dictdefs[self.position_key]
        except KeyError:
            dictdef = DictDef(self, is_r_dict=is_r_dict,
                              force_non_null=force_non_null)
            self.dictdefs[self.position_key] = dictdef
        return dictdef

    def newdict(self):
        """Make a so-far empty SomeDict associated with the current
        position."""
        return SomeDict(self.getdictdef())

    def immutablevalue(self, x):
        """The most precise SomeValue instance that contains the
        immutable value x."""
        # convert unbound methods to the underlying function
        if hasattr(x, 'im_self') and x.im_self is None:
            x = x.im_func
            assert not hasattr(x, 'im_self')
        tp = type(x)
        if issubclass(tp, Symbolic): # symbolic constants support
            result = x.annotation()
            result.const_box = Constant(x)
            return result
        if tp is bool:
            result = SomeBool()
        elif tp is int:
            result = SomeInteger(nonneg = x>=0)
        elif tp is long:
            if -sys.maxint-1 <= x <= sys.maxint:
                x = int(x)
                result = SomeInteger(nonneg = x>=0)
            else:
                raise Exception("seeing a prebuilt long (value %s)" % hex(x))
        elif issubclass(tp, str): # py.lib uses annotated str subclasses
            no_nul = not '\x00' in x
            if len(x) == 1:
                result = SomeChar(no_nul=no_nul)
            else:
                result = SomeString(no_nul=no_nul)
        elif tp is unicode:
            if len(x) == 1:
                result = SomeUnicodeCodePoint()
            else:
                result = SomeUnicodeString()
        elif tp is bytearray:
            result = SomeByteArray()
        elif tp is tuple:
            result = SomeTuple(items = [self.immutablevalue(e) for e in x])
        elif tp is float:
            result = SomeFloat()
        elif tp is list:
            key = Constant(x)
            try:
                return self.immutable_cache[key]
            except KeyError:
                result = SomeList(ListDef(self, s_ImpossibleValue))
                self.immutable_cache[key] = result
                for e in x:
                    result.listdef.generalize(self.immutablevalue(e))
                result.const_box = key
                return result
        elif (tp is dict or tp is r_dict or
              tp is SomeOrderedDict.knowntype or tp is r_ordereddict):
            key = Constant(x)
            try:
                return self.immutable_cache[key]
            except KeyError:
                if tp is SomeOrderedDict.knowntype or tp is r_ordereddict:
                    cls = SomeOrderedDict
                else:
                    cls = SomeDict
                is_r_dict = issubclass(tp, r_dict)
                result = cls(DictDef(self,
                                        s_ImpossibleValue,
                                        s_ImpossibleValue,
                                        is_r_dict = is_r_dict))
                self.immutable_cache[key] = result
                if is_r_dict:
                    s_eqfn = self.immutablevalue(x.key_eq)
                    s_hashfn = self.immutablevalue(x.key_hash)
                    result.dictdef.dictkey.update_rdict_annotations(s_eqfn,
                                                                    s_hashfn)
                seen_elements = 0
                while seen_elements != len(x):
                    items = x.items()
                    for ek, ev in items:
                        result.dictdef.generalize_key(self.immutablevalue(ek))
                        result.dictdef.generalize_value(self.immutablevalue(ev))
                        result.dictdef.seen_prebuilt_key(ek)
                    seen_elements = len(items)
                    # if the dictionary grew during the iteration,
                    # start over again
                result.const_box = key
                return result
        elif tp is weakref.ReferenceType:
            x1 = x()
            if x1 is None:
                result = SomeWeakRef(None)    # dead weakref
            else:
                s1 = self.immutablevalue(x1)
                assert isinstance(s1, SomeInstance)
                result = SomeWeakRef(s1.classdef)
        elif tp is property:
            return SomeProperty(x)
        elif ishashable(x) and x in BUILTIN_ANALYZERS:
            _module = getattr(x,"__module__","unknown")
            result = SomeBuiltin(BUILTIN_ANALYZERS[x], methodname="%s.%s" % (_module, x.__name__))
        elif extregistry.is_registered(x):
            entry = extregistry.lookup(x)
            result = entry.compute_annotation_bk(self)
        elif tp is type:
            result = SomeConstantType(x, self)
        elif callable(x):
            if hasattr(x, 'im_self') and hasattr(x, 'im_func'):
                # on top of PyPy, for cases like 'l.append' where 'l' is a
                # global constant list, the find_method() returns non-None
                s_self = self.immutablevalue(x.im_self)
                result = s_self.find_method(x.im_func.__name__)
            elif hasattr(x, '__self__') and x.__self__ is not None:
                # for cases like 'l.append' where 'l' is a global constant list
                s_self = self.immutablevalue(x.__self__)
                result = s_self.find_method(x.__name__)
                assert result is not None
            else:
                result = None
            if result is None:
                result = SomePBC([self.getdesc(x)])
        elif hasattr(x, '_freeze_'):
            assert x._freeze_() is True
            # user-defined classes can define a method _freeze_(), which
            # is called when a prebuilt instance is found.  If the method
            # returns True, the instance is considered immutable and becomes
            # a SomePBC().  Otherwise it's just SomeInstance().
            result = SomePBC([self.getdesc(x)])
        elif hasattr(x, '__class__') \
                 and x.__class__.__module__ != '__builtin__':
            if hasattr(x, '_cleanup_'):
                x._cleanup_()
            self.see_mutable(x)
            result = SomeInstance(self.getuniqueclassdef(x.__class__))
        elif x is None:
            return s_None
        else:
            raise Exception("Don't know how to represent %r" % (x,))
        result.const = x
        return result

    def getdesc(self, pyobj):
        # get the XxxDesc wrapper for the given Python object, which must be
        # one of:
        #  * a user-defined Python function
        #  * a Python type or class (but not a built-in one like 'int')
        #  * a user-defined bound or unbound method object
        #  * a frozen pre-built constant (with _freeze_() == True)
        #  * a bound method of a frozen pre-built constant
        try:
            return self.descs[pyobj]
        except KeyError:
            if isinstance(pyobj, types.FunctionType):
                result = description.FunctionDesc(self, pyobj)
            elif isinstance(pyobj, (type, types.ClassType)):
                if pyobj is object:
                    raise Exception("ClassDesc for object not supported")
                if pyobj.__module__ == '__builtin__': # avoid making classdefs for builtin types
                    result = self.getfrozen(pyobj)
                else:
                    result = description.ClassDesc(self, pyobj)
            elif isinstance(pyobj, types.MethodType):
                if pyobj.im_self is None:   # unbound
                    return self.getdesc(pyobj.im_func)
                if hasattr(pyobj.im_self, '_cleanup_'):
                    pyobj.im_self._cleanup_()
                if hasattr(pyobj.im_self, '_freeze_'):  # method of frozen
                    assert pyobj.im_self._freeze_() is True
                    result = description.MethodOfFrozenDesc(self,
                        self.getdesc(pyobj.im_func),            # funcdesc
                        self.getdesc(pyobj.im_self))            # frozendesc
                else: # regular method
                    origincls, name = origin_of_meth(pyobj)
                    self.see_mutable(pyobj.im_self)
                    assert pyobj == getattr(pyobj.im_self, name), (
                        "%r is not %s.%s ??" % (pyobj, pyobj.im_self, name))
                    # emulate a getattr to make sure it's on the classdef
                    classdef = self.getuniqueclassdef(pyobj.im_class)
                    classdef.find_attribute(name)
                    result = self.getmethoddesc(
                        self.getdesc(pyobj.im_func),            # funcdesc
                        self.getuniqueclassdef(origincls),      # originclassdef
                        classdef,                               # selfclassdef
                        name)
            else:
                # must be a frozen pre-built constant, but let's check
                if hasattr(pyobj, '_freeze_'):
                    assert pyobj._freeze_() is True
                else:
                    if hasattr(pyobj, '__call__'):
                        msg = "object with a __call__ is not RPython"
                    else:
                        msg = "unexpected prebuilt constant"
                    raise Exception("%s: %r" % (msg, pyobj))
                result = self.getfrozen(pyobj)
            self.descs[pyobj] = result
            return result

    def have_seen(self, x):
        # this might need to expand some more.
        if x in self.descs:
            return True
        elif (x.__class__, x) in self.seen_mutable:
            return True
        else:
            return False

    def getfrozen(self, pyobj):
        return description.FrozenDesc(self, pyobj)

    def getmethoddesc(self, funcdesc, originclassdef, selfclassdef, name,
                      flags={}):
        flagskey = flags.items()
        flagskey.sort()
        key = funcdesc, originclassdef, selfclassdef, name, tuple(flagskey)
        try:
            return self.methoddescs[key]
        except KeyError:
            result = description.MethodDesc(self, funcdesc, originclassdef,
                                            selfclassdef, name, flags)
            self.methoddescs[key] = result
            return result

    def see_mutable(self, x):
        key = (x.__class__, x)
        if key in self.seen_mutable:
            return
        clsdef = self.getuniqueclassdef(x.__class__)
        self.seen_mutable[key] = True
        self.event('mutable', x)
        source = InstanceSource(self, x)
        for attr in source.all_instance_attributes():
            clsdef.add_source_for_attribute(attr, source) # can trigger reflowing

    def valueoftype(self, t):
        return annotationoftype(t, self)

    def get_classpbc_attr_families(self, attrname):
        """Return the UnionFind for the ClassAttrFamilies corresponding to
        attributes of the given name.
        """
        map = self.classpbc_attr_families
        try:
            access_sets = map[attrname]
        except KeyError:
            access_sets = map[attrname] = UnionFind(description.ClassAttrFamily)
        return access_sets

    def pbc_getattr(self, pbc, s_attr):
        assert s_attr.is_constant()
        attr = s_attr.const

        descs = list(pbc.descriptions)
        first = descs[0]
        if len(descs) == 1:
            return first.s_read_attribute(attr)

        change = first.mergeattrfamilies(descs[1:], attr)
        attrfamily = first.getattrfamily(attr)

        position = self.position_key
        attrfamily.read_locations[position] = True

        actuals = []
        for desc in descs:
            actuals.append(desc.s_read_attribute(attr))
        s_result = unionof(*actuals)

        s_oldvalue = attrfamily.get_s_value(attr)
        attrfamily.set_s_value(attr, unionof(s_result, s_oldvalue))

        if change:
            for position in attrfamily.read_locations:
                self.annotator.reflowfromposition(position)

        if isinstance(s_result, SomeImpossibleValue):
            for desc in descs:
                try:
                    attrs = desc.read_attribute('_attrs_')
                except AttributeError:
                    continue
                if isinstance(attrs, Constant):
                    attrs = attrs.value
                if attr in attrs:
                    raise HarmlesslyBlocked("getattr on enforced attr")

        return s_result

    def pbc_call(self, pbc, args, emulated=None):
        """Analyse a call to a SomePBC() with the given args (list of
        annotations).
        """
        descs = list(pbc.descriptions)
        first = descs[0]
        first.mergecallfamilies(*descs[1:])

        if emulated is None:
            whence = self.position_key
            # fish the existing annotation for the result variable,
            # needed by some kinds of specialization.
            fn, block, i = self.position_key
            op = block.operations[i]
            s_previous_result = self.annotator.annotation(op.result)
            if s_previous_result is None:
                s_previous_result = s_ImpossibleValue
        else:
            if emulated is True:
                whence = None
            else:
                whence = emulated # callback case
            op = None
            s_previous_result = s_ImpossibleValue

        def schedule(graph, inputcells):
            return self.annotator.recursivecall(graph, whence, inputcells)

        results = []
        for desc in descs:
            results.append(desc.pycall(schedule, args, s_previous_result, op))
        s_result = unionof(*results)
        return s_result

    def emulate_pbc_call(self, unique_key, pbc, args_s, replace=[], callback=None):
        emulate_enter = not hasattr(self, 'position_key')
        if emulate_enter:
            self.enter(None)
        try:
            emulated_pbc_calls = self.emulated_pbc_calls
            prev = [unique_key]
            prev.extend(replace)
            for other_key in prev:
                if other_key in emulated_pbc_calls:
                    del emulated_pbc_calls[other_key]
            emulated_pbc_calls[unique_key] = pbc, args_s

            args = simple_args(args_s)
            if callback is None:
                emulated = True
            else:
                emulated = callback
            return self.pbc_call(pbc, args, emulated=emulated)
        finally:
            if emulate_enter:
                self.leave()

    def _find_current_op(self, opname=None, arity=None, pos=None, s_type=None):
        """ Find operation that is currently being annotated. Do some
        sanity checks to see whether the correct op was found."""
        # XXX XXX HACK HACK HACK
        fn, block, i = self.position_key
        op = block.operations[i]
        if opname is not None:
            assert op.opname == opname
        if arity is not None:
            assert len(op.args) == arity
        if pos is not None:
            assert self.annotator.binding(op.args[pos]) == s_type
        return op

    def whereami(self):
        return self.annotator.whereami(self.position_key)

    def event(self, what, x):
        return self.annotator.policy.event(self, what, x)

    def warning(self, msg):
        return self.annotator.warning(msg)

def origin_of_meth(boundmeth):
    func = boundmeth.im_func
    candname = func.func_name
    for cls in inspect.getmro(boundmeth.im_class):
        dict = cls.__dict__
        if dict.get(candname) is func:
            return cls, candname
        for name, value in dict.iteritems():
            if value is func:
                return cls, name
    raise Exception("could not match bound-method to attribute name: %r" % (boundmeth,))

def ishashable(x):
    try:
        hash(x)
    except TypeError:
        return False
    else:
        return True

# get current bookkeeper

def getbookkeeper():
    """Get the current Bookkeeper.
    Only works during the analysis of an operation."""
    try:
        return TLS.bookkeeper
    except AttributeError:
        return None

def immutablevalue(x):
    return getbookkeeper().immutablevalue(x)
