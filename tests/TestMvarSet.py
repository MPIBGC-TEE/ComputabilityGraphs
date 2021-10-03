import unittest
from sympy import symbols
from ComputabilityGraphs.MVarSet import MVarSet

from testComputers import (
    A, A1, A2, A3, A0, A_minus_1, A_minus_2, B,
    B1, B2, B3, B0, B_minus_1, B_minus_2, C, D, E, F, G, H, I,J, X, Y,
    a_from_x,
    b_from_y,
    a_from_i,
    b_from_c_d,
    b_from_e_f,
    a_from_y,
    b_from_x,
    a_from_z,
    b_from_z,
    c_from_b,
    d_from_b,
    d_from_g_h,
    a2_from_a1,
    a3_from_a2,
    b_minus_1_from_b_minus_2,
    b0_from_b_minus_1,
    a_minus_1_from_a_minus_2,
    a1_from_a0,
    a0_from_a_minus_1,
    b1_from_b0,
    b2_from_b1,
    b3_from_b2,
    a0_from_b0,
    a3_from_b0,
    b1_from_a2,
    e_from_b,
    f_from_b,
)
class TestMVarSet(unittest.TestCase):
    def setUp(self):
        self.provided_values=MVarSet(
            [
                A(),
                B(),
                C()
            ]
        )
        self.mvs=Node(self.provided_values)
    
    def test_provided_mvar_values(self):
        mvs = self.mvs
        pmvs = mvs.provided_mvar_values
        self.assertSetEqual(pmvs, self.provided_values)
        
    def test_provided_mvar_types(self):
        mvs = self.mvs
        pmvts = mvs.provided_mvar_types
        self.assertSetEqual(
            pmvts,
            frozenset(type(v) for v in self.provided_values)
        )
        

    # @unittest.skip
    def test_computable_mvar_types(self):
        ''' This test also depends on the content of bgc_md2.resolve.computers
            since more variables become computable if we add computers...
        '''
        mvs = self.mvs
        res = frozenset(
            [
                InFluxesBySymbol,
                OutFluxesBySymbol,
                InternalFluxesBySymbol,
                TimeSymbol,
                StateVariableTuple,
                SmoothReservoirModel,
                CompartmentalMatrix,
            ]
        )
        cmvs = mvs.computable_mvar_types()
        print("###############################################")
        print(cmvs)
        self.assertSetEqual(cmvs, res)

    
    def test_paths_to_single_mvar(self):
        mvs = self.mvs
        pd = mvs.path_dict_to_single_mvar(SmoothReservoirModel)
        startNode = frozenset(
            [
                InFluxesBySymbol,
                OutFluxesBySymbol,
                InternalFluxesBySymbol,
                TimeSymbol,
                StateVariableTuple,
            ]
        )
        paths = pd[startNode]
        res = paths[0]
        ref = [startNode, frozenset({SmoothReservoirModel})]
        self.assertEqual(res, ref)
    
    def test_get_mvar_value(self):
        mvs = self.mvs
        res = mvs._get_single_mvar_value(TimeSymbol)
        self.assertEqual(res, TimeSymbol("t"))
        
        ## now get a variable that is not provided directly but computable in one step
        res = mvs._get_single_mvar_value(SmoothReservoirModel)
        ## now get a variable that is not provided directly but computable in two steps
        res = mvs._get_single_mvar_value(CompartmentalMatrix)
        #print(res)
        ## self.assertTrue(False)

