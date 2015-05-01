'''
CommonSubExpressions gather expressions that are alike
'''

from pythran.analyses.cfg import CFG
from pythran.analyses.identifiers import Identifiers
from pythran.analyses.ast_matcher import ASTMatcher
from pythran.analyses.pure_expressions import PureExpressions
from pythran.passmanager import FunctionAnalysis

import ast


class CommonSubExpressions(FunctionAnalysis):
    """
    Gather basic-bloc level common subexpressions.

    This analyse creates a pattern -> set of node mapping, where the key is a
    pattern for an expression that computes a simple expression, and the values
    are sets of nodes that recompute this expression """

    def __init__(self):
        self.result = dict()
        super(CommonSubExpressions, self).__init__(CFG, PureExpressions)

    def visit_FunctionDef(self, node):
        self.patterns = {}

        visited = set()
        head = self.cfg.successors(node)
        # walk each block until we find a node
        # that has more than one in_degree,
        # which means the end of a basic block
        while head:
            nexts = set()
            for curr in head:
                while True:
                    visited.add(curr)
                    succs = self.cfg.successors(curr)
                    preds = self.cfg.predecessors(curr)
                    if len(succs) == len(preds) == 1:
                        self.generic_visit(curr)
                        curr = succs[0]
                    else:
                        nexts.update(succs)
                        break
            self.patterns.clear()
            nexts.difference_update(visited)
            head = nexts

        for k, v in self.result.items():
            if len(v) < 2:
                del self.result[k]

    def visit_any(self, node):
        self.generic_visit(node)
        if node not in self.pure_expressions:
            return
        for pattern in self.patterns.values():
            if {node} == pattern.search(node):
                self.result[pattern.pattern].add(node)
                return

        new_pattern = ASTMatcher(node)
        deps = self.passmanager.gather(Identifiers, node)
        self.patterns[tuple(deps)] = new_pattern
        self.result.setdefault(node, set()).add(node)

    visit_UnaryOp = visit_BinOp = visit_Call = visit_any

    def kill(self, target):
        for k in self.patterns.keys():
            if target.id in k:
                del self.patterns[k]

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            self.kill(node)

    def visit_Subscript(self, node):
        if isinstance(node.ctx, ast.Store):
            def rec(n):
                if isinstance(n, ast.Name):
                    return n
                elif isinstance(n, ast.Subscript):
                    return rec(n.value)
            nid = rec(node)
            if nid:
                self.kill(nid)
        else:
            self.visit_any(node)
