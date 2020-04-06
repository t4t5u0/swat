
def input_text():
    x = hex(ord(input()))
    if len(x) == 4:
        return ['0x'+x[2:]]
    else:
        return ['0x'+x[2:4], '0x'+x[4:]]

def fnc(text):
    result = []
    for item in text:
        result.append('0b'+bin(eval(item))[2:].zfill(8))
    return result

def fnc_2(arg):
    first = arg[0][2:]
    result = None
    print(len(arg))
    if len(arg) == 2:
        second = arg[1]
        second = second[2:]
        a = '0b1110'+first[:4]
        b = '0b10'+first[4:]+second[:2]
        c = '0b10'+second[2:]
        result = list(map(hex, map(eval, [a, b, c])))
        #print(result)
    else:
        first = '0b' + first
        if 0<= eval(first) <= 127:
            result = [(hex(eval(first)))]
        else:
            pass
    return result

hex_character = (fnc_2(fnc(input_text())))
print(hex_character)


if 0 <= eval(hex_character[0]) <= 127:
    print('1B')
    print((hex_character[0]))
#elif 128 <= eval(hex_character[0]) <= 191:
#    print('2B')
elif 224 <= eval(hex_character[0]) <= 239:
    print('3B')
    a, b, c = map(lambda x: x[2:], map(bin, map(eval, hex_character)))
    result = '0b' + a[4:] + b[2:] + c[2:]
    print(chr(eval(result)))
elif 240 <= eval(hex_character[0]) <= 247:
    print('4B')
elif 248 <= eval(hex_character[0]) <= 251:
    print('5B')
elif 252 <= eval(hex_character[0]) <= 255:
    print('6B')



# 0xe3 0x81 0x82 あ のUTF-8表現
# 0xe3 0b11100011
# 0x81 0b10000001
# 0x82 0b10000010
#     ord('あ')  => 12354
# bin(ord('あ')) => 0b11000001000010
# 0x3042 = 0d12354
# 0x30 0x42 に分割してから二進にして処理する







