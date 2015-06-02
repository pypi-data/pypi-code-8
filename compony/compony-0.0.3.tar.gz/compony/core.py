from compony.util import flatten, dictmerge

SPACES_PER_TAB = 2


class Element:
    attrs = None
    children = None
    tag = None
    self_closing = False
    multiline = True

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        if self.attrs is None:
            self.attrs = {}

        if self.children is None:
            self.children = []
        self.children = flatten(list(self.children))

        if self.tag is None:
            self.tag = 'div'


    def __eq__(self, other):
        return (
            self.tag == other.tag
            and self.attrs == other.attrs
            and list(self.children) == list(other.children)
        )


class AttrRequired(Exception):
    pass

class NotARegion(Exception):
    pass

class DoesNotExpectChildren(Exception):
    pass

class DoesNotExpectAttrs(Exception):
    pass


def create_element(tag, self_closing, multiline, *args):
    """
    (tag: str, self_closing: bool, multiline: bool,
        *args: List[Union[dict, Element]]) ->  Element
    """
    kwargs = {'tag': tag, 'self_closing': self_closing, 'multiline': multiline}
    if len(args) > 0:
        first_arg, rest_args = args[0], args[1:]
        if isinstance(first_arg, dict):
            kwargs['attrs'] = first_arg
            # children_element_functions = rest_args
            kwargs['children'] = rest_args
        else:
            kwargs['children'] = args
    return Element(**kwargs)



def to_html(component_tree, depth=0):
    """(element: Element) -> str"""

    element = to_element_tree(component_tree)

    if element is None:
        return ''
    elif isinstance(element, Element):

        attrs_str = ' '.join(['{}="{}"'.format(key, val)
                              for key, val in element.attrs.items()
                              if val is not None])

        if element.self_closing:
            return "\n{whitespace}<{tag}{attrs}/>".format(
                tag=element.tag,
                attrs= ' ' + attrs_str if attrs_str else '',
                whitespace= ' ' * (SPACES_PER_TAB * depth)
            )
        elif element.multiline is False:
            return "\n{whitespace}<{tag}{attrs}>{children}</{tag}>".format(
                children=to_html(element.children),
                tag=element.tag,
                attrs= ' ' + attrs_str if attrs_str else '',
                whitespace= ' ' * (SPACES_PER_TAB * depth)
            )
        else:
            return "\n{whitespace}<{tag}{attrs}>{children}\n{whitespace}</{tag}>".format(
                children=to_html(element.children, depth=depth+1),
                tag=element.tag,
                attrs= ' ' + attrs_str if attrs_str else '',
                whitespace= ' ' * (SPACES_PER_TAB * depth)
            )
    elif isinstance(element, str):
        return element
    else:
        # assume it's a list of elements
        return ''.join([to_html(e, depth=depth+1) for e in element])


class Component(object):

    xrays = None
    attrs = None
    children = None
    swappable = ()
    default_attrs = None

    def __init__(self, *args, swaps=None):

        if self.default_attrs is None:
            self.default_attrs = {}

        self.xrays = self.get_component_xrays()
        if not swaps:
            swaps = {}
        self.xrays.update({'swaps': swaps})

        self.attrs = self.default_attrs.copy()
        self.children = []
        if len(args) > 0:
            first_arg, rest_args = args[0], args[1:]
            if isinstance(first_arg, dict):
                self.attrs = dictmerge(self.attrs, first_arg)
                self.children = rest_args
            else:
                self.children = args

        self.children = flatten(list(self.children))

    def update_xrays(self, xrays):
        self.xrays.update(xrays)
        return self.xrays

    def get_component_xrays(self):
        return {}

    def swap(self, component_class):
        if component_class not in self.swappable:
            return component_class
        try:
            return self.xrays['swaps'][component_class]
        except KeyError:
            return component_class

    def merge(self, child_attrs):
        return dictmerge(self.attrs, child_attrs)


def to_element_tree(node, xrays={}):

    if isinstance(node, Element):
        transformed_children = []
        for child in node.children:
            transformed_children.append(to_element_tree(child, xrays))
        node.children = flatten(list(transformed_children))

    elif isinstance(node, Component):
        xrays = node.update_xrays(xrays)
        node = to_element_tree(node.render(), xrays)
        return node

    return node