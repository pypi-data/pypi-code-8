#-------------------------------------------------------------------------------
# Name:        myopenopt.py
# Purpose:     Calling openopt module using the same syntax as in Gurobi
#
# Author:      Mikio Kubo
#
# Created:     1/5/2015
# Copyright:   (c)  Mikio Kubo 2015
#-------------------------------------------------------------------------------
from __future__ import print_function
from FuncDesigner import *
from openopt import LP, MILP, NLP #, SOCP, QP

class GRB():
    pass
GRB.CONTINUOUS = "C"
GRB.INTEGER = "I"
GRB.BINARY = "B"
GRB.OPTIMAL = 1
GRB.INFEASIBLE = 3
GRB.UNBOUNDED = 5
GRB.UNDEFINED = None
GRB.MINIMIZE = 1
GRB.MAXIMIZE = -1
GRB.INFINITY = 1e+100

quicksum = sum

class Model():
    def __init__(self,name="", mtype="NLP"):
        self.name = name
        self.mtype = mtype
        self.constraints = [] #list of constraints
        self.variables = [] #list of variables
        self.objective = 0 #null objective function
        self.sense = GRB.MAXIMIZE
        self.var_id = 0
        self.init = {} #initial solution : key=var, value=initial solution value
                    
    def __str__(self):
        ret = "Problem Name={0} \n".format(self.name)
        if self.sense == GRB.MAXIMIZE:
            ret += "maximize  "
        else:
            ret += "minimize  "
        ret += self.objective.expr + "\n"
        for c in self.constraints:
            ret += c.expr + "\n"
        return ret
    
    def addVar(self, lb=0, ub=GRB.INFINITY, vtype="C", name="", init=0.0):
        if name == "":
            self.var_id += 1
            name = "x_{0}".format(self.var_id)
        if vtype == "C" or vtype == GRB.CONTINUOUS:
            CAT = None
        elif vtype == "I" or vtype == GRB.INTEGER:
            CAT = int
        elif vtype == "B" or vtype == GRB.BINARY:
            CAT = bool
        var = oovar(name=name, lb=lb, ub=ub, domain=CAT)
        self.variables.append(var)
        self.init[var] = init
        return var

    def update(self):
        pass

    def relax(self):
        for v in self.variables:
            v.domain = None
        return self

    def addConstr(self,Constraint=None, name=""):
        self.constraints.append(Constraint) # add a constraint
        return Constraint

    def setObjective(self, obj, sense=GRB.MAXIMIZE, name=""):
        self.objective = obj
        self.sense = sense

    def optimize(self, solver="ralg", plot=0,
                 maxIter=1e5, maxCPUTime=3600, maxFunEvals=1e12):
        if self.mtype == "LP" or self.mtype == "MILP":
            p = MILP(self.objective, self.init, constraints=self.constraints,
                     maxIter=maxIter, maxCPUTime=maxCPUTime, maxFunEvals=maxFunEvals)
        elif self.mtype == "NLP":
            p = NLP(self.objective, self.init, constraints=self.constraints,
                 maxIter=maxIter, maxCPUTime=maxCPUTime, maxFunEvals=maxFunEvals)
        else:
            print("Model Type Error")
            raise TypeError
        
        if self.sense == GRB.MAXIMIZE:
            self.Results = p.maximize(solver, plot=plot)
        else:
            self.Results = p.minimize(solver, plot=plot)
        #print(self.Results)
        self.ObjVal = self.Results.ff
 
        if self.Results.isFeasible:
            self.Status = GRB.OPTIMAL
        else:
            self.Status = GRB.INFEASIBLE

        for v in self.variables:
            v.VarName = v.name
            v.X = self.Results.xf[v]
        return self.Status
            
    def getVars(self):
        return self.variables

    def getConstrs(self):
        for c in self.constraints:
            self.constraints[c].Pi = self.constraints[c].pi
            self.constraints[c].Constrname = self.constraints[c].name
        ret = [self.constraints[c] for c in self.constraints]
        return ret

if __name__ == '__main__':
    #model_type = 'MILP'
    model_type = 'NLP'

    model = Model("sample", mtype=model_type)
    
    x1 = model.addVar(vtype="C", name="x1")
    if model_type =='MIP':
        x2 = model.addVar(vtype="I", name="x2")
    else:
        x2 = model.addVar(vtype="C", name="x2")
    x3 = model.addVar(vtype="C", ub=30, name="x3")
    model.update()

    c0 = model.addConstr(2*x1 + x2 + x3 <= 60, name="C0")
    if model_type == 'NLP':
        c1 = model.addConstr(x1**2 + 2*x2**2 <= x3**2, name="C1")
    else:
        c1 = model.addConstr(x1 + 2*x2 + x3 <= 60, name="C1")
    c2 = model.addConstr(x3 <= 30, name="C2")
    c3 = model.addConstr( quicksum([x1, x2, x3]) <= 20, name="C3" )    

    model.setObjective(15*x1 + 18*x2 + 30*x3, GRB.MAXIMIZE)
    
    print(model)
    if model_type == 'NLP':
        #r = model.optimize(solver="interalg")
        r = model.optimize(solver="ralg")
    else:
        r = model.optimize(solver="lpSolve")
    print("Result =", model.Status)
    for v in model.getVars():
        print(v.VarName, v.X)