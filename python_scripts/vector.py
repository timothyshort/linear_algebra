from math import acos
from decimal import Decimal, getcontext

getcontext().prec = 30
tolerance = 1e-10



class Vector(object):
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple(coordinates)
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')


    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def __iter__(self):
        self.current = 0
        return self

    def next(self):
        if self.current >= len(self.coordinates):
            raise StopIteration
        else:
            current_value = self.coordinates[self.current]
            self.current += 1
            return current_value

    def __len__(self):
        return len(self.coordinates)

    def __getitem__(self, i):
        return self.coordinates[i]

    def add(self,v):
        #newVector = [x+y for x,y in zip(self.coordinates,v.coordinates)]
        newVector = []
        n = len(self.coordinates)
        for i in range(n):
            newVector.append(self.coordinates[i] + v.coordinates[i])
        return Vector(newVector)

    def subtract(self,v):
        newVector = [x-y for x,y in zip(self.coordinates,v.coordinates)]
        return Vector(newVector)

    def magnitude(self):
        squaredCoordinates = [x**2 for x in self.coordinates]
        return (sum(squaredCoordinates))**.5

    def scalar(self,k):
        newVector = [x*k for x in self.coordinates]
        return Vector(newVector)

    def normal(self):
        return self.scalar(1/self.magnitude())

    def dotprod(self, v):
        dotproduct = sum([x*y for x,y in zip(self.coordinates,v.coordinates)])
        return dotproduct

    def angle(self, v, type):
        u1 = self.normal()
        u2 = v.normal()
        dotproduct = u1.dotprod(u2)
        if (type == "Radians"):
            return acos(dotproduct)
        else:
            return (acos(dotproduct) * (180/3.1415))

    def is_parallel(self, v):
        #Parallel - scalar multiple
        newVector = [x/y for x,y in zip(self.coordinates,v.coordinates)]
        for i in range(len(newVector)):
            if (abs(newVector[0]-newVector[i]) > tolerance) :
                return "Not Parallel"
        return "Parallel"


    def is_orthogonal(self, v):
        #Orthogonal - v (dot) w = 0
        if (abs(self.dotprod(v)) > tolerance):
            return "Not Orthogonal"
        return "Orthogonal"

    def comp_parallel(self, b):
        u = b.normal()
        k = self.dotprod(u)
        return u.scalar(k)

    def comp_orthogonal(self, b):
        projection = self.comp_parallel(b)
        return self.subtract(projection)

    def cross(self, w):
        newVector = []
        newVector.append(self.coordinates[1]*w.coordinates[2] - w.coordinates[1]*self.coordinates[2])
        newVector.append(-(self.coordinates[0]*w.coordinates[2] - w.coordinates[0]*self.coordinates[2]))
        newVector.append(self.coordinates[0]*w.coordinates[1] - w.coordinates[0]*self.coordinates[1])
        return Vector(newVector)

    def area_parallelogram(self, w):
        return (self.cross(w)).magnitude()

    def area_triangle(self, w):
        return ((self.cross(w)).magnitude())/2

if __name__ == '__main__':
    v = Vector([2,3,4])
    w = Vector([3,4,5])
    print v.cross(w)
    print v.area_triangle(w)