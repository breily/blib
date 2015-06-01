import random, math
import utility

class Matrix:
    def __init__(self, x, y, fill=0):
        self.nrows = y
        self.ncolumns = r 

        self.data = [[fill for _ in xrange(x)] for __ in xrange(y)]

    def get(self, r, c):
        return self.data[r][c]

    def __getitem__(self, r):
        return self.data[r]

    def getrow(self, n):
        return self.data[n]

    def getcol(self, n):
        return [x[n] for x in self.data]
 

def zeros(x, y): return Matrix(x. y)

####### 

# return the trace of a matrix m
def trace(m):
    if len(m) != len(m[0]):
        utility.error('not a square matrix')

    tr = sum([ m[i][i] for i in range(len(m))])
    return tr

# return the determinate of a matrix m
def det(m):
    sz = len(m)
    if sz != len(m[0]):
        utility.error('not a square matrix')
    
    # base condition
    if sz == 2:
        return (m[0][0] * m[1][1]) - (m[0][1] * m[1][0])
    
    # recursive condition (bigger than 2x2)
    # - make sure to alternate signs
    sign = '+'
    ct = 0
    # iterate over the first row only
    for i in range(sz):
        res = m[0][i] * det(__rest_of_matrix(m, i))
        if sign == '+':
            ct += res
            sign = '-'
        else:
            ct -= res
            sign = '+'

    return ct

# utility function for the determinate function
# det() goes across the first row, this function
# returns the part of the matrix that is not in the 
# first row or whatever column (c)
def __rest_of_matrix(m, c):
    ret = zerosm(len(m) - 1, len(m) - 1)
    for i in range(len(ret)):
        c_ = c
        skipped = False
        for j in range(len(ret)):
            if j == c_: 
                h = c_ + 1
                skipped = True
            else: 
                h = j
                if skipped: h += 1
            ret[i][j] = m[i + 1][h]
    return ret
 
# return the transpose of a matrix m 
def transposem(m):
    x = len(m)
    y = len(m[0])
    ret = zerosm(x, y)
    for i in range(y):
        for j in range(x):
            ret[i][j] = m[j][i]
    return ret

def transposev(v):
    ret = zerosm(1, len(v))
    for i in range(len(v)):
        ret[i][0] = v[i]
    return ret

# Dot product of two vectors
def dotv(x1, x2):
    if len(x1) != len(x2): utility.error('dimensions do not match')
    return sum([a * b for a, b in zip(x1, x2)])

# Generate a zero vector
def zerosv(n): return [0 for _ in xrange(n)]

# Generate a zero matrix
def zerosm(x, y): return [[0 for _ in xrange(x)] for __ in xrange(y)]

# Generate a ones vector
def onesv(n): return [1 for _ in xrange(n)]

# Generate a ones matrix
def onesm(x, y): return [[1 for _ in xrange(x)] for __ in xrange(y)]

# Generate a vector of random integers
def randomv(n, a=0, b=25):
    return [random.randint(a, b) for _ in xrange(n)]

# Generate a matrix of random integers
def randomm(x, y, a=0, b=25):
    return [[random.randint(a, b) for _ in xrange(x)] \
             for __ in xrange(y)]

# returns an identity matrix with dimensions x by x
def identitym(x):
    ret = zerosm(x, x)
    for i in range(x): ret[i][i] = 1
    return ret

# Compute mean for a vector
def meanv(x):
    if len(x) == 0: return 0.0
    return sum(x) / float(len(x))

# Compute mean for a matrix
def meanm(x):
    return sum([sum(r) for r in x]) / (float(len(x)) * float(len(x[0])))

# Add two matrices
def addm(a, b):
    if len(a) != len(b) or len(a[0]) != len(b[0]):
        utility.error('dimensions do not match')
    x = len(a[0])
    y = len(a)
    ret = zerosm(x, y)
    for i in range(x):
        for j in range(y):
            ret[j][i] = a[j][i] + b[j][i]
    return ret

def addv(a, b):
    if len(a) != len(b): utility.error('dimensions do not match')
    ret = zerosv(len(a))
    for i in range(len(a)):
        ret[i] = a[i] + b[i]
    return ret

def subtractms(m, s):
    ret = zerosm(len(m), len(m[0]))
    for i in range(len(m)):
        for j in range(len(m[0])):
            ret[i][j] = m[i][j] - s
    return ret

# multiply two matrices by eachother
def multiplym(a, b):
    if len(a[0]) != len(b): utility.error('dimensions do not match')
    x = len(b[0])
    y = len(a)
    ret = zerosm(x, y)
    for i in range(x):
        for j in range(y):
            for k in range(len(b)):
                ret[j][i] += a[j][k] * b[k][i]
    return ret

def multiplyvs(v, s):
    ret = zerosv(len(v))
    for i in range(len(v)):
        ret[i] = v[i] * s
    return ret

# divide a vector by a scalar
def dividevs(v, s):
    ret = zerosv(len(v))
    for i in range(len(v)):
        ret[i] = v[i] / float(s)
    return ret

# flatten a matrix into a vector
def flat(m):
    ret = []
    for row in m: ret.extend(row)
    return ret

# convert a flat vector back into a matrix
def unflat(m, x, y):
    ret = zerosm(x, y)
    ct = 0
    for i in range(y):
        for j in range(x):
            ret[i][j] = m[ct]
            ct += 1
    return ret

# returns the Euclidean norm of a matrix
def norm_euclidm(m):
    res = sum([math.pow(m[r][c], 2) for c in range(len(m[0]))
                                    for r in range(len(m))])
    return math.sqrt(res)

def norm_euclidv(v):
    res = sum([math.pow(v[i], 2) for i in range(len(v))])
    return math.sqrt(res)

def check_dimensions(a, b):
    if len(a) != len(b) or len(a[0]) != len(b[0]):
        utility.error('dimensions do not match')

# returns the cth column of m as a vector
def get_column(m, c):
    col = zerosv(len(m))
    for i in range(len(col)):
        col[i] = m[i][c]
    return col

# returns the rth row of m as a vector
def get_row(m, r):
    row = zerosv(len(m[0]))
    for i in range(len(row)):
        row[i] = m[r][i]
    return row

# returns a scalar number of rows
def len_rows(m): return len(m)
# returns an iterator over the rows
def range_rows(m): return range(len(m))

# returns a scalar number of columns
def len_cols(m): return len(m[0])
# returns an iterator over the columns
def range_cols(m): return range(len(m[0]))

def sign(s):
    if s < 0: return -1
    return 1
