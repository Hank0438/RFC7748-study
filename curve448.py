from math import sqrt
from modularSqrt import *
from Crypto.Util.number import bytes_to_long, long_to_bytes, inverse

'''
Montgomery curve
v^2 = u^3 + A*u^2 + u
'''

p = pow(2,448) - pow(2,224) - 1

class curve448:
    def __init__(self):
        '''
        base point 
        '''
        self.u = 5
        self.v = 355293926785568175264127502063783334808976399387714271831880898435169088786967410002932673765864550910142774147268105838985595290606362
        '''
        curve448
        '''
        self.p = pow(2,448) - pow(2,224) - 1
        self.A = 156326
        self.order = pow(2,446) - 0x8335dc163bb124b65129c96fde933d8d723a70aadc873d6d54a7bb0d
        self.cofactor = 4

    def birationalMap_ed448(self):
        x = (modular_sqrt(156324, self.p) * self.u) * inverse(self.v, self.p) # x or p-x
        y = (1 + self.u) * inverse(1 - self.u, self.p)
        return ((self.p - x) % self.p, y % self.p) 

    def birationalMap_goldilocks(self):
        '''
        (x, y) = (4*v*(u^2 - 1)                 /  (u^4 - 2*u^2 + 4*v^2 + 1),
                 -(u^5 - 2*u^3 - 4*u*v^2 + u)   /  (u^5 - 2*u^2*v^2 - 2*u^3 - 2*v^2 + u))
        '''
        x_numerator = 4 * self.v * (pow(self.u,2,self.p) - 1)
        x_denominator = pow(self.u,4,self.p) - 2*pow(self.u,2,self.p) + 4*pow(self.v,2,self.p) + 1
        x = (x_numerator % self.p) * inverse(x_denominator, self.p)
        
        y_numerator = - (pow(self.u,5,self.p) - 2*pow(self.u,3,self.p) - 4*self.u*pow(self.v,2,self.p) + self.u)
        y_denominator = pow(self.u,5,self.p) - 2*pow(self.u,2,self.p)*pow(self.v,2,self.p) - 2*pow(self.u,3,self.p) - 2*pow(self.v,2,self.p) + self.u
        y = (y_numerator) * inverse(y_denominator, self.p)
        return (x % self.p, y % self.p) 
        
'''
Edwards curve 
x^2 + y^2 = 1 + d*x^2*y^2

The birational maps are:
(u, v) = ((y-1)/(y+1), sqrt(156324)*u/x)
(x, y) = (sqrt(156324)*u/v, (1+u)/(1-u))
'''

class edwards448:
    def __init__(self):
        self.p = pow(2,448) - pow(2,224) - 1
        self.d = 611975850744529176160423220965553317543219696871016626328968936415087860042636474891785599283666020414768678979989378147065462815545017
        self.order = pow(2,446) - 0x8335dc163bb124b65129c96fde933d8d723a70aadc873d6d54a7bb0d
        self.cofactor = 4
        self.x = 345397493039729516374008604150537410266655260075183290216406970281645695073672344430481787759340633221708391583424041788924124567700732
        self.y = 363419362147803445274661903944002267176820680343659030140745099590306164083365386343198191849338272965044442230921818680526749009182718

    def birationalMap(self):
        u = (self.y - 1) * inverse(self.y + 1, self.p)
        v = (modular_sqrt(156324, self.p) * u) * inverse(self.x, self.p)
        return (u % self.p, (self.p - v) % self.p)

'''
Edwards curve 
x^2 + y^2 = 1 + d*x^2*y^2

The birational maps are:
(u, v) = (y^2/x^2, (2 - x^2 - y^2)*y/x^3)
(x, y) = (4*v*(u^2 - 1)/(u^4 - 2*u^2 + 4*v^2 + 1),
-(u^5 - 2*u^3 - 4*u*v^2 + u)/
(u^5 - 2*u^2*v^2 - 2*u^3 - 2*v^2 + u))
'''

class goldilocks:
    def __init__(self):
        self.p = pow(2,448) - pow(2,224) - 1
        self.d = -39081
        self.order = pow(2,446) - 0x8335dc163bb124b65129c96fde933d8d723a70aadc873d6d54a7bb0d
        self.cofactor = 4
        self.x = 224580040295924300187604334099896036246789641632564134246125461686950415467406032909029192869357953282578032075146446173674602635247710
        self.y = 298819210078481492676017930443930673437544040154080242095928241372331506189835876003536878655418784733982303233503462500531545062832660

    def birationalMap(self):
        XX = pow(self.x,2,self.p)
        XXX = pow(self.x,3,self.p)
        YY = pow(self.y,2,self.p)
        u = YY * inverse(XX, self.p)
        v = (((2 - XX - YY) * self.y) % p) * inverse(XXX, self.p)
        return (u % self.p, v % self.p)

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


def decodeScalar448(k, bits):
    k_list = [int(k[i*2:(i+1)*2], 16) for i in range((bits+7)//8)]
    k_list[0] &= 252
    k_list[55] |= 128
    return decodeLittleEndian(k_list, 448)

def scalarMult(u, k, bits): # scalar multiplication
    x_1 = u
    x_2 = 1
    z_2 = 0
    x_3 = u
    z_3 = 1
    swap = 0
    a24 = 39081
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
    print(((156326 - 2) * inverse(4, p)) % p) # a24 = 39081