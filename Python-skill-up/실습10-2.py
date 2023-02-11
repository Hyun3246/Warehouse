from decimal import Decimal

class Money(Decimal):
    
    def __init__(self, v, units = 'USD'):
        super().__init__(v)
        self.units = units
    
    def __add__(self, other):
        return Money(self.v + other.v, 'USD')

m1 = Money('0.11', 'USD')
m2 = Money('0.15', 'USD')

print(m1)
