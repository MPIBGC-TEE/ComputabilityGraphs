from unittest import TestCase
from frozendict import frozendict
import ComputabilityGraphs.helpers as h
from testComputers import (
        A, A1, A2, A3, A0, A_minus_1, A_minus_2, B,
        B1, B2, B3, B0, B_minus_1, B_minus_2, C, D, E, F, G, H, I, X, Y)
from testComputers import computers
from testComputers import (
    a_from_x,
    b_from_y,
    a_from_y,
    b_from_x,
    a_from_z,
    b_from_z,
    c_from_b,
    d_from_b,
    d_from_g_h,
    a2_from_a1,
    a3_from_a2,
    a3_from_b0,
    b_minus_1_from_b_minus_2,
    b0_from_b_minus_1,
    a_minus_1_from_a_minus_2,
    a1_from_a0,
    a0_from_a_minus_1,
    b1_from_b0,
    b1_from_a2,
    b2_from_b1,
    b3_from_b2,
    a0_from_b0
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
