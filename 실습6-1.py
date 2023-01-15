import re

def follow_the_rule(number):
    if re.match(r'\d{3}[- ]', number):
        return 'Correct'
    else:
        return 'Error'

print(follow_the_rule('393-4460'))