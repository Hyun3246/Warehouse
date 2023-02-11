# 16진수 덧셈 계산기

def hexa_cal():
    final_sum = 0
    while True:
        new_input = input("Only Hexa(blank to finish): ")
        if new_input != ' ':
            new_input = int(new_input, 16)
            final_sum += new_input
            continue
        else:
            break
    
    return hex(final_sum)

print(hexa_cal())
