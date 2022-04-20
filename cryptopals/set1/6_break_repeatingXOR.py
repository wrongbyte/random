from itertools import combinations, zip_longest
from singlebyteXOR import XOR_decode_bytes
from repeatingXOR import XOR_repeating_encode
import base64

#TODO: REFACTOR STRUCTURE OF FUNCTIONS

def hamming_distance(string1: bytes, string2: bytes) -> int:
    distance = 0
    for (byte1, byte2) in zip(string1, string2):
        distance += bin(byte1 ^ byte2).count('1')
    return distance

assert hamming_distance(b'this is a test', b'wokka wokka!!!') == 37

with open('6.txt', 'r') as file:
    text = base64.b64decode(file.read())
    print(len(text))

    def find_key_length():
        min_score = len(text)

        for keysize in range(2, 40):
            chunks = [text[start:start + keysize] for start in range(0, len(text), keysize)]
            subgroup = chunks[:4]
            average_score = (sum(hamming_distance(a, b) for a,b in combinations(subgroup, 2)) / 6) / keysize  # dividing the score by 6 gives us the average diff between chunks, dividing it by keysize gives us the average diff between each a, b bytes for chunk1, chunk2
            if average_score < min_score:
                min_score = average_score
                key_length = keysize

        return key_length

    def find_key(key_length = find_key_length()): 
        key_blocks = [text[start:start + key_length] for start in range(0, len(text), key_length)]
        # transpose the 2D matrix
        key = []
        single_XOR_blocks = [list(filter(None,i)) for i in zip_longest(*key_blocks)]
        for block in single_XOR_blocks:
            key_n = XOR_decode_bytes(block)
            key.append(key_n)

        ascii_key = ''.join([chr(c) for c in key])
        return ascii_key.encode()


    print(XOR_repeating_encode(text, find_key()))