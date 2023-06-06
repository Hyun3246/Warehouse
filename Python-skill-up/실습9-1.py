# 3차원 좌표 계산이 가능한 클래스 (덧셈, 뺄셈, 스칼라 곱셈 가능)

class Point():
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self):
        result = '({}, {}, {})'.format(self.x, self.y, self.z)
        return result

    
    def __repr__(self):
        result = '({}, {}, {})'.format(self.x, self.y, self.z)
        return result
    
    def __add__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        

    def __sub__(self, other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z

    def __mul__(self, n):
        self.x *= n
        self.y *= n
        self.z *= n

    def __rmul__(self, n):
        self.x *= n
        self.y *= n
        self.z *= n

a = Point(1, 2, 3)
b = Point(4, 5, 6)

4 * a
print(a)
