# from https://medium.com/analytics-vidhya/crypto-basics-understand-create-your-own-base64-encoding-with-python-a1481686a35a

from string import ascii_lowercase, ascii_uppercase

ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
digits = '0123456789'
base64_alphabet = ascii_uppercase + ascii_lowercase + digits + '/'

to_encode = input('base64 encoder ->')
chunks_8bit = ''.join([format(bits, '08b') for bits in to_encode.encode('utf8')])

# para converter para base64, primeiro precisamos converter de 8bits para 6bits

chunks_6bit = [chunks_8bit[bits:bits+6] for bits in range(0, len(chunks_8bit), 6)]

padding_amount = (6 - len(chunks_6bit[len(chunks_6bit)-1]))

chunks_6bit[len(chunks_6bit)-1] += padding_amount * '0'