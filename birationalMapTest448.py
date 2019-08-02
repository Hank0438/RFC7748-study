from curve448 import *

print("##### c448 <-> ed448 ######")
c448 = curve448()
print("c448's coordinate:", (c448.u, c448.v))
coord = c448.birationalMap_ed448()
print("ed448's coordinate:", coord)

ed448 = edwards448()
print("ed448's coordinate:", (ed448.x, ed448.y))
coord = ed448.birationalMap()
print("c448's coordinate:", coord)

print("##### c448 <-> goldilocks ######")
print("c448's coordinate:", (c448.u, c448.v))
coord = c448.birationalMap_goldilocks()
print("goldilocks's coordinate:", coord)

goldilocks = goldilocks()
print("goldilocks's coordinate:", (goldilocks.x, goldilocks.y))
coord = goldilocks.birationalMap()
print("c448's coordinate:", coord)