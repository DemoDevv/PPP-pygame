import math


class Vec2d():

    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def __add__(self, o):
        x = self.x + o.x
        y = self.y + o.y

        return Vec2d((x, y))
    
    def __sub__(self, o):
        x = self.x - o.x
        y = self.y - o.y

        return Vec2d((x, y))

    def __eq__(self, o):
        return self.x == o.x and self.y == o.y
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def normalize(self):
        norm = self.magnitude()
        self.x /= norm
        self.y /= norm

    def magnitude(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def to_tuple(self):
        return (self.x, self.y)
    
    def dot(self, o):
        return self.x * o.x + self.y * o.y
    
    def product(self, o):
        return self.x * o.y - self.y * o.x