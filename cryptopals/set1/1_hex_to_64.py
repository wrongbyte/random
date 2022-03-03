from base64 import b64encode
def encode_hex_to_64(string):
    return b64encode(bytes.fromhex(string.decode())).decode()

hex_string = b'49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
print(encode_hex_to_64(hex_string))