import sys
input = sys.stdin.readline

def recursion(s, l, r):
    global counter
    counter += 1
    if l >= r: return 1
    elif s[l] != s[r]: return 0
    else: return recursion(s, l+1, r-1)

def isPalindrome(s):
    return recursion(s, 0, len(s)-1)

T = int(input())

for i in range(T):
    counter = 0
    word = input().strip()
    print(isPalindrome(word), counter)