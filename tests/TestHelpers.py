from unittest import TestCase
from frozendict import frozendict
import ComputabilityGraphs.helpers as h
class TestHelpers(TestCase):

    def test_merge_dicts(self):
        d1 = frozendict({"a": 1})
        d2 = frozendict({"b": 2})
        d = h.merge_dicts(d1, d2)
        self.assertEqual(d,frozendict({"a": 1,"b": 2}))

    def test_list_mult(self):
        l1=["A","B"]
        l2=["c","d"]
        self.assertEqual(
            h.list_mult([l1,l2]),
            [
                ("A","c"),
                ("B","c"),
                ("A","d"),
                ("B","d")
            ]
        )
        l1=["A","B"]
        l2=["c","d"]
        l3=[1,2]
        self.assertEqual(
            h.list_mult([l1,l2,l3]),
            [
                ("A","c",1),
                ("B","c",1),
                ("A","d",1),
                ("B","d",1),
                ("A","c",2),
                ("B","c",2),
                ("A","d",2),
                ("B","d",2)
            ]
        )


    def test_tuple_list_mult(self):
        l1=[("A",),("B",)]
        l2=[("c",),("d",)]
        self.assertEqual(
            h.tuple_list_mult([l1,l2]),
            [
                ("A","c"),
                ("B","c"),
                ("A","d"),
                ("B","d")
            ]
        )
        l1=[("A",),("B",)]
        l2=[("c",),("d",)]
        l3=[(1,),(2,)]
        self.assertEqual(
            h.tuple_list_mult([l1,l2,l3]),
            [
                ("A","c",1),
                ("B","c",1),
                ("A","d",1),
                ("B","d",1),
                ("A","c",2),
                ("B","c",2),
                ("A","d",2),
                ("B","d",2)
            ]
        )
