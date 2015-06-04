from dispel4py.examples.graph_testing.testing_PEs \
    import TestProducer, TestOneInOneOut

from dispel4py.base import CompositePE, IterativePE


class MultiplyPE(IterativePE):

    def __init__(self, parameter):
        IterativePE.__init__(self)
        self.parameter = parameter

    def _process(self, data):
        return self.parameter * data


def create_test_graph(graph):
    prod = TestProducer()
    cons = TestOneInOneOut()
    graph.connect(prod, 'output', cons, 'input')
    graph._map_output('output', cons, 'output')


class MyCompositeTestPE(CompositePE):
    def __init__(self):
        CompositePE.__init__(self)
        create_test_graph(self)


def create_graph_param(graph, param):
    cons1 = TestOneInOneOut()
    cons2 = MultiplyPE(param)
    graph.connect(cons1, 'output', cons2, 'input')
    graph._map_input('input', cons1, 'input')
    graph._map_output('output', cons2, 'output')


class MyParameterisedCompositePE(CompositePE):
    def __init__(self, param):
        CompositePE.__init__(self)
        create_graph_param(self, param)


from dispel4py.workflow_graph import WorkflowGraph

graph = WorkflowGraph()
composite = MyCompositeTestPE()
comp2 = MyParameterisedCompositePE(5)
cons1 = TestOneInOneOut()
graph.connect(composite, 'output', comp2, 'input')
graph.connect(comp2, 'output', cons1, 'input')
