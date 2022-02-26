from singlebyteXOR import XOR_decode, assign_score

with open('4.txt') as file:
    last_score = 0
    greatest_score = 0
    greatest_score_string = ''
    
    lines = file.readlines()

    for line in lines:
        XORd_string = XOR_decode(line)
        last_score = assign_score(XORd_string)
        
        if (last_score > greatest_score):
            greatest_score = last_score
            greatest_score_string = XORd_string

    print(greatest_score_string)