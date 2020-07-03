import math
from math import sqrt
import numbers

def zeroes(height, width):
    """
    Creates a matrix of zeroes.
    """
    g = [[0.0 for _ in range(width)] for __ in range(height)]
    return Matrix(g)

def dot(v1, v2):
    if len(v1) != len(v2):
        return None

    s = 0
    for i in range(len(v1)):
        s += v1[i] * v2[i]

    return s

def identity(n):
    """
    Creates a n x n identity matrix.
    """
    I = zeroes(n, n)
    for i in range(n):
        I.g[i][i] = 1.0
    return I

class Matrix(object):

    # Constructor
    def __init__(self, grid):
        self.g = grid
        self.rows = len(grid)
        self.cols = len(grid[0])

    #
    # Primary matrix math methods
    #############################

    def determinant(self):
        """
        Calculates the determinant of a 1x1 or 2x2 matrix.
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate determinant of non-square matrix.")
        if self.rows > 2:
            raise(NotImplementedError, "Calculating determinant not implemented for matrices largerer than 2x2.")

        n = self.rows

        if n == 1:
            return self.g[0][0]
        elif n == 2:
            a = self.g[0][0]
            b = self.g[0][1]
            c = self.g[1][0]
            d = self.g[1][1]

            detA = (a * d) - (b * c)

            return detA

    def trace(self):
        """
        Calculates the trace of a matrix (sum of diagonal entries).
        """
        if not self.is_square():
            raise(RuntimeError, "Cannot calculate the trace of a non-square matrix.")

        s = 0
        for i in range(self.rows):
            for j in range(self.cols):
                if i == j:
                    s += self.g[i][j]

        return s

    def inverse(self):
        """
        Calculates the inverse of a 1x1 or 2x2 Matrix.
        """
        if not self.is_square():
            raise(RuntimeError, "Non-square Matrix does not have an inverse.")
        if self.rows > 2:
            raise(NotImplementedError, "inversion not implemented for matrices larger than 2x2.")

        n = self.rows

        if n == 1:
            return Matrix([[1/self.g[0][0]]])
        elif n == 2:
            a = self.g[0][0]
            b = self.g[0][1]
            c = self.g[1][0]
            d = self.g[1][1]

            detA = self.determinant()

            if detA == 0:
                raise(ValueError, "The determinant is zero!")

            m = [[d, -b], [-c, a]]

            for i in range(2):
                for j in range(2):
                    m[i][j] = m[i][j] * (1/detA)

            return Matrix(m)

    def T(self):
        """
        Returns a transposed copy of this Matrix.
        """
        n_rows = self.cols
        n_cols = self.rows

        inv = []
        for i in range(n_rows):
            row = []
            for j in range(n_cols):
                row.append(self.g[j][i])
            inv.append(row)

        return Matrix(inv)

    def is_square(self):
        return self.rows == self.cols

    #
    # Begin Operator Overloading
    ############################
    def __getitem__(self,idx):
        """
        Defines the behavior of using square brackets [] on instances
        of this class.

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > my_matrix[0]
          [1, 2]

        > my_matrix[0][0]
          1
        """
        return self.g[idx]

    def __repr__(self):
        """
        Defines the behavior of calling print on an instance of this class.
        """
        s = ""
        for row in self.g:
            s += " ".join(["{} ".format(x) for x in row])
            s += "\n"
        return s

    def __add__(self,other):
        """
        Defines the behavior of the + operator
        """
        if isinstance(other, Matrix):
            if self.rows != other.rows or self.cols != other.cols:
                raise(RuntimeError, "Matrices can only be added if the dimensions are the same")

            result = []

            for i in range(self.rows):
                row = []
                for j in range(self.cols):
                    row.append(self.g[i][j] + other.g[i][j])
                result.append(row)

            return Matrix(result)

    def __neg__(self):
        """
        Defines the behavior of - operator (NOT subtraction)

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > negative  = -my_matrix
        > print(negative)
          -1.0  -2.0
          -3.0  -4.0
        """
        result = []

        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(-self.g[i][j])
            result.append(row)

        return Matrix(result)

    def __sub__(self, other):
        """
        Defines the behavior of - operator (as subtraction)
        """
        if isinstance(other, Matrix):
            if self.rows != other.rows or self.cols != other.cols:
                raise(RuntimeError, "Matrices can only be added if the dimensions are the same")

            result = []

            for i in range(self.rows):
                row = []
                for j in range(self.cols):
                    row.append(self.g[i][j] - other.g[i][j])
                result.append(row)

            return Matrix(result)

    def __mul__(self, other):
        """
        Defines the behavior of * operator (matrix multiplication)
        """
        if isinstance(other, Matrix) and self.cols == other.rows:
            result = []
            tMatrixB = other.T()

            for i in range(self.rows):
                row = self.g[i]
                new_row = []
                for j in range(tMatrixB.rows):
                    col = tMatrixB[j]
                    s = dot(row, col)
                    new_row.append(s)
                result.append(new_row)

            return Matrix(result)
        else:
            return self.__rmul__(other)


    def __rmul__(self, other):
        """
        Called when the thing on the left of the * is not a matrix.

        Example:

        > identity = Matrix([ [1,0], [0,1] ])
        > doubled  = 2 * identity
        > print(doubled)
          2.0  0.0
          0.0  2.0
        """
        result = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(self.g[i][j] * other)
            result.append(row)

        return Matrix(result)
