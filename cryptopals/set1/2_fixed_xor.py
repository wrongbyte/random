# two equal-length buffers, produce their XOR combination
# 1 - hex decode 2 - XOR against another string
import codecs

str1 = '1c0111001f010100061a024b53535009181c'
str2 = '686974207468652062756c6c277320657965'
# the XOR operator works on integers and returns the result in decimal format.
# so, first we have to convert the strings from hex to int. then, we convert the result back to hex

def fixed_xor(string1, string2):
    result = hex(int(string1, 16) ^ int(string2, 16))
    print (result)

fixed_xor(str1, str2)