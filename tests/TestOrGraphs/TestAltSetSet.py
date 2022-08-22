from unittest import TestCase
from ComputabilityGraphs.or_graph_helpers import (
    TypeSet,
    AltSet,
    AltSetSet
)
from testComputers import (
    A,
    B,
    C,
    D,
    E,
    F,
    G,
    I,
    J,
    K
)


class TestAltSetSet(TestCase):

    def test_combine(self):
        ass = AltSetSet([
            AltSet([
                TypeSet([I])
            ]),
            AltSet([
                TypeSet([J])
            ]),
            AltSet([
                TypeSet([K])
            ]),
        ])

        res = ass.combine()
        ref = AltSet([
                TypeSet([I, J, K])
        ])
        self.assertEqual(res, ref)

        ass = AltSetSet([
            AltSet([
                TypeSet([A, B]),
                TypeSet([C])
            ]),
            AltSet([
                TypeSet([D])
            ])
        ])
        res = ass.combine()
        ref = AltSet([
                TypeSet([A, B, D]),
                TypeSet([C, D])
        ])
        self.assertEqual(res, ref)

        # 3 Variables with one  of them computable in 2 ways
        ass = AltSetSet([
            AltSet([
                TypeSet([A, B]),
                TypeSet([C])
            ]),
            AltSet([
                TypeSet([D])
            ]),
            AltSet([
                TypeSet([E, F])
            ])
        ])
        res = ass.combine()
        ref = AltSet([
                TypeSet([A, B, D, E, F]),
                TypeSet([C, D, E, F])
        ])
        self.assertEqual(res, ref)

        # 2 Variables with both computable in 2 ways
        ass = AltSetSet([
            AltSet([
                TypeSet([A, B]),
                TypeSet([C])
            ]),
            AltSet([
                TypeSet([D]),
                TypeSet([E, F])
            ])
        ])
        res = ass.combine()
        ref = AltSet([
                TypeSet([A, B, D]),
                TypeSet([A, B, E, F]),
                TypeSet([C, D]),
                TypeSet([C, E, F])
        ])
        self.assertEqual(res, ref)
