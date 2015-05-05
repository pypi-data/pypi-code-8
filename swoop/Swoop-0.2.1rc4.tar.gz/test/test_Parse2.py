from __future__ import unicode_literals
import unittest
import pypeg2
import re
from pyparsing import *


class TestPyPEG(unittest.TestCase):
    
    def setUp(self):
        pass

    @unittest.skipIf(True, "Disabled in production")
    def test_Parse(self):
        SIPrefixes = {"G" : 1e9,
                      "M" : 1e6,
                      "K" : 1e3,
                      "k" : 1e3,
                      "m" : 1e-3,
                      "u" : 1e-6,
                      "n" : 1e-9,
                      "p" : 1e-12,
                      "f" : 1e-15};

        def SIMagnitude(p):
            return SIPrefixes[p]


        class FloatConstant(str): 
            grammar = re.compile('([+-]?(([1-9][0-9]*)|0+)(\.[0-9]*)?)')
            def __init__(self,t):
                #print "Float t = " + repr(t)
                self.v = float(t)

            def __str__(self):
                return str(self.v)
            
            def eval(self, env):
                return self.v

        SIBaseUnit = re.compile("F|W|V|A|Ohm|m|g")
        class SIPrefix(FloatConstant):
            grammar = re.compile("|".join(SIPrefixes.keys()))
            def __init__(self,t):
                #print "SIPrefix t = " + repr(t)
                FloatConstant.__init__(self, SIPrefixes[t])

        class SIUnit(FloatConstant):
            grammar = pypeg2.optional(SIPrefix), SIBaseUnit
            def __init__(self,t):
                #print "SIUnit t = " + repr(t)
                if len(t) == 1:
                    FloatConstant.__init__(self,1.0)
                else:
                    FloatConstant.__init__(self,t[0].v)

        class SIConstant(FloatConstant):
            grammar = FloatConstant, SIUnit
            def __init__(self, t):
                #print "SIConstant t = " + repr(t)
                FloatConstant.__init__(self,t[0].v * t[1].v)
            
        #SI_CONSTANT = (FLOAT("num") + SI_UNIT("mult")).setParseAction(SIConstant)

        class PercentConstant(FloatConstant):
            grammar = FloatConstant, "%"
            def __init__(self,t):
                FloatConstant.__init__(self, t.v*0.01)

        class Constant(FloatConstant):
            grammar = [SIConstant,  PercentConstant,FloatConstant]
            def __init__(self,t):
                #print "Constant t = " + repr(t)
                FloatConstant.__init__(self, t.v)

        class Identifier(object):
            grammar = re.compile("\w[\w\d_]*")
            def __init__(self,t):
                #print "Identifier t = " + repr(t)
                self.v = t
            def eval(self, env):
                return env[self.v]
                
        class Term(object):
            grammar = [Constant, Identifier]
            def __init__(self,t):
                #print "Term t = " + repr(t)
                self.v = t
            def __str__(self):
                return str(self.v)
            def eval(self, env):
                return self.v.eval(env)
            
        PredicateOperator = re.compile(">=|<=|==|!=|<|>")

        class PredicateExpr(object):
            grammar = Term, PredicateOperator, Term
            #grammar = Constant, PredicateOperator, Constant
            
            def __init__(self, t):
                #print "PredicateExpr t = " + repr(t)
                self.lhs = t[0]
                self.op = t[1]
                self.rhs= t[2]

            def __str__(self):
                return " ".join(map(str,[self.lhs, self.op, self.rhs]))
            
            def eval(self, env):
                if self.op == "<" or self.op == "<=":
                    return self.lhs.eval(env) <= self.rhs.eval(env)
                elif self.op == ">" or self.op == ">=":
                    return self.lhs.eval(env) >= self.rhs.eval(env)
                elif self.op == "==":
                    return self.lhs.eval(env) == self.rhs.eval(env)
                elif self.op == "!=":
                    return self.lhs.eval(env) != self.rhs.eval(env)
                else:
                    assert False

        OrderingOperator = re.compile(">=|<=|<|>")
        class TrinaryPredicateExpr(object):
            grammar = Term, OrderingOperator, Term, OrderingOperator, Term
            
            def __init__(self, t):
                self.lhs = t[0]
                self.lop = t[1]
                self.chs = t[2]
                self.rop = t[3]
                self.rhs = t[4]

            def __str__(self):
                return " ".join(map(str,[self.lhs, self.lop, self.chs, self.rop, self.rhs]))
            
            def eval(self, env):

                if self.lop == "<" or self.lop == "<=":
                    assert self.rop == "<" or self.rop == "<="

                if self.lop == ">" or self.lop == ">=":
                    assert self.rop == ">" or self.rop == ">="

                if self.lop == "<" or self.lop == "<=":
                    lp = self.lhs.eval(env) <= self.chs.eval(env)
                elif self.lop == ">" or self.lop == ">=":
                    lp = self.lhs.eval(env) <= self.chs.eval(env)
                else:
                    assert False
                
                if self.rop == "<" or self.rop == "<=":
                    rp = self.chs.eval(env) <= self.rhs.eval(env)
                elif self.rop == ">" or self.rop == ">=":
                    rp = self.chs.eval(env) >= self.rhs.eval(env)
                else:
                    assert False

                return (lp and rp)

        class BoundExpr(object):
            grammar = PredicateOperator, Term
            def __init__(self, t):
                self.op = t[0]
                self.bound = t[1]
            def contains(self, v, env):
                if self.op == "<" or self.op == "<=":
                    return v.eval(env) < self.bound.eval(env)
                elif self.op == ">" or self.op == ">=":
                    return v.eval(env) > self.bound.eval(env)
                elif self.op == "==":
                    return v.eval(env) == self.bound.eval(env)
                elif self.op == "!=":
                    return v.eval(env) != self.bound.eval(env)
                else:
                    assert False

        class OptionsExpr(object):
            grammar = "{", pypeg2.csl(Term), "}"
            def __init__(self, t):
                self.values = t
            def contains(self, v, env):
                for x in self.values:
                    if x.eval(env) == v.eval(env):
                        return True
                return False
            #ComplexSetExpr.grammar += [pypeg2.csl(SetExpr)]            

        class SetIntersectionPrimeExpr(object):
            def __init__(self, t):
                self.v = t
            def contains(self, v, env):
                for s in self.v:
                    if not s.contains(v,env):
                        return False
                return True
            
        class SetIntersectionExpr(object):
            def __init__(self, t):
                self.v = t
            def contains(self, v, env):
                for s in self.v:
                    if not s.contains(v,env):
                        return False
                return True

        class SetUnionExpr(object):
            #grammar = SetExpr, maybe_some("|", SetExpr)
            def __init__(self, t):
                self.v = t
            def contains(self, v, env):
                for s in self.v:
                    if s.contains(v,env):
                        return True
                return False

        class ComplexSetExpr(object):
            #grammar = "(", SetIntersectionExpr, ")"
            def __init__(self, t):
                self.v = t
            def contains(self, v, env):
                return self.v.contains(v,env)

        class SetExpr(object):
            #grammar = [ComplexSetExpr, BoundExpr, OptionsExpr]
            def __init__(self, t):
                self.v = t
            def contains(self, v, env):
                return self.v.contains(v,env)

        SetExpr.grammar = [SetIntersectionExpr,
                           #SetUnionExpr,
                           BoundExpr,
                           OptionsExpr]
        
        SetIntersectionExpr.grammar      =  SetExpr, "&", SetExpr, SetIntersectionPrimeExpr
        SetIntersectionPrimeExpr.grammar =  ["",("&", SetIntersectionPrimeExpr)]
        
        #SetUnionExpr.grammar =        SetExpr, "|", SetExpr
#        SetUnionExpr.grammar =        "(",SetExpr, pypeg2.maybe_some("|", SetExpr), ")"



        class IsInExpr(object):
            grammar = Term, "in", SetExpr
            def __init__(self, t):
                self.lhs = t[0]
                self.set = t[1]
            def eval(self, env):
                return self.set.contains(self.lhs, env)
            
        class Expr(object):
            grammar = [TrinaryPredicateExpr, PredicateExpr, IsInExpr, Term]
            def __init__(self, t):
                self.v = t
            def eval(self, env):
                return self.v.eval(env)

        def doTest(test, grammar, desc):
            print "=================================="
            print "Test: '" + str(test[0]) + "' | " + str(test[1]) + " = " + str(test[2])
            self.assertEqual(pypeg2.parse(test[0], grammar).eval(test[1]), test[2], desc + ": " + str(test))
            
        floatTests =[("1.0",{},1.0),
                     ("1",{},1),
                     ("-2",{},-2),
                     ("-0.0",{},0),
                     ("+4.2",{},4.2),
                     ("1",{},1),
                     ("-100",{},-100),
                     ( "1234.123445",{},1234.123445)];
        for t in floatTests:

            doTest(t, FloatConstant, "Float Constant")
    
        siTests=[("F", {}, 1),
                 ("uF", {}, 1e-6),
                 ("mA", {}, 1e-3),
                 ("pV", {}, 1e-12),
                 ("kW", {}, 1e3),
                 ("MA", {}, 1e6)]
        for t in siTests:
            doTest(t, SIUnit, "SI unit")

        
        percentTests = [("10%", {}, 0.1),
                        ("10 %", {}, 0.1)]
        for t in percentTests:
            doTest(t, PercentConstant, "Percent Constant")

        siConstantTests =[("1.0F", {},1.0),
                          ("1 A", {},1),
                          ("-2V", {},-2),
                          ("-0.0W", {},0),
                          ("+4.2A", {},4.2),
                          ("1F", {},1),
                          ("-100W", {},-100),
                          (" 1234.123445 V", {},1234.123445)]
        for t in siConstantTests:
            doTest(t, SIConstant, "SI Constant")

        constantTests = [("1.0F", {},1.0),
                         ("1 A", {},1),
                         ("-2V", {},-2),
                         ("-0.0W", {},0),
                         ("+4.2A", {},4.2),
                         ("1F", {},1),
                         ("-100W", {},-100),
                         (" 1234.123445 V", {},1234.123445),
                         ("1.0uF", {},1.0*1e-6),
                         ("1 mA",{}, 1*1e-3),
                         ("-2MV", {},-2*1e6),
                         ("-0.0nW", {},0),
                         ("+4.2A", {},4.2),
                         ("1pF", {},1*1e-12),
                         ("-100kW",{}, -100*1e3),
                         ("-100fW", {},-100*1e-15),
                         ("10%",{}, 10*.01)]
        for t in constantTests:
            doTest(t, Constant, "Constant")

        predicateExprTests = [("1pF < 1uF", {}, True),
                              ("x < 10", {"x":5}, True),
                              ("x>y", {"x":1,"y":2}, False),
                              ("x!= 10", {"x":4}, True),
                              ("x < 10pF", {"x":0}, True)
                              ]

        for t in predicateExprTests:
            doTest(t, PredicateExpr, "Predicate expr")

        trinaryPredicateTests = [("0 < x < 10", {"x":5}, True),
                                 ("0 > x > 10", {"x":5}, False),
                                 ("0 >= x > 10", {"x":5}, False),
                                 ("1uF < x < 10MF", {"x": 10*1e-6}, True)]

        for t in trinaryPredicateTests:
            doTest(t, TrinaryPredicateExpr, "Trinary Predicate Expr")


        isInTests = [("4 in <10", {}, True),
                     ("x in <=10", {"x":5}, True),
                     ("4 in >10", {}, False),
                     ("4 in <x", {"x":10}, True),
                     ("4 in >=x", {"x":10}, False),
                     ("4 in ==x", {"x":10}, False),
                     ("4 in ==x", {"x":4}, True),
                     ("4 in !=x", {"x":4}, False),
                     ("x in <y", {"x":10, "y": 4}, False),
                     ("x in {1,2}", {"x":1},True),
                     ("x in {1,2}", {"x":2},True),
                     ("x in {1,2}", {"x":3},False),
                     ("x in {a,b}", {"x":3, "a":1, "b":2},False),
                     ("3 in {a,b}", {"a":1, "b":2},False),
                     ("3 in {a}", {"a":3},True),
                     ("3 in (<10 & >20)", {},False),
                     ("13 in (>10 & <20)", {},True),
                     ("13 in (>10 | <20)", {},True),
                     ("35 in (<10 | <20 | (>30 & <40))", {},True),
                     ("41 in (<10 | <20 | (>30 & <40))", {},False),
                     ("x in (<10 | <20 | (>30 & <y))", {'x':41, 'y':40},False),
                     ("x in ((>10 & <20) | {35, 40})", {'x':40},True),
                     ("x in ((>10 & <20) | {35, 40})", {'x':35},True),
                     ("x in ((>10 & <20) | {35, 40})", {'x':15},True),
                     ("x in ((>10 & <20) | {35, 40})", {'x':36},False),
                     ("4 in <10", {}, True)]

        for t in isInTests:
            doTest(t, IsInExpr, "IsIn Predicate Expr")
        
        for t in floatTests + predicateExprTests + trinaryPredicateTests + constantTests + isInTests:
            doTest(t, Expr, "Expression")
            
