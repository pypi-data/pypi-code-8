import unittest
from collatex import collate, Collation
from tests import unit_disabled

__author__ = 'ronalddekker'

class TestTranspositionDetection(unittest.TestCase):

    def testThisMorningExample(self):
        def find_out_going_vertex_for_a_witness(graph, vertex, expected_sigil):
            #TODO: this can be done using generators!
            edges = graph.out_edges(vertex, data=True)
            found_vertex = None
            for (_, target, attrs) in edges:
                # there can be multiple sigli on one edge
                sigli = attrs["label"].split(", ")
                if expected_sigil in sigli:
                    found_vertex = target
                    break
            return found_vertex

        collation = Collation()
        collation.add_plain_witness("A", "This morning the cat observed little birds in the trees.")
        collation.add_plain_witness("B", "The cat was observing birds in the little trees this morning, it observed birds for two hours.")
        alignment_table = collate(collation, detect_transpositions=True)
        # we have to walk over the variant graph following a path for a witness
        variant_graph = collate(collation, detect_transpositions=True, output="graph")
        print(variant_graph)
        # variant graph has out edges
        # not so nice, but witnesses are stored on a label
        out_edges = variant_graph.out_edges(variant_graph.start, data=True)
        print(out_edges)
        sigil_to_find = "A"
        next_vertex = find_out_going_vertex_for_a_witness(variant_graph, variant_graph.start, sigil_to_find)
        print(next_vertex)

