from decimal import Decimal, getcontext
from copy import deepcopy

from vector import Vector
from plane import Plane

getcontext().prec = 30


class LinearSystem(object):

    ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG = 'All planes in the system should live in the same dimension'
    NO_SOLUTIONS_MSG = 'No solutions'
    INF_SOLUTIONS_MSG = 'Infinitely many solutions'

    def __init__(self, planes):
        try:
            d = planes[0].dimension
            for p in planes:
                assert p.dimension == d

            self.planes = planes
            self.dimension = d

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)


    def swap_rows(self, row1, row2):
        """
        temp = self[row1]
        self[row1] = self[row2]
        self[row2] = temp
        """
        self[row1], self[row2] = self[row2], self[row1]


    def multiply_coefficient_and_row(self, coefficient, row):
        #self[row] = Plane(self[row].normal_vector.scalar(coefficient), self[row].constant_term * coefficient)

        v = self[row].normal_vector
        k = self[row].constant_term

        new_v = v.scalar(coefficient)
        new_k = k * coefficient

        self[row] = Plane(Vector(new_v), new_k)

    def add_multiple_times_row_to_row(self, coefficient, row_to_add, row_to_be_added_to):
        #Define variable for the vector and constant term
        v = self[row_to_add].normal_vector
        k = self[row_to_add].constant_term

        #Perform multiplication / scaler operations (coefficient * row)
        v_multi = v.scalar(coefficient)
        k_multi = k * coefficient

        #Add new vector to existing vector
        v_new = v_multi.add(self[row_to_be_added_to].normal_vector)
        k_new = k_multi + self[row_to_be_added_to].constant_term

        self[row_to_be_added_to] = Plane(Vector(v_new), k_new)      


    def indices_of_first_nonzero_terms_in_each_row(self):
        num_equations = len(self)
        num_variables = self.dimension

        indices = [-1] * num_equations

        for i,p in enumerate(self.planes):
            try:
                indices[i] = p.first_nonzero_index(p.normal_vector)
            except Exception as e:
                if str(e) == Plane.NO_NONZERO_ELTS_FOUND_MSG:
                    continue
                else:
                    raise e

        return indices


    def __len__(self):
        return len(self.planes)


    def __getitem__(self, i):
        return self.planes[i]


    def __setitem__(self, i, x):
        try:
            assert x.dimension == self.dimension
            self.planes[i] = x

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)


    def __str__(self):
        ret = 'Linear System:\n'
        temp = ['Equation {}: {}'.format(i+1,p) for i,p in enumerate(self.planes)]
        ret += '\n'.join(temp)
        return ret


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps



def rowOpsTest(s, p0, p1, p2, p3):
    s.swap_rows(0,1)
    if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
        print 'test case 1 failed'

    s.swap_rows(1,3)
    if not (s[0] == p1 and s[1] == p3 and s[2] == p2 and s[3] == p0):
        print 'test case 2 failed'

    s.swap_rows(3,1)
    if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
        print 'test case 3 failed'

    s.multiply_coefficient_and_row(1,1)
    if not (s[0] == (p1) and s[1] == p0 and s[2] == p2 and s[3] == p3):
        print s[0]
        print p1
        print 'test case 4 failed'

    s.multiply_coefficient_and_row(-1,2)
    if not (s[0] == p1 and
            s[1] == p0 and
            s[2] == Plane(normal_vector=Vector([-1,-1,1]), constant_term=-3) and
            s[3] == p3):
        print 'test case 5 failed'
    
    s.multiply_coefficient_and_row(10,1)
    if not (s[0] == p1 and
            s[1] == Plane(normal_vector=Vector([10,10,10]), constant_term=10) and
            s[2] == Plane(normal_vector=Vector([-1,-1,1]), constant_term=-3) and
            s[3] == p3):
        print 'test case 6 failed'

    s.add_multiple_times_row_to_row(0,0,1)
    if not (s[0] == p1 and
            s[1] == Plane(normal_vector=Vector([10,10,10]), constant_term=10) and
            s[2] == Plane(normal_vector=Vector([-1,-1,1]), constant_term=-3) and
            s[3] == p3):
        print 'test case 7 failed'

    s.add_multiple_times_row_to_row(1,0,1)
    if not (s[0] == p1 and
            s[1] == Plane(normal_vector=Vector([10,11,10]), constant_term=12) and
            s[2] == Plane(normal_vector=Vector([-1,-1,1]), constant_term=-3) and
            s[3] == p3):
        print 'test case 8 failed'

    s.add_multiple_times_row_to_row(-1,1,0)
    if not (s[0] == Plane(normal_vector=Vector([-10,-10,-10]), constant_term=-10) and
            s[1] == Plane(normal_vector=Vector([10,11,10]), constant_term=12) and
            s[2] == Plane(normal_vector=Vector([-1,-1,1]), constant_term=-3) and
            s[3] == p3):
        print 'test case 9 failed'

p0 = Plane(normal_vector=Vector([1,1,1]), constant_term=1)
p1 = Plane(normal_vector=Vector([0,1,0]), constant_term=2)
p2 = Plane(normal_vector=Vector([1,1,-1]), constant_term=3)
p3 = Plane(normal_vector=Vector([1,0,-2]), constant_term=2)

s = LinearSystem([p0,p1,p2,p3])

#print s.indices_of_first_nonzero_terms_in_each_row()
#print '{},{},{},{}'.format(s[0],s[1],s[2],s[3])
print s

print "******\nROW OPERATIONS"
rowOpsTest(s, p0, p1, p2 ,p3)
print s