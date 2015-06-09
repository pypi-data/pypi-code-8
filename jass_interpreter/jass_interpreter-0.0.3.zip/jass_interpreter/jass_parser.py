from parsimonious import Grammar


def ascii_to_integer(ascii_integer: bytes):
    if not isinstance(ascii_integer, bytes):
        ascii_integer = bytes(ascii_integer, encoding="utf-8")
    if len(ascii_integer) == 1:
        return ascii_integer[0]
    elif len(ascii_integer) == 4:
        return ((ascii_integer[0] << 24) +
                (ascii_integer[1] << 16) +
                (ascii_integer[2] << 8) +
                (ascii_integer[3]))
    else:
        raise ValueError("ascii-integer must be either 4 or 1 bytes., given string has length %s" % len(ascii_integer))


class JassParser(object):
    grammar = Grammar(
        # TODO: FIXE: generating invalid empty else block without pass statement
        #       (preferable eliminate empty blocks, else make sure pass statement is present always..)
        # TODO: allow for escaped quotes inside strings

        # TODO?: constant qualifier for functions

        # TODO: persist jass comments in generated python code

        # TODO: user defined types (vjass compat?) (low priority)
        #   notice: actual usage of user defined types (jass2) is very limited, they are more like C typedefes not classes
        #   vjass types (calles structs) are a lot more powerful class like entities but that doesnt really matter
        #   as all vjass features can be reduced to pure jass2 via a precompiler

        # TODO: ensure operator precedence correctness (low priority)
        #   notice: low priority

        # TODO: improve variable scoping, support more than 2 levels (optional, goes beyond standard jass2 capabilities)

        # blocks and lines
        """
            program = statement_block+

            native_function_headers = qualifiers kw_native name kw_takes argument_list kw_returns type_name

            function_definition = function_headers function_body function_end
            function_headers = _ qualifiers kw_function name kw_takes argument_list kw_returns type_name newline
            argument_list = kw_nothing / argument_list_component
            argument_list_component = typed_var typed_var_with_comma*
            typed_var_with_comma = kw_comma typed_var
            function_body = statement_block
            function_end = _ kw_endfunction newline

            loop = kw_loop statement_block kw_endloop

            if_then = if_header if_body if_elseif if_else if_end
                if_header = _ kw_if expression kw_then newline
                if_body = statement_block
                if_else = if_else_content?
                if_elseif = if_elseif_content*
                if_elseif_content = _ kw_elseif expression kw_then newline if_body
                if_else_content = _ kw_else newline if_body
                if_end = _ kw_endif newline


            globals_block = "globals" newline global_declaration_block "endglobals" newline
            global_declaration_block = global_declaration_or_empty_statement *
            global_declaration_or_empty_statement = global_declaration / empty_statement
            global_declaration = _ variable_declaration newline?


            local_declaration = kw_local variable_declaration

            statement_block = statement*
            statement = _ any_statement_type newline?
            any_statement_type = degug_statement / loop / exitwhen / typedef / globals_block / native_function_headers /function_definition / if_then / call_statement / set_statement / local_declaration / return_statement / empty_statement
            call_statement = kw_call call_expression
            set_statement = kw_set name kw_eq expression
            variable_declaration = qualifiers typed_var optional_initial_value?
            optional_initial_value = kw_eq expression
            return_statement = kw_return expression?
            typed_var = type_name kw_array? name


            degug_statement = _ kw_debug statement

            exitwhen = kw_exitwhen expression
            qualifiers = kw_constant?
            typedef = kw_type simple_name kw_extends simple_name

        # complex expressions
            expression_list = ( expression ( kw_comma expression )* )?
            expression = binary_operation / simple_expression
            call_expression = name kw_left_parens expression_list kw_right_parens
            simple_expression = call_expression / function_dereference / unary_operation / parens_expression / any_literal / name
            name = array_dereference / simple_name
            parens_expression = kw_left_parens expression kw_right_parens
            bracket_expression = kw_left_bracket expression kw_right_bracket
            attribute_dereference = "." name
            array_dereference = simple_name (bracket_expression / attribute_dereference)+

            function_dereference = kw_function name


        # notice: simple expression bto avoid infinite recursion. #TODO: ensure this doesnt rule out some types of valid expressions
            binary_operation =  simple_expression bin_op expression
            unary_operation = un_op expression

            any_literal = number / string_literal / null_literal / boolean_literal
            number = float_literal / integer_literal
            string_literal = ~'[\"][^"]*[\"]' _

        # leaf nodes
            type_name  = simple_name _
            simple_name = ~"[-_a-zA-Z][-_a-zA-Z0-9]*" _
            integer_literal =  integer_literal_hex / integer_literal_ascii / integer_literal_regular
            integer_literal_regular = ~"[0-9][0-9]*" _
            integer_literal_hex = ~"0x[1-9a-f][0-9a-f]*"i _
            integer_literal_ascii = kw_single_quote ~"[^']{1}([^']{3})?" kw_single_quote _

            null_literal = kw_null
            boolean_literal = kw_true / kw_false
            kw_true = "true" _
            kw_false = "false" _

            float_literal = ~"[0-9][0-9]*" "." ~"[0-9]*" _
            un_op = ( "not" / "-" ) _
            bin_op = ("*" / "/" /"+" / "-" / "==" / "!=" / "and" / "or" / "<=" / ">=" / "<" / ">" ) _

            kw_local = "local" _
            kw_array = "array" _

            kw_function = "function" _
            kw_takes = "takes" _
            kw_returns = "returns" _
            kw_endfunction ="endfunction" _

            kw_if = "if" _
            kw_then = "then" _
            kw_elseif = "elseif" _
            kw_else = "else" _
            kw_endif = "endif" _

            kw_left_parens = "(" _
            kw_right_parens = ")" _

            kw_left_bracket = "[" _
            kw_right_bracket = "]" _

            empty_statement = "" _
            kw_nothing = "nothing" _
            kw_return = "return" _
            kw_call = "call" _
            kw_set = "set" _

            kw_eq = "=" _
            """ r"""
            comment = ~"//[^\r\n]*"
            """ """
            newline = (_ comment? "\\n") +
            _ = ~"[ \\t]*"
            kw_single_quote = "'"
            kw_comma = "," _
            kw_constant = "constant" _

            kw_type = "type" _
            kw_extends = "extends" _
            kw_null = "null" _
            kw_exitwhen = "exitwhen" _

            kw_loop = "loop" _
            kw_endloop = "endloop" _

            kw_debug = "debug" _
            kw_native = "native" _

        """)

    def parse(self, src, root_node="program"):
        return self.grammar[root_node].parse(src)





