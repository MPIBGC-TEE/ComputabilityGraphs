"""This module is just a collection of test classes and functions to provide material for text fixures
"""
class SC:
    # a simple class for testing (it's subclasses)
    # as a stand in for the more complex stuff
    def __init__(self,v):
        self.v=v

    def __eq__(self,other):
        return self.v == other.v

    # The hash method involving the type is necessary for sets and frozensets since 
    # oddly enoght {A(1),B(1)} reduces to {B(1)} which would be disastrous
    def __hash__(self):
        return hash(self.v)*hash(type(self))

    def __str__(self):
        return type(self).__name__+ "(" + str(self.v) + ")"


class A(SC):
    pass


class B(SC):
    pass


class C(SC):
    pass


class D(SC):
    pass


class E(SC):
    pass


class F(SC):
    pass


class G(SC):
    pass


class H(SC):
    pass


class I(SC):
    pass


class J(SC):
    pass


class K(SC):
    pass


class L(SC):
    pass


class M(SC):
    pass


class N(SC):
    pass


class O(SC):
    pass


class P(SC):
    pass


class Q(SC):
    pass


class R(SC):
    pass


class S(SC):
    pass

class T(SC):
    pass

class A2:
    pass


class A3:
    pass


class B_minus_2:
    pass


class B_minus_1:
    pass


class B0:
    pass


class B1:
    pass


class B2:
    pass


class B3:
    pass



class X:
    pass


class Y:
    pass


class Z:
    pass


def a_from_b_c(b: B, c: C) -> A:
    return A(b.v+c.v)


def a_from_b_d(b: B, d: D) -> A:
    return A()


def a_from_x(x: X) -> A:
    return A()


def a_from_y(y: Y) -> A:
    return A()


def b_from_y(y: Y) -> B:
    return B()


def a_from_z(z: Z) -> A:
    return A()


def b_from_z(z: Z) -> B:
    return B()

def b_from_x(x: X) -> B:
    return B()

def c_from_z(z: Z) -> C:
    return C()

def c_from_e_f(e: E,f:F) -> C:
    return C(e.v + f.v)

def a_from_i(i: I) -> A:
    return A()

def a_from_g_h(g:G, h:H) -> A:
    return A()

def a_from_e_f(e:E, f:F) -> A:
    return A()


def b_from_c_d(c: C, d: D) -> B:
    return B(c.v+d.v)


def b_from_d_e(d: D, e: E) -> B:
    return B()


def b_from_e_f(e: E, f: F) -> B:
    return B()


def b_from_i_j(i: I, j: J) -> B:
    return B()


def c_from_b(b: B) -> C:
    return C()


def d_from_a(a: A) -> D:
    return D()


def d_from_b(b: B) -> D:
    return D()


def d_from_g_h(g: G, h: H) -> D:
    return D(g.v+h.v)


def e_from_b(b: B) -> E:
    return E()


def f_from_b(b: B) -> F:
    return F()


def j_from_g(g: G) -> J:
    return J()


def a3_from_a2(a2: A2) -> A3:
    return A3()


def a3_from_b0(b0: B0) -> A3:
    return A3()


def b_minus_1_from_b_minus_2(x: B_minus_2) -> B_minus_1:
    return B_minus_1()


def b1_from_a2(a2: A2) -> B1:
    return B1()


def b1_from_b0(b0: B0) -> B1:
    return B1()


def d_from_a_c(a: A, c: C) -> D:
    return D()


def d_from_b_c(b: B, c: C) -> D:
    return D()


def b_from_a(a: A) -> B:
    return B()


def f_from_e(e: E) -> F:
    return F()


def g_from_i_j_k(
        i: I,
        j: J,
        k: K
) -> G:
    return G()


def g_from_p_q(
        p: P,
        q: Q
) -> G:
    return G()


def h_from_i_l(
        i: I,
        l: L
) -> H:
    return H()


def j_from_i_p_q(
        i: I,
        p: P,
        q: Q
) -> J:
    return J()


def k_from_g_i(
        g: G,
        i: I
) -> K:
    return K()

# fake (no equivalent in  bgc_md2)
def k_from_r_s(
        r: R,
        s: S 
) -> K:
    return K()


def p_from_r_s(
        r: R,
        s: S 
) -> P:
    return P()


def l_from_h_i(
        h: H,
        i: I
) -> L:
    return L()


def o_from_i_k(
        i: I,
        k: K,
) -> O:
    return O()


def p_from_i_j_k(
        i: I,
        j: J,
        k: K
) -> P:
    return P()


def q_from_i_j_k(
        i: I,
        j: J,
        k: K
) -> Q:
    return Q()


computers = frozenset(
    {
        a_from_i,
        b_from_c_d,
        b_from_e_f,
        c_from_b,
        d_from_b,
        d_from_g_h,
        e_from_b,
        f_from_b,
    }
)
