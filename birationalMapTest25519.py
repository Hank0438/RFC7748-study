from curve25519 import *

c25519 = curve25519()
print("c25519's coordinate:", (c25519.u, c25519.v))
coord = c25519.birationalMap()
print("ed25519's coordinate:", coord)

ed25519 = edwards25519()
print("ed25519's coordinate:", (ed25519.x, ed25519.y))
coord = ed25519.birationalMap()
print("c25519's coordinate:", coord)