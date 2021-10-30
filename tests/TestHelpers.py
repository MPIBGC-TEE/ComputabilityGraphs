from unittest import TestCase
from frozendict import frozendict
import ComputabilityGraphs.helpers as h
from testComputers import  A2, B0
from testComputers import (
    a3_from_a2,
    a3_from_b0,
)


class TestHelpers(TestCase):
    def test_combi_arg_set(self):
        self.assertEqual(
            h.combi_arg_set(
                frozenset([
                    a3_from_a2,
                    a3_from_b0
                ])
            ),
            frozenset([A2, B0])
        )


    def test_merge_dicts(self):
        d1 = frozendict({"a": 1})
        d2 = frozendict({"b": 2})
        d = h.merge_dicts(d1, d2)
        self.assertEqual(d, frozendict({"a": 1, "b": 2}))

    def test_list_mult(self):
        l1 = ["A", "B"]
        l2 = ["c", "d"]
        self.assertEqual(
            h.list_mult([l1, l2]),
            [
                ("A", "c"),
                ("B", "c"),
                ("A", "d"),
                ("B", "d")
            ]
        )
        l1 = ["A", "B"]
        l2 = ["c", "d"]
        l3 = [1, 2]
        self.assertEqual(
            h.list_mult([l1, l2, l3]),
            [
                ("A", "c", 1),
                ("B", "c", 1),
                ("A", "d", 1),
                ("B", "d", 1),
                ("A", "c", 2),
                ("B", "c", 2),
                ("A", "d", 2),
                ("B", "d", 2)
            ]
        )

    def test_tuple_list_mult(self):
        l1 = [("A", ), ("B", )]
        l2 = [("c", ), ("d", )]
        self.assertEqual(
            h.tuple_list_mult([l1, l2]),
            [
                ("A", "c"),
                ("B", "c"),
                ("A", "d"),
                ("B", "d")
            ]
        )
        l1 = [("A", ), ("B", )]
        l2 = [("c", ), ("d", )]
        l3 = [(1, ), (2, )]
        self.assertEqual(
            h.tuple_list_mult([l1, l2, l3]),
            [
                ("A", "c", 1),
                ("B", "c", 1),
                ("A", "d", 1),
                ("B", "d", 1),
                ("A", "c", 2),
                ("B", "c", 2),
                ("A", "d", 2),
                ("B", "d", 2)
            ]
        )

    def test_remove_supersets(self):
        self.assertEqual(
            h.remove_supersets(
                frozenset([
                    frozenset({1}),
                    frozenset({2}),
                    frozenset({1, 3}), 
                    frozenset({2, 4}),
                    frozenset({3, 4}),
                    frozenset({1, 3, 4})
                ])
            ),
            frozenset([
                frozenset({1}),
                frozenset({2}),
                frozenset({3, 4})
            ])
        )

    def test_power_list(self):
        s1 = [1,2]
        power_list1 = [[2],[1],[1,2]]
        self.assertEqual(power_list1, h.power_list(s1))
        
        s2=[1,2,3]
        psl2 = [[3],[2],[2,3]] + [[3],[1],[1,3]] + [[2],[1],[1,2]] + [s2] 
        self.assertEqual(psl2, h.power_list(s2))
    
    def test_power_set(self):
        s1 = frozenset([1,2])
        power_set_1 = frozenset(
            [
                frozenset([]),
                frozenset([2]),
                frozenset([1]),
                frozenset([1,2])
            ]
        )
        self.assertEqual(power_set_1, h.power_set(s1))
        
        s2=frozenset([1,2,3])
        psl2 = frozenset(
            [
                frozenset(l) 
                for l in [[],[3],[2],[2,3],[3],[1],[1,3],[2],[1],[1,2],s2] 
            ]
        )
        self.assertEqual(psl2, h.power_set(s2))
