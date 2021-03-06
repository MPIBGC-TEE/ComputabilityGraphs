"""This module is just a collection of test classes and functions to provide material for text fixures
"""
class SC:
    # a simple class for testing (it's subclasses)
    # as a stand in for the more complex stuff
    def __init__(self,v):
        self.v=v

    def __eq__(self,other):
        return self.v == other.v

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

class A_minus_1:
    pass


class A_minus_2:
    pass


class A0:
    pass


class A1:
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
    return A()


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
    """Computes a from i"""
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
    """Computes c from b"""
    return C()


def d_from_a(a: A) -> D:
    return D()


def d_from_b(b: B) -> D:
    """Computes d from b"""
    return D()


def d_from_g_h(g: G, h: H) -> D:
    """Computes d from g and h"""
    return D(g.v+h.v)


def e_from_b(b: B) -> E:
    """Computes e from b"""
    return E()


def f_from_b(b: B) -> F:
    """Computes f from b"""
    return F()

def j_from_g(g: G) -> J:
    return J()


def a_minus_1_from_a_minus_2(x: A_minus_2) -> A_minus_1:
    return A_minus_1()


def a0_from_a_minus_1(x: A_minus_1) -> A0:
    return A0()


def a1_from_a0(a0: A0) -> A1:
    return A1()


def a2_from_a1(a1: A1) -> A2:
    return A2()

def a3_from_a2(a2: A2) -> A3:
    return A3()


def a3_from_b0(b0: B0) -> A3:
    return A3()


def a0_from_b0(x: B0) -> A0:
    return A0()


def b_minus_1_from_b_minus_2(x: B_minus_2) -> B_minus_1:
    return B_minus_1()


def b0_from_b_minus_1(x: B_minus_1) -> B0:
    return B0()


def b1_from_a2(a2: A2) -> B1:
    return B1()

def b1_from_b0(b0: B0) -> B1:
    return B1()


def b2_from_b1(b1: B1) -> B2:
    return B2()


def b3_from_b2(b2: B2) -> B3:
    return B3()

def b_from_i_j(i: I, j: J) -> B:
    return B()

def d_from_a_c(a: A, c: C) -> D:
    return D()

def d_from_b_c(b: B, c: C) -> D:
    return D()

def b_from_a(a: A) -> B:
    return B()

def f_from_e(e: E) -> F:
    return F()

# for easier debugging in ipython
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

