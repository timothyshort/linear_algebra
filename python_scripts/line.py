from decimal import Decimal, getcontext

from vector import Vector

getcontext().prec = 30


class Line(object):

    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self, normal_vector, constant_term):
        self.dimension = 2
        self.normal_vector = normal_vector
        self.constant_term = constant_term
        self.set_basepoint()

        #if not normal_vector:
        #    all_zeros = [0]*self.dimension
        #    normal_vector = Vector(all_zeros)
        #if not constant_term:
        #    constant_term = Decimal(0)
    
    def set_basepoint(self):
        try:
            n = self.normal_vector
            c = self.constant_term
            basepoint_coords = [0]*self.dimension

            initial_index = Line.first_nonzero_index(n)
            initial_coefficient = n[initial_index]

            basepoint_coords[initial_index] = c/initial_coefficient
            self.basepoint = Vector(basepoint_coords)
        
        except Exception as e:
            if str(e) == Line.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise e
    
    def __str__(self):

        num_decimal_places = 3

        def write_coefficient(coefficient, is_initial_term=False):
            coefficient = round(coefficient, num_decimal_places)
            if coefficient % 1 == 0:
                coefficient = int(coefficient)

            output = ''

            if coefficient < 0:
                output += '-'
            if coefficient > 0 and not is_initial_term:
                output += '+'

            if not is_initial_term:
                output += ' '

            if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))

            return output

        n = self.normal_vector

        try:
            initial_index = Line.first_nonzero_index(n)
            terms = [write_coefficient(n[i], is_initial_term=(i==initial_index)) + 'x_{}'.format(i+1)
                     for i in range(self.dimension) if round(n[i], num_decimal_places) != 0]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise e

        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)

        return output


    @staticmethod
    def first_nonzero_index(iterable):
        for k, item in enumerate(iterable):
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Line.NO_NONZERO_ELTS_FOUND_MSG)

    def is_parallel(self, line):
        return (self.normal_vector.is_parallel(line.normal_vector))

    def is_coincident(self, line):    
        difference = self.basepoint.subtract(line.basepoint)
        return difference.is_orthogonal(self.normal_vector)
        
    def intersection(self, line):
        A = self.normal_vector[0]
        B = self.normal_vector[1]
        C = line.normal_vector[0]
        D = line.normal_vector[1]
        k1 = self.constant_term
        k2 = line.constant_term

        x = (D*k1 - B*k2) / (A*D - B*C)
        y = (-C*k1 + A*k2) / (A*D - B*C)
        return (x,y)

    def twoLineProperties(self, line):
        if (self.is_coincident(line) == "Orthogonal"):
            return "The two lines are coincident"
        elif (self.is_parallel(line) == "Parallel"):
            return "The two lines are parallel"
        else:
            pairs = self.intersection(line)
            return "The two lines intersect at: " + str(pairs)

class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps

def hw1():
    line1 = Line(Vector([4.046, 2.836]), 1.21)
    line2 = Line(Vector([10.115,7.09]),3.025)
    print "**********"
    print str(line1); print str(line2)
    print line1.twoLineProperties(line2)

    line3 = Line(Vector([7.204, 3.182]), 8.68)
    line4 = Line(Vector([8.172, 4.114]), 9.883)
    print "**********"
    print str(line3); print str(line4)
    print line3.twoLineProperties(line4)

    line5 = Line(Vector([1.182, 5.562]), 6.744)
    line6 = Line(Vector([1.773, 8.343]), 9.525)
    print "**********"
    print str(line4); print str(line5)
    print line5.twoLineProperties(line6)

hw1()

