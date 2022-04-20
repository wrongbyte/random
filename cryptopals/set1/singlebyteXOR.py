from textwrap import wrap
encoded_str = b'1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'

# check letter frequency to choose the most english-like output, i.e ETAOIN SHRDLU
# outputs the str with highest score

def assign_score(output_string):
    string_score = 0
    freq = [' ', 'e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'u']
    for letter in output_string:
        if letter in freq:
            string_score += 1
    return string_score

def XOR_decode(encoded_string):
    encoded_string = encoded_string.decode()
    last_score = 0
    greatest_score = 0

    bytes_array = wrap(encoded_string, 2) # split every two hex letters (every byte)
    decimal_string = [int(byte, 16) for byte in bytes_array] # convert each byte to decimal form to perform XOR op

    for n in range(256): # checks for every possible value for XOR key
        xord_str = [byte ^ n for byte in decimal_string]
        xord_ascii = ('').join([chr(b) for b in xord_str])
        last_score = assign_score(xord_ascii)
        if (last_score > greatest_score):
            greatest_score = last_score
            key = n

    return key

#TODO: REFACTOR
def XOR_decode_bytes(encoded_array):
    last_score = 0
    greatest_score = 0
    for n in range(256): # checks for every possible value for XOR key
        xord_str = [byte ^ n for byte in encoded_array]
        xord_ascii = ('').join([chr(b) for b in xord_str])
        last_score = assign_score(xord_ascii)
        if (last_score > greatest_score):
            greatest_score = last_score
            key = n
    return key

print(XOR_decode(encoded_str))
# print(XOR_decode(encoded_str))