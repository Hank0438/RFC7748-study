from curve25519 import *

print("##### X25519 case1 #####")
k_byte = 'a546e36bf0527c9d3b16154b82465edd62144c0ac1fc5a18506a2244ba449ac4'
k_int = 31029842492115040904895560451863089656472772604678260265531221036453811406496
k_int_decode = decodeScalar25519(k_byte,255)
#print('k_int:', k_int_decode)
print('check k_int:', k_int_decode == k_int)

u_byte = 'e6db6867583030db3594c1a424b15f7c726624ec26b3353b10a903a6d0ab1c4c'
u_int = 34426434033919594451155107781188821651316167215306631574996226621102155684838
u_int_decode = decodeUCoordinate(u_byte,255)
u_int_encode = encodeUCoordinate(u_int_decode,255)
#print('u_byte:', u_byte)
#print('u_int:', u_int_decode)
print('check u_byte:', u_int_encode == u_byte)
print('check u_int:', u_int_decode == u_int)

output_u_int = scalarMult(u_int, k_int, 255)
output_u_byte = 'c3da55379de9c6908e94ea4df28d084f32eccf03491c71f754b4075577a28552'
output_u_int_encode = encodeUCoordinate(output_u_int, 255)
print('check output_u_int_encode:', output_u_int_encode == output_u_byte)


print("##### X25519 case2 #####")
k_byte = '4b66e9d4d1b4673c5ad22691957d6af5c11b6421e0ea01d42ca4169e7918ba0d'
k_int = 35156891815674817266734212754503633747128614016119564763269015315466259359304
k_int_decode = decodeScalar25519(k_byte,255)
#print('k_int:', k_int_decode)
print('check k_int:', k_int_decode == k_int)

u_byte = 'e5210f12786811d3f4b7959d0538ae2c31dbe7106fc03c3efc4cd549c715a493'
u_int = 8883857351183929894090759386610649319417338800022198945255395922347792736741
u_byte_decode = decodeUCoordinate(u_byte,255)
u_int_encode = encodeUCoordinate(u_int,255)
print('check u_byte:', u_byte == u_int_encode)
print('u_byte:      ', u_byte)
print('u_int_encode:', u_int_encode)
print('check u_int:', u_byte_decode == u_int)
output_u_int = scalarMult(u_int, k_int, 255)
output_u_byte = '95cbde9476e8907d7aade45cb4b873f88b595a68799fa152e6f8f7647aac7957'
output_u_int_encode = encodeUCoordinate(output_u_int, 255)
print('check output_u_int_encode:', output_u_int_encode == output_u_byte)


print("##### X25519 scalarMult iteration #####")
u = decodeUCoordinate("0900000000000000000000000000000000000000000000000000000000000000", 255)
k = decodeScalar25519("0900000000000000000000000000000000000000000000000000000000000000", 255)
for i in range(1000000):
    result = scalarMult(u, k, 255)
    u = decodeUCoordinate(encodeUCoordinate(k, 255), 255)
    k = decodeScalar25519(encodeUCoordinate(result, 255), 255)
    if (i + 1) in [1,2,3, 1000, 1000000]:
        print(u)
        print(k)
        print("After ", i+1, " iteration: ", encodeUCoordinate(result, 255))








print("##### X25519 Diffie-Hellman #####")
privateKey_A = '77076d0a7318a57d3c16c17251b26645df4c2f87ebc0992ab177fba51db92c2a' #scalar
privateKey_A_decode = decodeScalar25519(privateKey_A, 255)
base = 900000000000000000000000000000000000000000000000000000000000000
publicKey_A = scalarMult(9, privateKey_A_decode,  255)
print('publicKey_A: ', encodeUCoordinate(publicKey_A, 255))


privateKey_B = '5dab087e624a8a4b79e17f8b83800ee66f3bb1292618b6fd1c2f8b27ff88e0eb' #scalar
privateKey_B_decode = decodeScalar25519(privateKey_B, 255)
publicKey_B = scalarMult(9, privateKey_B_decode, 255)
print('publicKey_B: ', encodeUCoordinate(publicKey_B, 255))

sharedSecret_A = scalarMult(publicKey_B, privateKey_A_decode,  255)
print("sharedSecret_A: ", encodeUCoordinate(sharedSecret_A, 255))
sharedSecret_B = scalarMult(publicKey_A, privateKey_B_decode,  255)
print("sharedSecret_B: ", encodeUCoordinate(sharedSecret_B, 255))