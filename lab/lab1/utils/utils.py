import struct

def fast_trick_2_byte(token):
    result = []
    for x in token:
        code = list(x.encode('utf8'))
        code = [-1] * (3 - len(code)) + code        
        result += code
    return result

def fast_trick_2_str(token):
    new_token = []
    for x in token:
        if x != -1:
            new_token.append(x)
    return bytes(new_token).decode('utf8')