import re

user_search = input("문자열을 입력하세요: ")

output = re.sub(r'(\s+)\1', r'\1', user_search, flags=re.I)

print(output)