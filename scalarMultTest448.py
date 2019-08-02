from curve448 import *

print("##### X448 case1 #####")
k_byte = '3d262fddf9ec8e88495266fea19a34d28882acef045104d0d1aae121700a779c984c24f8cdd78fbff44943eba368f54b29259a4f1c600ad3'
k_int = 599189175373896402783756016145213256157230856085026129926891459468622403380588640249457727683869421921443004045221642549886377526240828
k_int_decode = decodeScalar448(k_byte,448)
#print('k_int:', k_int_decode)
print('check k_int:', k_int_decode == k_int)

u_byte = '06fce640fa3487bfda5f6cf2d5263f8aad88334cbd07437f020f08f9814dc031ddbdc38c19c6da2583fa5429db94ada18aa7a7fb4ef8a086'
u_int = 382239910814107330116229961234899377031416365240571325148346555922438025162094455820962429142971339584360034337310079791515452463053830
u_byte_decode = decodeUCoordinate(u_byte,448)
u_int_encode = encodeUCoordinate(u_int,448)
print('check u_byte:', u_int_encode == u_byte)
#print('u_int_encode:', u_int_encode)
#print('u_byte:      ', u_byte)
print('check u_int: ', u_byte_decode == u_int)
#print('u_byte_decode:', u_byte_decode)
#print('u_int:       ', u_int)

output_u_int = scalarMult(u_int, k_int, 448)
output_u_byte = 'ce3e4ff95a60dc6697da1db1d85e6afbdf79b50a2412d7546d5f239fe14fbaadeb445fc66a01b0779d98223961111e21766282f73dd96b6f'
output_u_int_encode = encodeUCoordinate(output_u_int, 448)
#print('output_u_int_encode: ', output_u_int_encode)
#print('output_u_byte:       ', output_u_byte)
print('check output_u_int_encode:', output_u_int_encode == output_u_byte)







print("##### X448 case2 #####")
k_byte = '203d494428b8399352665ddca42f9de8fef600908e0d461cb021f8c538345dd77c3e4806e25f46d3315c44e0a5b4371282dd2c8d5be3095f'
k_int = 633254335906970592779259481534862372382525155252028961056404001332122152890562527156973881968934311400345568203929409663925541994577184
k_int_decode = decodeScalar448(k_byte,448)
#print('k_int:', k_int_decode)
print('check k_int:', k_int_decode == k_int)

u_byte = '0fbcc2f993cd56d3305b0b7d9e55d4c1a8fb5dbb52f8e9a1e9b6201b165d015894e56c4d3570bee52fe205e28a78b91cdfbde71ce8d157db'
u_int = 622761797758325444462922068431234180649590390024811299761625153767228042600197997696167956134770744996690267634159427999832340166786063
u_byte_decode = decodeUCoordinate(u_byte,448)
u_int_encode = encodeUCoordinate(u_int,448)
print('check u_byte:', u_int_encode == u_byte)
#print('u_int_encode:', u_int_encode)
#print('u_byte:      ', u_byte)
print('check u_int: ', u_byte_decode == u_int)
#print('u_byte_decode:', u_byte_decode)
#print('u_int:       ', u_int)

output_u_int = scalarMult(u_int, k_int, 448)
output_u_byte = '884a02576239ff7a2f2f63b2db6a9ff37047ac13568e1e30fe63c4a7ad1b3ee3a5700df34321d62077e63633c575c1c954514e99da7c179d'
output_u_int_encode = encodeUCoordinate(output_u_int, 448)
#print('output_u_int_encode: ', output_u_int_encode)
#print('output_u_byte:       ', output_u_byte)
print('check output_u_int_encode:', output_u_int_encode == output_u_byte)




print("##### X448 scalarMult iteration #####")

u = decodeUCoordinate("0500000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000", 448)
k = decodeScalar448("0500000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000", 448)
for i in range(1000000):
    result = scalarMult(u, k, 448)
    u = decodeUCoordinate(encodeUCoordinate(k, 448), 448)
    k = decodeScalar448(encodeUCoordinate(result, 448), 448)
    if (i + 1) in [1,2,3, 1000, 1000000]:
        print(u)
        print(k)
        print("After ", i+1, " iteration: ", encodeUCoordinate(result, 448))




'''
Alice’s private key, a:
    9a8f4925d1519f5775cf46b04b5800d4ee9ee8bae8bc5565d498c28dd9c9baf574a9419744897391006382a6f127ab1d9ac2d8c0a598726b
Alice’s public key, X448(a, 5):
    9b08f7cc31b7e3e67d22d5aea121074a273bd2b83de09c63faa73d2c22c5d9bbc836647241d953d40c5b12da88120d53177f80e532c41fa0
Bob’s private key, b:
    1c306a7ac2a0e2e0990b294470cba339e6453772b075811d8fad0d1d6927c120bb5ee8972b0d3e21374c9c921b09d1b0366f10b65173992d
Bob’s public key, X448(b, 5):
    3eb7a829b0cd20f5bcfc0b599b6feccf6da4627107bdb0d4f345b43027d8b972fc3e34fb4232a13ca706dcb57aec3dae07bdc1c67bf33609
Their shared secret, K:
    07fff4181ac6cc95ec1c16a94a0f74d12da232ce40a77552281d282bb60c0b56fd2464c335543936521c24403085d59a449a5037514a879d
'''

privateKey_A = '9a8f4925d1519f5775cf46b04b5800d4ee9ee8bae8bc5565d498c28dd9c9baf574a9419744897391006382a6f127ab1d9ac2d8c0a598726b' #scalar
privateKey_A_decode = decodeScalar448(privateKey_A, 448)
publicKey_A = scalarMult(5, privateKey_A_decode,  448)
print('publicKey_A: ', encodeUCoordinate(publicKey_A, 448))


privateKey_B = '1c306a7ac2a0e2e0990b294470cba339e6453772b075811d8fad0d1d6927c120bb5ee8972b0d3e21374c9c921b09d1b0366f10b65173992d' #scalar
privateKey_B_decode = decodeScalar448(privateKey_B, 448)
publicKey_B = scalarMult(5, privateKey_B_decode, 448)
print('publicKey_B: ', encodeUCoordinate(publicKey_B, 448))

sharedSecret_A = scalarMult(publicKey_B, privateKey_A_decode, 448)
print("sharedSecret_A: ", encodeUCoordinate(sharedSecret_A, 448))
sharedSecret_B = scalarMult(publicKey_A, privateKey_B_decode, 448)
print("sharedSecret_B: ", encodeUCoordinate(sharedSecret_B, 448))