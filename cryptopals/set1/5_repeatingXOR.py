input_text = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
XOR_key = "ICE"

def XOR_repeating_encode(input_string, key):
    xord_output = []
    decimal_array = [ord(char) for char in input_string]
    grouped_list = [decimal_array[i:i+ len(key)] for i in range(0, len(decimal_array), len(key))]

    for sublist in grouped_list:
        for i in range((len(sublist))):
            xord_char = hex(int(sublist[i]) ^ ord(XOR_key[i]))
            xord_output.append(str(xord_char)[2:])

    return ('').join(xord_output)

print(XOR_repeating_encode(input_text, XOR_key))