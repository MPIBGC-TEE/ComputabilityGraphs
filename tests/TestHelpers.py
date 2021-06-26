from unittest import TestCase
from ComputabilityGraphs.helpers import merge_dicts
from frozendict import frozendict


class TestHelpers(TestCase):
    def test_merge_dicts(self):
        d1 = frozendict({"a": 1})
        d2 = frozendict({"b": 2})
        d = merge_dicts(d1, d2)
        self.assertEqual(d,frozendict({"a": 1,"b": 2}))
