input_text1 = b"Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
XOR_key = b"ICE"

def XOR_repeating_encode(input_string: bytes, key: bytes) -> bytes:
    xord_output = []

    for i in range(len(input_string)):
        xord_output.append(input_string[i] ^ key[i % len(key)])

    return bytes(xord_output).hex()

print(XOR_repeating_encode(input_text1, XOR_key))