from math import sqrt
from modularSqrt import *
from Crypto.Util.number import bytes_to_long, long_to_bytes, inverse

'''
Montgomery curve
v^2 = u^3 + A*u^2 + u
'''

p = pow(2,255) - 19

class curve25519:
    def __init__(self):
        '''
        base point 
        '''
        self.u = 9 
        self.v = 14781619447589544791020593568409986887264606134616475288964881837755586237401
        '''
        curve25519
        '''
        self.p = pow(2,255) - 19
        self.A = 486662
        self.order = pow(2,255) + 0x14def9dea2f79cd65812631a5cf5d3ed
        self.cofactor = 8

    def birationalMap(self):
        x = (modular_sqrt(-486664, self.p) * self.u) * inverse(self.v, self.p) # x or p-x
        y = (self.u - 1) * inverse(self.u + 1, self.p)
        return ((self.p - x) % self.p, y % self.p) 

        
'''
twisted Edwards curve 
-x^2 + y^2 = 1 + d*x^2*y^2

The birational maps are:
(u, v) = ((1+y)/(1-y), sqrt(-486664)*u/x)
(x, y) = (sqrt(-486664)*u/v, (u-1)/(u+1))
'''

class edwards25519:
    def __init__(self):
        self.p = pow(2,255) - 19
        self.d = 37095705934669439343138083508754565189542113879843219016388785533085940283555
        self.order = pow(2,255) + 0x14def9dea2f79cd65812631a5cf5d3ed
        self.cofactor = 8
        self.x = 15112221349535400772501151409588531511454012693041857206046113283949847762202
        self.y = 46316835694926478169428394003475163141307993866256225615783033603165251855960

    def birationalMap(self):
        u = (1 + self.y) * inverse(1 - self.y, self.p)
        v = (modular_sqrt(-486664, self.p) * u) * inverse(self.x, self.p)
        return (u % self.p, (self.p - v) % self.p)

def decodeLittleEndian(b, bits):
    return sum([b[i] << 8*i for i in range((bits+7)//8)]) # (255 + 7) // 8 = 32

def decodeUCoordinate(u, bits):
    u_list = [int(u[i*2:(i+1)*2], 16) for i in range((bits+7)//8)]
    # Ignore any unused bits.
    if bits % 8:
        #u_list[-1] &= 0x7f
        u_list[-1] &= (1<<(bits%8))-1
    return decodeLittleEndian(u_list, bits)
    
def encodeUCoordinate(u, bits):
    u = u % p
    s = ""
    for i in range((bits+7)//8):
        c = (hex((u >> 8*i) & 0xff)[2:]).rjust(2, '0')
        #print(c)
        s += c
    return s
    #return "".join([hex((u >> 8*i) & 0xff)[2:] for i in range((bits+7)//8)])

def decodeScalar25519(k, bits):
    k_list = [int(k[i*2:(i+1)*2], 16) for i in range((bits+7)//8)]
    k_list[0] &= 248
    k_list[31] &= 127
    k_list[31] |= 64
    return decodeLittleEndian(k_list, 255)


def scalarMult(u, k, bits): # scalar multiplication
    x_1 = u
    x_2 = 1
    z_2 = 0
    x_3 = u
    z_3 = 1
    swap = 0
    a24 = 121665
    for t in range(bits)[::-1]: # t = bits-1 down to 0
        k_t = (k >> t) & 1
        swap ^= k_t
        #Conditional swap
        (x_2, x_3) = cswap(swap, x_2, x_3)
        (z_2, z_3) = cswap(swap, z_2, z_3)
        swap = k_t
        
        A = (x_2 + z_2) % p
        AA = pow(A,2,p)
        B = (x_2 - z_2) % p
        BB = pow(B,2,p)
        E = (AA - BB) % p
        C = (x_3 + z_3) % p
        D = (x_3 - z_3) % p
        DA = (D * A) % p
        CB = (C * B) % p
        x_3 = pow(DA + CB,2,p)
        z_3 = (x_1 * pow(DA - CB,2,p)) % p
        x_2 = (AA * BB) % p
        z_2 = (E * (AA + a24 * E)) % p
        
    #Conditional swap
    (x_2, x_3) = cswap(swap, x_2, x_3)
    (z_2, z_3) = cswap(swap, z_2, z_3)
    return (x_2 * pow(z_2, p-2, p)) % p  #equal to (x_2 * inverse(z_2, p)) % p


def cswap(swap, x_2, x_3):
    dummy = (0 - swap) & (x_2 ^ x_3)
    x_2 ^= dummy
    x_3 ^= dummy
    return (x_2, x_3)

if __name__ == '__main__':

    print("main")
    print(((486662 - 2) * inverse(4, p)) % p) # a24 = 121665
    print(hex(122)[2:])
    print(-1 & 123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890)
    print(0 & 123456789)
    print(1 & 123456789)

