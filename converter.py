def convert(numb):
    code = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I', 10: 'J', 11: 'K', 12: 'L', 13: 'M',
            14: 'N', 15: 'O', 16: 'P', 17: 'Q', 18: 'R', 19: 'S', 20: 'T', 21: 'U', 22: 'V', 23: 'W', 24: 'X',
            25: 'Y', 26: 'Z'}
    last_let = numb % 26
    digit = numb // 26
    if digit > 0:
        let = code[digit] + code[last_let]
    else:
        let = code[last_let]
    return let
if __name__ == "__main__":
    a = int(input())
    b =  convert(a)
    print(b)
