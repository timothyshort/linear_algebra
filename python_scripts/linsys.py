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

    def compute_triangular_form(self):
        system = deepcopy(self)

        #Column by column (variable by variable)
            
        #Row (reduce row)
        for row in range(len(system)-1):
            print system; print ""

            #Make sure we find our pivot row by having a leading non-zero coefficient
            if system[row].normal_vector[row] == 0:
                print "LEADING TERM = 0 | SWAP WITH FIRST NON-ZERO COEFFICIENT"
                #Find the first leading non-zero term
                for rowLeadingNonZero in range(row+1,len(system)-1):
                    if system[rowLeadingNonZero] != 0 :
                        #Swap leading non-zero row with current row
                        system.swap_rows(row,rowLeadingNonZero)

            #Define Pivot Row and leading coefficient
            pivotRow = system[row]
            leadingCoefficient = pivotRow.normal_vector[row]

            print "FOUND PIVOT ROW | " + str(row)
            #Multiple all following rows by alpha
            
            for rowToBeMultipled in range(row+1,len(system)):
                #Alpha = leading coefficient of row to be swapped / leading coefficient of pivot
                alpha = float(-(system[rowToBeMultipled].normal_vector[row]/leadingCoefficient))
                print "ALPHA = " + str(alpha)
                system.add_multiple_times_row_to_row(alpha,row,rowToBeMultipled)
            
            print ""; print system
            print "*******\nIteration"
        return system        


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


def triangularFormTest():
    print "******\nTRIANGULAR FORM OPERATIONS"
    
    p1 = Plane(normal_vector=Vector([1,1,1]), constant_term=1)
    p2 = Plane(normal_vector=Vector([0,1,1]), constant_term=2)
    s = LinearSystem([p1,p2])
    t = s.compute_triangular_form()
    if not (t[0] == p1 and t[1] == p2):
        print 'test case 1 failed'

    p1 = Plane(normal_vector=Vector([1,1,1]), constant_term=1)
    p2 = Plane(normal_vector=Vector([1,1,1]), constant_term=2)
    s = LinearSystem([p1,p2])
    print s
    t = s.compute_triangular_form()
    if not (t[0] == p1 and
            t[1] == Plane(constant_term=1)):
        print 'test case 2 failed'
    
    p1 = Plane(normal_vector=Vector([1,1,1]), constant_term=1)
    p2 = Plane(normal_vector=Vector([0,1,0]), constant_term=2)
    p3 = Plane(normal_vector=Vector([1,1,-1]), constant_term=3)
    p4 = Plane(normal_vector=Vector([1,0,-2]), constant_term=2)
    s = LinearSystem([p1,p2,p3,p4])
    t = s.compute_triangular_form()
    if not (t[0] == p1 and
            t[1] == p2 and
            t[2] == Plane(normal_vector=Vector([0,0,-2]), constant_term=2) and
            t[3] == Plane()):
        print 'test case 3 failed'
    
    p1 = Plane(normal_vector=Vector([0,1,1]), constant_term=1)
    p2 = Plane(normal_vector=Vector([1,-1,1]), constant_term=2)
    p3 = Plane(normal_vector=Vector([1,2,-5]), constant_term=3)
    s = LinearSystem([p1,p2,p3])
    t = s.compute_triangular_form()
    if not (t[0] == Plane(normal_vector=Vector([1,-1,1]), constant_term=2) and
            t[1] == Plane(normal_vector=Vector([0,1,1]), constant_term=1) and
            t[2] == Plane(normal_vector=Vector([0,0,-9]), constant_term=-2)):
        print 'test case 4 failed'

def rowOpsTest():
    print "******\nROW OPERATIONS"

    p0 = Plane(normal_vector=Vector([1,1,1]), constant_term=1)
    p1 = Plane(normal_vector=Vector([0,1,0]), constant_term=2)
    p2 = Plane(normal_vector=Vector([1,1,-1]), constant_term=3)
    p3 = Plane(normal_vector=Vector([1,0,-2]), constant_term=2)
    s = LinearSystem([p0,p1,p2,p3])

    #print s.indices_of_first_nonzero_terms_in_each_row()
    #print '{},{},{},{}'.format(s[0],s[1],s[2],s[3])
    print s

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

    print s


#rowOpsTest()
triangularFormTest()