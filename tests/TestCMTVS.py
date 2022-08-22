import unittest
from ComputabilityGraphs.CMTVS import CMTVS
from ComputabilityGraphs.Node import Node


from testComputers import (
    A, B, C, D, E, F, G, H,
    a_from_i,
    a_from_b_c,
    b_from_c_d,
    c_from_e_f,
    d_from_g_h,
)
class TestCMTVS(unittest.TestCase):
    def setUp(self):
        self.provided_values = {
            E(1),
            F(1),
            G(1),
            H(1)
        }
        self.computers = {
            a_from_i,
            b_from_c_d,
            c_from_e_f,
            d_from_g_h
        }
        self.cmtvs=CMTVS(
            self.provided_values,
            self.computers
        )

    def test_repr(self):
        print(self.cmtvs)

    def test_update(self):
        c_new = self.cmtvs.update({H(2)})
        res = c_new.get_H()
        self.assertEqual(res.v,2)
    
    def test_provided_mvar_values(self):
        self.assertSetEqual(
        self.cmtvs.provided_mvar_values,
            self.provided_values
        )
        
    def test_provided_mvar_types(self):
        ref = frozenset(
                [
                    type(v) 
                    for v in self.provided_values
                ]
        ) 
        print(ref)
        self.assertSetEqual(
            self.cmtvs.provided_mvar_types,
            ref
        )

    def test_computable_mvar_types(self):
        res = self.cmtvs.computable_mvar_types()
        print(res)
        self.assertSetEqual(
            res, 
            frozenset(
                [B, C, D, E, F, G, H]
            )
        )

    def test_paths_to_single_mvar(self):
        cmtvs = self.cmtvs
        pd = cmtvs.path_dict_to_single_mvar(B)
        startNode = frozenset(
            [G,H,E,F]
        )
        paths = pd[startNode]
        
        res = paths[0]
        ref = [startNode, Node({C, D}), Node({B})]
        self.assertEqual(res, ref)

    def test_get_single_value(self):
        cmtvs = self.cmtvs
        res = cmtvs._get_single_value(E)
        self.assertEqual(res, E(1))
        
        ## now get a variable that is not provided directly but computable in one step
        #res = cmtvs._get_single_value(C)
        #self.assertEqual(res,C(2)) 
        ## now get a variable that is not provided directly but computable in two steps
        res = cmtvs._get_single_value(B)
        print(res)
        self.assertEqual(res,B(4))


    def test_get_single_value_by_depgraph(self):
        
        cmtvs = self.cmtvs

        self.assertEqual( 
            cmtvs._get_single_value_by_depgraph(E),
            E(1)
        )
        
        # now get a variable that is not provided directly but computable in one step
        self.assertEqual( 
            cmtvs._get_single_value_by_depgraph(C),
            C(2)
        )
        #self.assertEqual(res,C(2)) 
        # now get a variable that is not provided directly but computable in two steps
        self.assertEqual( 
            cmtvs._get_single_value_by_depgraph(B),
            B(4)
        )
        # now we create a situation where there are more than one possible depgraph
        # because there is a variable with are more than one computers providing it. 
        computers={
            a_from_i,
            a_from_b_c, 
            b_from_c_d,
            c_from_e_f,
            d_from_g_h
        }
        provided_values = {
            E(1),
            F(1),
            G(1),
            H(1)
        }
        cmtvs = CMTVS(
            provided_values,
            computers
        )
        self.assertEqual( 
            cmtvs._get_single_value_by_depgraph(A),
            A(6)
        )
