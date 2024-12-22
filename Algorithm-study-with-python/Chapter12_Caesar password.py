import string

rotation = 3
P = 'CALM'
C = ''

for letter in P:
    C = C + (chr(ord(letter) + rotation))


print(C)
