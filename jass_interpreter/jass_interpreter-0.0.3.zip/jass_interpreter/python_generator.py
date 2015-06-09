import itertools
from operator import attrgetter, itemgetter
from parsimonious import NodeVisitor

from jass_interpreter.jass_parser import ascii_to_integer


#TODO: this should be a command line parameter!
from parsimonious.nodes import RegexNode

EMIT_DEBUG_STATEMENTS = True

def filter_non_empty_statements(stmt):
    # print(repr(stmt))
    return not stmt.is_empty

def indented(s):
    return "\n".join(map(lambda s1: "    " + s1, s.split("\n")))

class Statement(object):
    def __init__(self, text, assigned_variables=set(), declared_variables=set()):
        # declared/assigned variables are useful in fucntion definition
        # for managing scope of variables
        self.text = text
        self.declared_variables = declared_variables
        self.assigned_variables = assigned_variables

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.__class__.__qualname__ + "({},{},{})".format(self.text, self.declared_variables, self.assigned_variables)

    @property
    def is_empty(self):
        return self.text.strip() == ""

class ReturnStatement(Statement):
    def __str__(self):
        return "return " + super().__str__()


class Assignment(Statement):
    def __init__(self, name, value):
        super().__init__(text=name + " = " + str(value), assigned_variables={name})
        self.name = name
        self.value = value

class VariableDefinition(Statement):
    def __init__(self, name, initializer, is_array):
        has_init = bool(initializer)
        initializer = initializer if has_init else "= [None]*8192" if is_array else "= None"
        super().__init__(text=str(name) + " " + str(initializer), declared_variables={name}, assigned_variables={name} if has_init else set())
        self.name = name

class StatementBlock(object):
    def __init__(self, statements, join_str="\n"):
        self.statements = list(filter(filter_non_empty_statements, statements))
        self.join_str = join_str

    @property
    def declared_variables(self):
        _declared_variables = map(attrgetter("declared_variables"), self.statements)
        return set(itertools.chain(*_declared_variables))

    @property
    def assigned_variables(self):
        _assigned_variables = map(attrgetter("assigned_variables"), self.statements)
        return set(itertools.chain(*_assigned_variables))

    def __str__(self):
        return self.join_str.join(map(str, self.statements))

    def __iter__(self):
        return iter(self.statements)

    def __len__(self):
        return len(self.statements)

    def __repr__(self):
        return self.__class__.__qualname__ + "(\n" + str(self) + "\n)"

    @property
    def is_empty(self):
        return len(self.statements) == 0

class ConditionalBlock(StatementBlock):
    def __init__(self, statements, template="else{}", condition=""):
        super().__init__(statements)
        self.template = template
        self.condition = condition

    def __str__(self):
        if len(self.statements) == 0:
            return ""

        if_body = super().__str__()
        return self.template.format(self.condition) + "\n" + indented(if_body)

class ConditionalBlockIF(ConditionalBlock):
    def __init__(self, statements, template="else{}", condition=""):
        if len(statements) == 0:
            statements = [Statement("pass")]
        super().__init__(statements, template=template, condition=condition)

class ArgumentList(object):

    def __init__(self, arguments):
        if arguments[0] =="nothing":
            self.arguments = []
        else:
            self.arguments = [{"type": type_, "array": array_ == "array", "name": name_} for type_, array_, name_ in arguments]

    def __str__(self):
        if len(self.arguments) == 0:
            return ""
        else:
            return ", ".join('{name}:"{type}"'.format(name=a["name"], type=a["type"]) for a in self.arguments)

    @property
    def declared_variables(self):
        return list(map(itemgetter("name"), self.arguments))

class FunctionHeader(object):
    def __init__(self, name:"str", arguments: "{name:type}", return_type:"str"):
        self.name = name
        self.arguments = arguments
        self.return_type = return_type

    def __str__(self):
        return '\ndef {fn}({al})->"{rtype}":'.format(fn=str(self.name), al=str(self.arguments), rtype=str(self.return_type))

    @property
    def declared_variables(self):
        return self.arguments.declared_variables

    @property
    def assigned_variables(self):
        # all variables declared in the arguents list are treated as if they have been assigned to
        return self.arguments.declared_variables

class FunctionBody(object):
    def __init__(self, statements: StatementBlock):
        self.statements = statements

    def __str__(self):
        return indented(str(self.statements)) + "\n    pass\n"

    @property
    def declared_variables(self):
        return self.statements.declared_variables

    @property
    def assigned_variables(self):
        return self.statements.assigned_variables


class FunctionDefinition(object):
    def __init__(self, header: FunctionHeader, body: FunctionBody):
        self.header = header
        self.body = body

    def __str__(self):
        return str(self.header) +"\n" + self.nonlocals_as_globals + "\n" + str(self.body)

    @property
    def nonlocals_as_globals(self):
        return indented("\n".join(map(lambda nl: "global " + nl, self.nonlocals)))

    @property
    def nonlocals(self):
        return set(filter(lambda s: "[" not in s, self.assigned_variables - self.declared_variables))

    @property
    def declared_variables(self):
        return set(self.header.declared_variables) | set(self.body.declared_variables)

    @property
    def assigned_variables(self):
        return set(self.header.assigned_variables) | set(self.body.assigned_variables)

    @property
    def is_empty(self):
        # we cant omit functions just because they are useless for API reasons..
        return False

class JassToPyTransformer(NodeVisitor):

    def visit_program(self, node, children):
        _preamble = "# jass2->py3.4\n"
        children = map(str, children)

        return _preamble + ("".join(children))

    # def generic_visit(self, node, visited_children):
    #     #
    #     print("generic_visit:", node.expr_name)
    #     # print("generic_visit@[{}]".format(node.expr_name))
    #     # raise NotImplemented(node.expr_name)
    #     # return visited_children

    def visit_(self, node, children):
        if not node.text:
            return ""

        if children:
            try:
                return "".join(children)
            except:
                return children

        # TODO: node.text is definitely the wrong answer here, must fix
        return node.text

    def visit_name(self, node, children):
        return node.text.strip()

    def visit_integer_literal(self, node, children):
        return children[0]  # return the actual value

    def visit_integer_literal_regular(self, node, children):
        return int(node.text)

    def visit_integer_literal_hex(self, node, children):
        return int(node.text, base=16)

    def visit_integer_literal_ascii(self, node, children):
        return ascii_to_integer(children[1])

    def visit_kw_call(self, node, children):
        return ""

    def visit_call_statement(self, node, children):
        return Statement(children[1])

    def visit_float_literal(self, node, children):
        return float(node.text)

    def visit_expression(self, node, children):
        return str(children[0])

    def visit_statement(self, node, children):
        return children[1]

    def visit_statement_block(self, node, children):
        return StatementBlock(children)

    def visit_kw_if(self, node, children):
        return "if"

    def visit__(self, node, children):
        #visit optional whitespace
        return ""

    def visit_kw_then(self, node, children):
        return ":"

    def visit_if_header(self, node, children):
        _, kw_if, condition, kw_then, _ = children
        return kw_if + " " + str(condition) + kw_then

    def visit_if_else(self, node, children):
        try:
            _, kw_else, newline, if_body = children[0]
            return ConditionalBlock(if_body, template="else{}:", condition="")
        except IndexError:
            return StatementBlock(statements=[])

    def visit_if_then(self, node, children):
        head, body, else_if, else_block, end = children
        if_real = ConditionalBlockIF(body, condition=head, template="{}")
        return StatementBlock(list(itertools.chain([if_real], else_if, [else_block])), join_str="\n\n")

    def visit_empty_statement(self, node, children):
        return Statement("")

    def visit_kw_endif(self, node, children):
        return ""

    def visit_kw_elseif(self, node, children):
        return "elif"

    def visit_simple_expression(self, node, children):
        return children[0]

    def visit_binary_operation(self, node, children):
        return " ".join(map(str, children))

    def visit_elseif(self, node, children):
        return "\n".join(children)

    def visit_if_elseif_content(self, node, children):
        _, kw_elseif, expression, kw_then, newline, if_body = children
        return ConditionalBlock(if_body, template="elif {}:", condition=expression)


    def visit_newline(self, node, children):
        return "\n"


    def visit_simple_name(self, node, children):
        return node.children[0].text

    def visit_kw_left_parens(self, node, children):
        return "("

    def visit_kw_right_parens(self, node, children):
        return ")"

    def visit_call_expression(self, node, children):
        name, lp, expr, rp = children
        return "{fname}({args})".format(fname=name, args=expr)

    def visit_expression_list(self, node, children):
        return ", ".join(map(str, children))


    def visit_number(self, node, children):
        return children[0]

    def visit_any_statement_type(self, node, children):
        return children[0]

    def visit_if_body(self, node, children):
        return children[0]

    def visit_kw_local(self, node, children):
        return ""

    def visit_variable_declaration(self, node, children):
        # variable_declaration = qualifiers typed_var optional_initial_value?
        # typed_var = type_name _ kw_array? name

        # the only qualifier currently is "constant" but that is only enforced by convention is python (all-caps)
        quals, (typename,  kw_array, varname), initializer = children
        return VariableDefinition(varname, initializer, len(kw_array) > 0)

    def visit_local_declaration(self, node, children):
        return children[1]

    def visit_global_declaration(self, node, children):
        return children[1]

    def visit_global_declaration_or_empty_statement(self, node, children):
        return children[0]

    def visit_global_declaration_block(self, node, children):
        return StatementBlock(statements=children)
        # return "\n".join(map(str, children))

    def visit_typed_var(self, node, children):
        return children

    def visit_kw_endfunction(self, node, children):
        return ""

    def visit_return_statement(self, node, children):
        return ReturnStatement(text=children[1])

    def visit_bin_op(self, node, children):
        return children[0]

    def visit_un_op(self, node, children):
        return node.text

    def visit_any_literal(self, node, children):
        return children[0]

    def visit_string_literal(self, node, children):
        return node.text

    def visit_argument_list_component(self, node, children):
        try:
            return [children[0]] + children[1]
        except Exception:
            # single argument case
            # slice because the results needs to have same nesting as the default case
            return children[0:1]

    def visit_typed_var_with_comma(self, node,children):
        return children[1]

    def visit_argument_list(self, node, children):
        """  argument_list = kw_nothing / (( typed_var _ kw_comma _ )* typed_var)"""
        return ArgumentList(children[0])

    def visit_native_function_headers(self, node, children):
        # real function def
        #   _, quals, kw_function, function_name, kw_takes, argument_list, kw_returns, return_type, newline = children
        # native declarationdef
        quals, kw_native, function_name, kw_takes, argument_list, kw_returns, return_type = children

        # _function_headers = self.visit_function_headers(None, [None] + children + [None])
        _function_headers = FunctionHeader(function_name, argument_list, return_type)
        _function_body = FunctionBody(StatementBlock([Statement("raise NotImplemented")]))
        return FunctionDefinition(_function_headers, _function_body)

    def visit_function_headers(self, node, children):
        """_ kw_function name kw_takes argument_list kw_returns type_name newline"""
        _, quals, kw_function, function_name, kw_takes, argument_list, kw_returns, return_type, newline = children
        return FunctionHeader(function_name, argument_list, return_type)

    def visit_function_definition(self, node, children):
        header, body, end = children
        return FunctionDefinition(header, FunctionBody(body))

    def visit_globals_block(self, node, children):
        return children[2]

    def visit_set_statement(self, node, children):
        _, name, _, value = children
        return Assignment(name=name, value=value)

    def visit_typedef(self, node, children):
        kw_type, name, kw_extends, super_name = children
        return Statement("\nclass {name}({super}):\n    pass\n".format(name=name, super=super_name),
                         declared_variables={name},
                         assigned_variables={name})

    def visit_kw_extends(self, node, children):
        return children[0]

    def visit_kw_type(self, node, children):
        return children[0]

    def visit_kw_constant(self, node, children):
        return ""
    #
    # def visit_kw_private(self, node, children):
    #     return ""
    #
    # def visit_kw_public(self, node, children):
    #     return ""

    def visit_kw_null(self, node, children):
        return None

    def visit_loop(self, node, children):
        body = children[1]
        return Statement("while True:\n" + indented(str(body)) + "\n    pass\n",
                         declared_variables=body.declared_variables,
                         assigned_variables=body.assigned_variables)

    def visit_exitwhen(self, node, children):
        expr = children[1]
        return Statement("if {expr}:\n    break\n".format(expr=expr))

    def visit_degug_statement(self, node, children):
        if EMIT_DEBUG_STATEMENTS:
            return children[2]
        else:
            return "\n"

    def visit_unary_operation(self, node, children):
        return " ".join(children)

    def visit_function_dereference(self, node, children):
        kw_function, name = children
        return name

    def visit_optional_initial_value(self, node, children):
        return "= " + str(children[1])

    def visit_parens_expression(self, node, children):
        return " ".join(children)

    def visit_bracket_expression(self, node, children):
        return " ".join(children)

    def visit_kw_true(self, node, children):
        return "True"

    def visit_kw_false(self, node, children):
        return "False"

    def visit_null_literal(self, node, children):
        return "None"

    def visit_boolean_literal(self, node, children):
        return children[0]

    def visit_qualifiers(self, node, children):
        return ""

    def visit_type_name(self, node, children):
        return children[0]

    def visit_kw_comma(self, node, children):
        return ", "

    def visit_kw_set(self, node, children):
        return "set"

    def visit_kw_eq(self, node, children):
        return "set"

    def visit_kw_single_quote(self, node, children):
        return "'"

    def visit_kw_function(self, node, children):
        return "function"

    def visit_kw_loop(self, node, children):
        return "loop"

    def visit_kw_endloop(self, node, children):
        return "endloop"

    def visit_kw_exitwhen(self, node, children):
        return "exitwhen"

    def visit_kw_return(self, node, children):
        return "return"

    def visit_kw_takes(self, node, children):
        return "takes"

    def visit_kw_returns(self, node, children):
        return "returns"

    def visit_kw_array(self, node, children):
        return "array"

    def visit_kw_nothing(self, node, children):
        return children

    def visit_if_end(self, node, children):
        return ""

    def visit_if_elseif(self, node, children):
        #TODO: am i correct?
        return children

    def visit_function_end(self, node, children):
        return ""

    def visit_comment(self, node, children):
        return ""

    def visit_kw_else(self, node, children):
        return "else"

    def visit_kw_globals(self, node, children):
        return "globals"

    def visit_kw_endglobals(self, node, children):
        return "endglobals"

    def visit_if_else_content(self, node, children):
        return children

    def visit_kw_left_bracket(self, node, children):
        return "["

    def visit_kw_right_bracket(self, node, children):
        return "]"

    def visit_array_dereference(self, node, children):
        return "".join(children)

    def visit_kw_debug(self, node, children):
        return ""

    def visit_kw_native(self, node, children):
        return ""

    def visit_attribute_dereference(self, node, children):
        return node.text
