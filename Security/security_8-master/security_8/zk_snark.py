import numpy as np
import sys
from sympy import factor, symbols, factorint, simplify, Poly

from ecpy.curves import Curve, Point

def trust_middle(cv, Xt, t_0):
    A = np.dot(Xt, np.array([1,t_0,t_0*t_0]))
    B = list()
    for i in range(0,len(A)):
        if int(A[i]) == 0:
            B.append(0)
            continue
        B.append(cv.mul_point(cv.order + int(A[i]),G))
    return B

#test
def public_2_x(public_1_x, k_x):
    A = list()
    for i in range(len(public_1_x)):
        if type(public_1_x[i]) == int:
            A.append(0)
            continue
        A.append(cv.mul_point(cv.order + k_x, public_1_x[i]))
    return A


x = symbols('x')
sym1 = x*(x+2)
sym2 = sym1*x
y = (sym2+x+1)

At = np.array([[1,-1.5,0.5], [4,-4,1], [-3,4,-1], [1,-1.5, 0.5], [0,0,0]]) *2
Bt = np.array([[7,-6.5,1.5],[0,1.5,-0.5],[0,0,0],[0,0,0],[0,0,0]]) *2
Ct = np.array([[0,0,0],[0,0,0],[3,-2.5,0.5],[-3,4,-1],[1,-1.5,0.5]]) *4
# 기본 증명식을 QAP화 A[t]

cv = Curve.get_curve('secp256k1')
G = cv.generator

class verifier():
    def __init__(self, t_0, k_a, k_b, k_c, b):
        self.t_0 = t_0
        self.k_a = k_a
        self.k_b = k_b
        self.k_c = k_c
        self.b = b

    def gen_pub_1(self):
        t_0 = self.t_0
        self.public_1_a = trust_middle(cv, At, t_0)
        self.public_1_b = trust_middle(cv, Bt, t_0)
        self.public_1_c = trust_middle(cv, Ct, t_0)
        self.public_1_g = [G, cv.mul_point(cv.order + t_0, G), cv.mul_point(cv.order + t_0 * t_0, G)]
        # public_1_z = cv.mul_point(int(ZP.eval(t_0)), G)

        return self.public_1_a, self.public_1_b, self.public_1_c, self.public_1_g

    def gen_pub_2(self):
        # A[t_0]*G*k_a = (k_a * A[t_0]) * G
        self.public_2_a = public_2_x(self.public_1_a, self.k_a)
        self.public_2_b = public_2_x(self.public_1_b, self.k_b)
        self.public_2_c = public_2_x(self.public_1_c, self.k_c)

        return self.public_2_a, self.public_2_b, self.public_2_c

    def gen_pub_3(self):
        self.public_3 = public_2_x(trust_middle(cv, (At + Bt + Ct), self.t_0), self.b)

        return self.public_3

    def verify_1(self,AT, BT, CT, HT, p_n_a, p_n_b, p_n_c, p_n_h):
        self.AT = AT
        self.BT = BT
        self.CT = CT
        self.HT = HT

        x = symbols('x')
        AP = Poly(np.flip(AT, 0), x)
        BP = Poly(np.flip(BT, 0), x)
        CP = Poly(np.flip(CT, 0), x)
        HP = Poly(np.flip(HT, 0), x)
        print(HP)

        # A(t_0)
        A_t_0 = AP.eval(self.t_0)
        B_t_0 = BP.eval(self.t_0)
        C_t_0 = CP.eval(self.t_0)
        H_t_0 = HP.eval(self.t_0)

        # verifier
        self.v_n_a = cv.mul_point(cv.order + int(A_t_0), G)
        self.v_n_b = cv.mul_point(cv.order + int(B_t_0), G)
        self.v_n_c = cv.mul_point(cv.order + int(C_t_0), G)
        self.v_n_h = cv.mul_point(cv.order + int(H_t_0), G)

        print(p_n_a == self.v_n_a, p_n_b == self.v_n_b , p_n_c == self.v_n_c , p_n_h == self.v_n_h )

        return (p_n_a == self.v_n_a and p_n_b == self.v_n_b and p_n_c == self.v_n_c and p_n_h == self.v_n_h)

    def verify_2(self, p_n_a_2, p_n_b_2, p_n_c_2,):
        self.v_n_a_2 = cv.mul_point(cv.order + self.k_a, self.v_n_a)
        self.v_n_b_2 = cv.mul_point(cv.order + self.k_b, self.v_n_b)
        self.v_n_c_2 = cv.mul_point(cv.order + self.k_c, self.v_n_c)

        print(self.v_n_a_2 == p_n_a_2, self.v_n_b_2 == p_n_b_2, self.v_n_c_2 == p_n_c_2)

        return (self.v_n_a_2 == p_n_a_2 and self.v_n_b_2 == p_n_b_2 and self.v_n_c_2 == p_n_c_2)

    def verify_3(self, p_n):
        v_n = cv.mul_point(cv.order + self.b, (self.v_n_a + self.v_n_b + self.v_n_c))
        return p_n == v_n


class prover():
    def __init__(self, witness):
        self.witness = witness
        self.s = [1, witness, sym1.subs({x:witness}), sym2.subs({x:witness}), y.subs({x:witness})]
        print("witness = ",self.s)

    def QAP(self):
        self.AT = np.dot(self.s, At)
        self.BT = np.dot(self.s, Bt)
        self.CT = np.dot(self.s, Ct)

        x = symbols('x')
        AP = Poly(np.flip(self.AT, 0), x)
        BP = Poly(np.flip(self.BT, 0), x)
        CP = Poly(np.flip(self.CT, 0), x)
        G0 = Poly([1, -1], x)
        G1 = Poly([1, -2], x)
        G2 = Poly([1, -3], x)

        T = (AP * BP - CP) / (G0 * G1 * G2)
        print("DEUBG ",simplify(T))
        self.HT = np.flip(Poly(simplify(T), x).coeffs(), axis=0)
        print("DEBUG2 ", self.HT)
        # QAP 생성 A(t)
        print(self.AT,self.BT,self.CT)

        return self.AT, self.BT, self.CT, self.HT

    # s * trust_middle = s*A[t_0]*G
    def proof_1_x(self, public_1_x):
        A = 0
        chk = 0
        for i in range(len(self.s)):
            if type(public_1_x[i]) == int:
                continue
            if chk == 0:
                chk = 1
                A = cv.mul_point(cv.order + int(self.s[i]), public_1_x[i])
            else:
                A = A + cv.mul_point(cv.order + int(self.s[i]), public_1_x[i])
        return A

    def get_proof_1(self, public_1_a, public_1_b, public_1_c, public_1_g):
        self.p_n_a = self.proof_1_x(public_1_a)
        self.p_n_b = self.proof_1_x(public_1_b)
        self.p_n_c = self.proof_1_x(public_1_c)
        #self.p_n_h = cv.mul_point(int(self.HT[0]) + cv.order, G) + cv.mul_point(int(self.HT[1]), public_1_g)
        self.p_n_h = 0
        for i in range(len(self.HT)):
            if type(self.p_n_h) == int:
                self.p_n_h = cv.mul_point(cv.order + int(self.HT[i]), public_1_g[i])
            else:
                self.p_n_h = self.p_n_h + cv.mul_point(cv.order + int(self.HT[i]), public_1_g[i])
        return self.p_n_a, self.p_n_b, self.p_n_c, self.p_n_h

    def get_proof_2(self, public_2_a, public_2_b, public_2_c):
        self.p_n_a_2 = self.proof_1_x(public_2_a)
        self.p_n_b_2 = self.proof_1_x(public_2_b)
        self.p_n_c_2 = self.proof_1_x(public_2_c)

        return self.p_n_a_2, self.p_n_b_2, self.p_n_c_2

    def get_proof_3(self, public_3):
        self.p_n = self.proof_1_x(public_3)
        return self.p_n