#     Copyright 2015, Kay Hayen, mailto:kay.hayen@gmail.com
#
#     Part of "Nuitka", an optimizing Python compiler that is compatible and
#     integrates with CPython, but also works on its own.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#
""" Reformulation of assignment statements.

Consult the developer manual for information. TODO: Add ability to sync
source code comments with developer manual sections.

"""

from nuitka import Utils
from nuitka.nodes.AssignNodes import (
    StatementAssignmentAttribute,
    StatementAssignmentSlice,
    StatementAssignmentSubscript,
    StatementAssignmentVariable,
    StatementDelAttribute,
    StatementDelSlice,
    StatementDelSubscript,
    StatementDelVariable,
    StatementReleaseVariable
)
from nuitka.nodes.AttributeNodes import ExpressionAttributeLookup
from nuitka.nodes.BuiltinIteratorNodes import (
    ExpressionBuiltinIter1,
    ExpressionSpecialUnpack,
    StatementSpecialUnpackCheck
)
from nuitka.nodes.BuiltinTypeNodes import ExpressionBuiltinList
from nuitka.nodes.ComparisonNodes import ExpressionComparisonIsNOT
from nuitka.nodes.ConditionalNodes import StatementConditional
from nuitka.nodes.ConstantRefNodes import ExpressionConstantRef
from nuitka.nodes.OperatorNodes import ExpressionOperationBinaryInplace
from nuitka.nodes.SliceNodes import ExpressionSliceLookup, ExpressionSliceObject
from nuitka.nodes.StatementNodes import StatementsSequence
from nuitka.nodes.SubscriptNodes import ExpressionSubscriptLookup
from nuitka.nodes.VariableRefNodes import (
    ExpressionTargetTempVariableRef,
    ExpressionTargetVariableRef,
    ExpressionTempVariableRef,
    ExpressionVariableRef
)

from .Helpers import (
    buildNode,
    getKind,
    makeSequenceCreationOrConstant,
    makeStatementsSequenceFromStatement,
    makeStatementsSequenceOrStatement,
    makeTryFinallyStatement,
    mangleName
)


def buildExtSliceNode(provider, node, source_ref):
    elements = []

    for dim in node.slice.dims:
        dim_kind = getKind(dim)

        if dim_kind == "Slice":
            lower = buildNode(provider, dim.lower, source_ref, True)
            upper = buildNode(provider, dim.upper, source_ref, True)
            step = buildNode(provider, dim.step, source_ref, True)

            element = ExpressionSliceObject(
                lower      = lower,
                upper      = upper,
                step       = step,
                source_ref = source_ref
            )
        elif dim_kind == "Ellipsis":
            element = ExpressionConstantRef(
                constant      = Ellipsis,
                source_ref    = source_ref,
                user_provided = True
            )
        elif dim_kind == "Index":
            element = buildNode(
                provider   = provider,
                node       = dim.value,
                source_ref = source_ref
            )
        else:
            assert False, dim

        elements.append(element)

    return makeSequenceCreationOrConstant(
        sequence_kind = "tuple",
        elements      = elements,
        source_ref    = source_ref
    )


def buildAssignmentStatementsFromDecoded(provider, kind, detail, source,
                                         source_ref):
    # This is using many variable names on purpose, so as to give names to the
    # unpacked detail values, and has many branches due to the many cases
    # dealt with, pylint: disable=R0912,R0914

    if kind == "Name":
        variable_ref = detail

        return StatementAssignmentVariable(
            variable_ref = variable_ref,
            source       = source,
            source_ref   = source_ref
        )
    elif kind == "Attribute":
        lookup_source, attribute_name = detail

        return StatementAssignmentAttribute(
            expression     = lookup_source,
            attribute_name = attribute_name,
            source         = source,
            source_ref     = source_ref
        )
    elif kind == "Subscript":
        subscribed, subscript = detail

        return StatementAssignmentSubscript(
            expression = subscribed,
            subscript  = subscript,
            source     = source,
            source_ref = source_ref
        )
    elif kind == "Slice":
        lookup_source, lower, upper = detail

        # For Python3 there is no slicing operation, this is always done
        # with subscript using a slice object. For Python2, it is only done
        # if no "step" is provided.
        use_sliceobj = Utils.python_version >= 300

        if use_sliceobj:
            return StatementAssignmentSubscript(
                expression = lookup_source,
                source     = source,
                subscript  = ExpressionSliceObject(
                    lower      = lower,
                    upper      = upper,
                    step       = None,
                    source_ref = source_ref
                ),
                source_ref = source_ref
            )

        else:
            return StatementAssignmentSlice(
                expression = lookup_source,
                lower      = lower,
                upper      = upper,
                source     = source,
                source_ref = source_ref
            )
    elif kind == "Tuple":
        temp_scope = provider.allocateTempScope("tuple_unpack")

        source_iter_var = provider.allocateTempVariable(
            temp_scope = temp_scope,
            name       = "source_iter"
        )

        statements = [
            StatementAssignmentVariable(
                variable_ref = ExpressionTargetTempVariableRef(
                    variable   = source_iter_var,
                    source_ref = source_ref
                ),
                source       = ExpressionBuiltinIter1(
                    value      = source,
                    source_ref = source_ref
                ),
                source_ref   = source_ref
            )
        ]

        element_vars = [
            provider.allocateTempVariable(
                temp_scope = temp_scope,
                name       = "element_%d" % (
                    element_index + 1
                )
            )
            for element_index in
            range(len(detail))
        ]

        starred = False

        for element_index, element in enumerate(detail):
            element_var = element_vars[element_index]

            if element[0] != "Starred":
                statements.append(
                    StatementAssignmentVariable(
                        variable_ref = ExpressionTargetTempVariableRef(
                            variable   = element_var,
                            source_ref = source_ref
                        ),
                        source       = ExpressionSpecialUnpack(
                            value      = ExpressionTempVariableRef(
                                variable   = source_iter_var,
                                source_ref = source_ref
                            ),
                            count      = element_index + 1,
                            source_ref = source_ref
                        ),
                        source_ref   = source_ref
                    )
                )
            else:
                starred = True

                statements.append(
                    StatementAssignmentVariable(
                        variable_ref = ExpressionTargetTempVariableRef(
                            variable   = element_var,
                            source_ref = source_ref
                        ),
                        source       = ExpressionBuiltinList(
                            value      = ExpressionTempVariableRef(
                                variable   = source_iter_var,
                                source_ref = source_ref
                            ),
                            source_ref = source_ref
                        ),
                        source_ref   = source_ref
                    )
                )

        if not starred:
            statements.append(
                StatementSpecialUnpackCheck(
                    iterator   = ExpressionTempVariableRef(
                        variable   = source_iter_var,
                        source_ref = source_ref
                    ),
                    count      = len(detail),
                    source_ref = source_ref
                )
            )

        for element_index, element in enumerate(detail):
            if element[0] == "Starred":
                element = element[1]

            element_var = element_vars[element_index]

            statements.append(
                buildAssignmentStatementsFromDecoded(
                    provider   = provider,
                    kind       = element[0],
                    detail     = element[1],
                    source     = ExpressionTempVariableRef(
                        variable   = element_var,
                        source_ref = source_ref
                    ),
                    source_ref = source_ref
                )
            )

        final_statements = []

        final_statements.append(
            StatementReleaseVariable(
                variable   = source_iter_var,
                tolerant   = True,
                source_ref = source_ref
            )
        )

        # TODO: In that order, or reversed.
        for element_var in element_vars:
            final_statements.append(
                StatementReleaseVariable(
                    variable   = element_var,
                    tolerant   = True,
                    source_ref = source_ref
                )
            )

        return makeTryFinallyStatement(
            tried      = statements,
            final      = final_statements,
            source_ref = source_ref
        )
    else:
        assert False, (kind, source_ref, detail)


def buildAssignmentStatements(provider, node, source, source_ref,
                              allow_none = False, temp_provider = None):
    if node is None and allow_none:
        return None

    if temp_provider is None:
        temp_provider = provider

    # We don't allow None, as we handled that above, and so we know it must
    # be a tuple, pylint: disable=W0633
    kind, detail = decodeAssignTarget(
        provider   = provider,
        node       = node,
        source_ref = source_ref
    )

    return buildAssignmentStatementsFromDecoded(
        provider   = temp_provider,
        kind       = kind,
        detail     = detail,
        source     = source,
        source_ref = source_ref
    )


def decodeAssignTarget(provider, node, source_ref, allow_none = False):
    # Many cases to deal with, because of the different assign targets,
    # pylint: disable=R0911,R0912

    if node is None and allow_none:
        return None

    if hasattr(node, "ctx"):
        assert getKind(node.ctx) in ("Store", "Del")

    kind = getKind(node)

    if type(node) is str:
        return "Name", ExpressionTargetVariableRef(
            variable_name = mangleName(node, provider),
            source_ref    = source_ref
        )
    elif kind == "Name":
        return kind, ExpressionTargetVariableRef(
            variable_name = mangleName(node.id, provider),
            source_ref    = source_ref
        )
    elif kind == "Attribute":
        return kind, (
            buildNode(provider, node.value, source_ref),
            node.attr
        )
    elif kind == "Subscript":
        slice_kind = getKind(node.slice)

        if slice_kind == "Index":
            return "Subscript", (
                buildNode(provider, node.value, source_ref),
                buildNode(provider, node.slice.value, source_ref)
            )
        elif slice_kind == "Slice":
            lower = buildNode(provider, node.slice.lower, source_ref, True)
            upper = buildNode(provider, node.slice.upper, source_ref, True)

            if node.slice.step is not None:
                step = buildNode(provider, node.slice.step, source_ref)

                return "Subscript", (
                    buildNode(provider, node.value, source_ref),
                    ExpressionSliceObject(
                        lower      = lower,
                        upper      = upper,
                        step       = step,
                        source_ref = source_ref
                    )
                )
            else:
                return "Slice", (
                    buildNode(provider, node.value, source_ref),
                    lower,
                    upper
                )
        elif slice_kind == "ExtSlice":
            return "Subscript", (
                buildNode(provider, node.value, source_ref),
                buildExtSliceNode(provider, node, source_ref)
            )
        elif slice_kind == "Ellipsis":
            return "Subscript", (
                buildNode(provider, node.value, source_ref),
                ExpressionConstantRef(
                    constant   = Ellipsis,
                    source_ref = source_ref
                )
            )
        else:
            assert False, slice_kind
    elif kind in ("Tuple", "List"):
        return "Tuple", tuple(
            decodeAssignTarget(
                provider   = provider,
                node       = sub_node,
                source_ref = source_ref,
                allow_none = False
            )
            for sub_node in
            node.elts
        )
    elif kind == "Starred":
        return "Starred", decodeAssignTarget(
            provider   = provider,
            node       = node.value,
            source_ref = source_ref,
            allow_none = False
        )
    else:
        assert False, (source_ref, kind)


def buildAssignNode(provider, node, source_ref):
    assert len(node.targets) >= 1, source_ref

    # Evaluate the right hand side first, so it can get names provided
    # before the left hand side exists.
    source = buildNode(provider, node.value, source_ref)

    if len(node.targets) == 1:
        # Simple assignment case, one source, one target.

        return buildAssignmentStatements(
            provider   = provider,
            node       = node.targets[0],
            source     = source,
            source_ref = source_ref
        )
    else:
        # Complex assignment case, one source, but multiple targets. We keep the
        # source in a temporary variable, and then assign from it multiple
        # times.

        temp_scope = provider.allocateTempScope("assign_unpack")

        tmp_source = provider.allocateTempVariable(
            temp_scope = temp_scope,
            name       = "assign_source"
        )

        statements = [
            StatementAssignmentVariable(
                variable_ref = ExpressionTargetTempVariableRef(
                    variable   = tmp_source,
                    source_ref = source_ref
                ),
                source       = source,
                source_ref   = source_ref
            )
        ]

        for target in node.targets:
            statements.append(
                buildAssignmentStatements(
                    provider   = provider,
                    node       = target,
                    source     = ExpressionTempVariableRef(
                        variable   = tmp_source,
                        source_ref = source_ref
                    ),
                    source_ref = source_ref
                )
            )

        final_statements = StatementReleaseVariable(
            variable   = tmp_source,
            tolerant   = True,
            source_ref = source_ref
        )

        return makeTryFinallyStatement(
            tried      = statements,
            final      = final_statements,
            source_ref = source_ref
        )


def buildDeleteStatementFromDecoded(kind, detail, source_ref):
    if kind in ("Name", "Name_Exception"):
        # Note: Name_Exception is a "del" for exception handlers that doesn't
        # insist on the variable being defined, user code may do it too, and
        # that will be fine, so make that tolerant.
        variable_ref = detail

        return StatementDelVariable(
            variable_ref = variable_ref,
            tolerant     = kind == "Name_Exception",
            source_ref   = source_ref
        )
    elif kind == "Attribute":
        lookup_source, attribute_name = detail

        return StatementDelAttribute(
            expression     = lookup_source,
            attribute_name = attribute_name,
            source_ref     = source_ref
        )
    elif kind == "Subscript":
        subscribed, subscript = detail

        return StatementDelSubscript(
            expression = subscribed,
            subscript  = subscript,
            source_ref = source_ref
        )
    elif kind == "Slice":
        lookup_source, lower, upper = detail

        use_sliceobj = Utils.python_version >= 300

        if use_sliceobj:
            return StatementDelSubscript(
                expression = lookup_source,
                subscript  = ExpressionSliceObject(
                    lower      = lower,
                    upper      = upper,
                    step       = None,
                    source_ref = source_ref
                ),
                source_ref = source_ref
            )
        else:
            return StatementDelSlice(
                expression = lookup_source,
                lower      = lower,
                upper      = upper,
                source_ref = source_ref
            )
    elif kind == "Tuple":
        result = []

        for sub_node in detail:
            result.append(
                buildDeleteStatementFromDecoded(
                    kind       = sub_node[0],
                    detail     = sub_node[1],
                    source_ref = source_ref
                )
            )

        return makeStatementsSequenceOrStatement(
            statements = result,
            source_ref = source_ref
        )
    else:
        assert False, (kind, detail, source_ref)


def buildDeleteNode(provider, node, source_ref):
    # Build "del" statements.

    # Note: Each delete is sequential. It can succeed, and the failure of a
    # later one does not prevent the former to succeed. We can therefore have a
    # simple sequence of "del" statements that each only delete one thing
    # therefore. In output tree "del" therefore only ever has single arguments.

    statements = []

    for target in node.targets:
        # We don't allow None, cannot happen, and so we know it must
        # be a tuple, pylint: disable=W0633
        kind, detail = decodeAssignTarget(
            provider   = provider,
            node       = target,
            source_ref = source_ref
        )

        statements.append(
            buildDeleteStatementFromDecoded(
                kind       = kind,
                detail     = detail,
                source_ref = source_ref
            )
        )

    return makeStatementsSequenceOrStatement(
        statements = statements,
        source_ref = source_ref
    )


def _buildInplaceAssignVariableNode(variable_ref, operator, expression,
                                    source_ref):
    assert variable_ref.isExpressionTargetVariableRef(), variable_ref

    inplace_node = ExpressionOperationBinaryInplace(
        operator   = operator,
        left       = ExpressionVariableRef(
            variable_name = variable_ref.getVariableName(),
            source_ref    = source_ref
        ),
        right      = expression,
        source_ref = source_ref
    )

    inplace_node.markAsInplaceSuspect()

    result = (
        StatementAssignmentVariable(
            variable_ref = ExpressionTargetVariableRef(
                variable_name = variable_ref.getVariableName(),
                source_ref    = source_ref
            ),
            source       = inplace_node,
            source_ref   = source_ref
        ),
    )

    return result


def _buildInplaceAssignAttributeNode(lookup_source, attribute_name,
                                     tmp_variable1, tmp_variable2, operator,
                                     expression, source_ref):
    # First assign the target value to a temporary variable.
    preserve_to_tmp = StatementAssignmentVariable(
        variable_ref = ExpressionTargetTempVariableRef(
            variable   = tmp_variable1,
            source_ref = source_ref
        ),
        source       = ExpressionAttributeLookup(
            source         = lookup_source.makeCloneAt(source_ref),
            attribute_name = attribute_name,
            source_ref     = source_ref
        ),
        source_ref   = source_ref
    )

    # Second assign the in-place result to a temporary variable
    inplace_to_tmp = StatementAssignmentVariable(
        variable_ref = ExpressionTargetTempVariableRef(
            variable   = tmp_variable2,
            source_ref = source_ref
        ),
        source       = ExpressionOperationBinaryInplace(
            operator   = operator,
            left       = ExpressionTempVariableRef(
                variable   = tmp_variable1,
                source_ref = source_ref
            ),
            right      = expression,
            source_ref = source_ref
        ),
        source_ref   = source_ref
    )

    # Third, copy it over, if the reference values change, i.e. IsNot is true.
    copy_back_from_tmp = StatementConditional(
        condition  = ExpressionComparisonIsNOT(
            left       = ExpressionTempVariableRef(
                variable   = tmp_variable1,
                source_ref = source_ref
            ),
            right      = ExpressionTempVariableRef(
                variable   = tmp_variable2,
                source_ref = source_ref
            ),
            source_ref = source_ref
        ),
        yes_branch = makeStatementsSequenceFromStatement(
            statement = StatementAssignmentAttribute(
                expression     = lookup_source.makeCloneAt(source_ref),
                attribute_name = attribute_name,
                source         = ExpressionTempVariableRef(
                    variable   = tmp_variable2,
                    source_ref = source_ref
                ),
                source_ref     = source_ref
            )
        ),
        no_branch  = None,
        source_ref = source_ref
    )

    copy_back_from_tmp = makeTryFinallyStatement(
        tried      = copy_back_from_tmp,
        final      = StatementReleaseVariable(
            variable   = tmp_variable2,
            tolerant   = False,
            source_ref = source_ref
        ),
        source_ref = source_ref
    )

    return (
        preserve_to_tmp,
        # making sure the above temporary variable is deleted in any case.
        makeTryFinallyStatement(
            tried      = (
                inplace_to_tmp,
                copy_back_from_tmp,
            ),
            final      = StatementReleaseVariable(
                variable   = tmp_variable1,
                tolerant   = False,
                source_ref = source_ref
            ),
            source_ref = source_ref
        )
    )


def _buildInplaceAssignSubscriptNode(subscribed, subscript, tmp_variable1,
                                     tmp_variable2, operator, expression,
                                     source_ref):
    # First assign the subscribed value to a temporary variable.
    preserve_to_tmp1 = StatementAssignmentVariable(
        variable_ref = ExpressionTargetTempVariableRef(
            variable   = tmp_variable1,
            source_ref = source_ref
        ),
        source       = subscribed,
        source_ref   = source_ref
    )
    # Second assign the subscript value to a temporary variable
    preserve_to_tmp2  = StatementAssignmentVariable(
        variable_ref = ExpressionTargetTempVariableRef(
            variable   = tmp_variable2,
            source_ref = source_ref
        ),
        source       = subscript,
        source_ref   = source_ref
    )

    execute_in_place = StatementAssignmentSubscript(
        expression = ExpressionTempVariableRef(
            variable   = tmp_variable1,
            source_ref = source_ref
        ),
        subscript  = ExpressionTempVariableRef(
            variable   = tmp_variable2,
            source_ref = source_ref
        ),
        source     = ExpressionOperationBinaryInplace(
            operator   = operator,
            left       = ExpressionSubscriptLookup(
                subscribed = ExpressionTempVariableRef(
                    variable   = tmp_variable1,
                    source_ref = source_ref
                ),
                subscript  = ExpressionTempVariableRef(
                    variable   = tmp_variable2,
                    source_ref = source_ref
                ),
                source_ref = source_ref
            ),
            right      = expression,
            source_ref = source_ref
        ),
        source_ref = source_ref
    )

    # Note: No copy back is happening, for subscripts that is implied.

    return (
        preserve_to_tmp1,
        makeTryFinallyStatement(
            tried      = (
                preserve_to_tmp2,
                execute_in_place,
            ),
            final      = (
                StatementReleaseVariable(
                    variable   = tmp_variable1,
                    tolerant   = False,
                    source_ref = source_ref
                ),
                StatementReleaseVariable(
                    variable   = tmp_variable2,
                    tolerant   = True,
                    source_ref = source_ref
                )
            ),
            source_ref = source_ref
        )
    )


def _buildInplaceAssignSliceNode(lookup_source, lower, upper, tmp_variable1,
                                 tmp_variable2, tmp_variable3, operator,
                                 expression, source_ref):

    # Due to the 3 inputs, which we need to also put into temporary variables,
    # there are too many variables here, but they are needed.
    # pylint: disable=R0914

    # First assign the target value, lower and upper to temporary variables.
    copy_to_tmp = StatementAssignmentVariable(
        variable_ref = ExpressionTargetTempVariableRef(
            variable   = tmp_variable1,
            source_ref = source_ref
        ),
        source       = lookup_source,
        source_ref   = source_ref
    )

    final_statements = [
        StatementReleaseVariable(
            variable   = tmp_variable1,
            tolerant   = False,
            source_ref = source_ref
        )
    ]
    statements = []

    if lower is not None:
        statements.append(
            StatementAssignmentVariable(
                variable_ref = ExpressionTargetTempVariableRef(
                    variable   = tmp_variable2,
                    source_ref = source_ref
                ),
                source       = lower,
                source_ref   = source_ref
            )
        )
        final_statements.append(
            StatementReleaseVariable(
                variable   = tmp_variable2,
                tolerant   = True,
                source_ref = source_ref
            )
        )

        lower_ref1 = ExpressionTempVariableRef(
            variable   = tmp_variable2,
            source_ref = source_ref
        )
        lower_ref2 = ExpressionTempVariableRef(
            variable   = tmp_variable2,
            source_ref = source_ref
        )
    else:
        assert tmp_variable2 is None

        lower_ref1 = lower_ref2 = None

    if upper is not None:
        statements.append(
            StatementAssignmentVariable(
                variable_ref = ExpressionTargetTempVariableRef(
                    variable   = tmp_variable3,
                    source_ref = source_ref
                ),
                source       = upper,
                source_ref   = source_ref
            )
        )
        final_statements.append(
            StatementReleaseVariable(
                variable   = tmp_variable3,
                tolerant   = True,
                source_ref = source_ref
            )
        )

        upper_ref1 = ExpressionTempVariableRef(
            variable   = tmp_variable3,
            source_ref = source_ref
        )
        upper_ref2 = ExpressionTempVariableRef(
            variable   = tmp_variable3,
            source_ref = source_ref
        )
    else:
        assert tmp_variable3 is None

        upper_ref1 = upper_ref2 = None

    use_sliceobj = Utils.python_version >= 300

        # Second assign the in-place result over the original value.
    if use_sliceobj:
        statements.append(
            StatementAssignmentSubscript(
                expression = ExpressionTempVariableRef(
                    variable   = tmp_variable1,
                    source_ref = source_ref
                ),
                subscript  = ExpressionSliceObject(
                    lower      = lower_ref1,
                    upper      = upper_ref1,
                    step       = None,
                    source_ref = source_ref
                ),
                source     = ExpressionOperationBinaryInplace(
                    operator   = operator,
                    left       = ExpressionSubscriptLookup(
                        subscribed = ExpressionTempVariableRef(
                            variable   = tmp_variable1,
                            source_ref = source_ref
                        ),
                        subscript  = ExpressionSliceObject(
                            lower      = lower_ref2,
                            upper      = upper_ref2,
                            step       = None,
                            source_ref = source_ref
                        ),
                        source_ref = source_ref
                    ),
                    right      = expression,
                    source_ref = source_ref
                ),
                source_ref = source_ref
            )
        )
    else:
        statements.append(
            StatementAssignmentSlice(
                expression = ExpressionTempVariableRef(
                    variable   = tmp_variable1,
                    source_ref = source_ref
                ),
                lower      = lower_ref1,
                upper      = upper_ref1,
                source     = ExpressionOperationBinaryInplace(
                    operator   = operator,
                    left       = ExpressionSliceLookup(
                        expression = ExpressionTempVariableRef(
                            variable   = tmp_variable1,
                            source_ref = source_ref
                        ),
                        lower      = lower_ref2,
                        upper      = upper_ref2,
                        source_ref = source_ref
                    ),
                    right      = expression,
                    source_ref = source_ref
                ),
                source_ref = source_ref
            )
        )

    return (
        copy_to_tmp,
        makeTryFinallyStatement(
            tried      = statements,
            final      = final_statements,
            source_ref = source_ref
        )
    )


def buildInplaceAssignNode(provider, node, source_ref):
    # There are many inplace assignment variables, and the detail is unpacked
    # into names, so we end up with a lot of variables, which is on purpose,
    # pylint: disable=R0914

    operator = getKind(node.op)

    if operator == "Div" and source_ref.getFutureSpec().isFutureDivision():
        operator = "TrueDiv"

    expression = buildNode(provider, node.value, source_ref)

    # We don't allow None, as we handled that above, and so we know it must
    # be a tuple, pylint: disable=W0633
    kind, detail = decodeAssignTarget(
        provider   = provider,
        node       = node.target,
        source_ref = source_ref
    )

    if kind == "Name":
        variable_ref = detail

        statements = _buildInplaceAssignVariableNode(
            variable_ref = variable_ref,
            operator     = operator,
            expression   = expression,
            source_ref   = source_ref
        )
    elif kind == "Attribute":
        lookup_source, attribute_name = detail

        temp_scope = provider.allocateTempScope("inplace_assign_attr")

        tmp_variable1 = provider.allocateTempVariable(
            temp_scope = temp_scope,
            name       = "start"
        )
        tmp_variable2 = provider.allocateTempVariable(
            temp_scope = temp_scope,
            name       = "end"
        )

        statements = _buildInplaceAssignAttributeNode(
            lookup_source  = lookup_source,
            attribute_name = attribute_name,
            tmp_variable1  = tmp_variable1,
            tmp_variable2  = tmp_variable2,
            operator       = operator,
            expression     = expression,
            source_ref     = source_ref
        )
    elif kind == "Subscript":
        subscribed, subscript = detail

        temp_scope = provider.allocateTempScope("inplace_assign_subscr")

        tmp_variable1 = provider.allocateTempVariable(
            temp_scope = temp_scope,
            name       = "target"
        )
        tmp_variable2 = provider.allocateTempVariable(
            temp_scope = temp_scope,
            name       = "subscript"
        )

        statements = _buildInplaceAssignSubscriptNode(
            subscribed    = subscribed,
            subscript     = subscript,
            tmp_variable1 = tmp_variable1,
            tmp_variable2 = tmp_variable2,
            operator      = operator,
            expression    = expression,
            source_ref    = source_ref
        )
    elif kind == "Slice":
        lookup_source, lower, upper = detail

        temp_scope = provider.allocateTempScope("inplace_assign_slice")

        tmp_variable1 = provider.allocateTempVariable(
            temp_scope = temp_scope,
            name       = "target"
        )
        if lower is not None:
            tmp_variable2 = provider.allocateTempVariable(
                temp_scope = temp_scope,
                name       = "lower"
            )
        else:
            tmp_variable2 = None

        if upper is not None:
            tmp_variable3 = provider.allocateTempVariable(
                temp_scope = temp_scope,
                name       = "upper"
            )
        else:
            tmp_variable3 = None

        statements = _buildInplaceAssignSliceNode(
            lookup_source = lookup_source,
            lower         = lower,
            upper         = upper,
            tmp_variable1 = tmp_variable1,
            tmp_variable2 = tmp_variable2,
            tmp_variable3 = tmp_variable3,
            operator      = operator,
            expression    = expression,
            source_ref    = source_ref
        )
    else:
        assert False, kind

    return StatementsSequence(
        statements = statements,
        source_ref = source_ref
    )
