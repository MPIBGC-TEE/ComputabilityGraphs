#!/usr/bin/env python3
import matplotlib.pyplot as plt
from ComputabilityGraphs.helpers import (
    computable_mvars,
    directly_computable_mvars,
    input_mvars,
    arg_set,
    arg_set_set,
    output_mvar,
    all_mvars,
    applicable_computers,
    all_computers_for_mvar,
)

from unittest import TestCase, skip

from testComputers import (
    A, B, C, D, E, F, G, H, I,
    b_from_a,
    c_from_b,
    f_from_b,
    d_from_a_c,
    d_from_b_c,
    f_from_e,
)


class TestResolveWithoutGraphs(TestCase):
    def setUp(self):
        # we produce a small set of Mvars with a loop (b could be something
        # like a CompartmentalSystem that can be computed  in different ways
        # and can also be queried about its constituents.
        #
        self.mvars = {
            A,
            B,
            C,
            D,
            E,
            F,
            G,
            H,
            I,
        }
        self.computers = frozenset(
            {f_from_b, d_from_a_c, d_from_b_c, c_from_b, b_from_a, f_from_e}
        )

    def test_signature(self):
        self.assertEqual(input_mvars(f_from_b), frozenset({B}))
        self.assertEqual(input_mvars(d_from_a_c), frozenset({A, C}))

    def test_all_computers_for_mvar(self):
        self.assertEqual(
            all_computers_for_mvar(D, self.computers),
            frozenset({d_from_a_c, d_from_b_c}),
        )

    def test_all_mvars(self):
        self.assertEqual(all_mvars(self.computers), frozenset({A, B, C, D, E, F}))

    def test_arg_set(self):
        self.assertEqual(arg_set(d_from_a_c), frozenset({A, C}))

    def test_arg_set_set(self):
        self.assertEqual(
            arg_set_set(D, self.computers),
            frozenset({frozenset({A, C}), frozenset({B, C})}),
        )

    def test_applicable_computers(self):
        self.assertEqual(
            applicable_computers(self.computers, frozenset({B, C})),
            frozenset({f_from_b, d_from_b_c, c_from_b}),
        )

    def test_direct_computability(self):
        self.assertEqual(
            directly_computable_mvars(self.computers, frozenset({B, C})),
            frozenset({F, D, C}),
        )

    def test_computability(self):
        res = computable_mvars(
            allComputers=self.computers, available_mvars=frozenset([A, C])
        )
        # pe('mvars',locals())
        # e and f are not computable
        self.assertEqual(res, frozenset({A, B, C, D, F}))
