# two equal-length buffers, produce their XOR combination
from binascii import unhexlify

str1 = b'1c0111001f010100061a024b53535009181c'
str2 = b'686974207468652062756c6c277320657965'

def fixed_xor(string1: bytes, string2: bytes) -> bytes:
    string1_decoded = unhexlify(string1)
    string2_decoded = unhexlify(string2)
    return bytes([ x^y for (x,y) in zip(string1_decoded, string2_decoded)])

print(fixed_xor(str1, str2).hex())