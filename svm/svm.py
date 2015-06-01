# SMO (sequential minimal optimization) algorithm from:
# http://research.microsoft.com/en-us/um/people/jplatt/smoTR.pdf
# http://cs229.stanford.edu/notes/cs229-notes3.pdf

import math, random
import matrix

random.seed(0)

class SVM:
    def __init__(self, kernel='poly',
        degree=2, sigma=0.5, sigmoid_k=1, sigmoid_theta=2,
        C=100, tol=0.001, eps=0.00001,
        maxiter=2000,
    ):
        self._kernel_choices = {'linear':  self._kernel_linear,
                                'poly':    self._kernel_poly,
                                'rbf':     self._kernel_rbf,
                                'sigmoid': self._kernel_sigmoid,
                               }

        self.kernel = self._kernel_choices[kernel]

        self.degree = degree                    # used for polynomial kernel
        self.sigma = sigma                      # used for gaussian kernel
        self.sigmoid_k = sigmoid_k              # used for sigmoid kernel
        self.sigmoid_theta = sigmoid_theta      # used for sigmoid kernel

        # TODO: option to disregard C in order to have a hard margin SVM?
        self.C = C
        self.b = 0.0
        self.tol = tol
        self.eps = eps
        self.maxiter = maxiter

        self.X = []
        self.Y = []

        self._support_alphas = []
        self._support_vectors = []
        self._support_labels  = []

    # X -> vector of input vectors
    # Y -> vector of input labels
    # output -> self
    def train(self, X, Y):
        self.X = X
        self.Y = Y
        self.N = len(X)          # number of data points
        self.D = len(X[0])       # number of dimensions

        # lagrangian multipliers all start at zero
        self.A = matrix.zerosv(self.N)
        # makes self.K, a cache of kernel function results
        self.form_kernel_matrix()

        self.smo()
        self.form_support_vectors()
        self.bias()

    # smo(), examine(i), and step(i, j) are directly from Platt's paper
    def smo(self):
        delta = False
        check_all = True
        passes = 0

        while (delta or check_all and passes < self.maxiter):
            delta = False
            if check_all:
                # check all alphas / input vectors
                for i in range(self.N):
                    delta = self.examine(i) or delta
                check_all = False
            else:
                # only check instances where alpha is not 0, not C
                for i, a in enumerate(self.A):
                    if a not in (0, self.C): 
                        delta = self.examine(i) or delta

            # if nothing changed, recheck everything
            if not delta: check_all = True
            passes += 1

    def examine(self, i):
        yi = self.Y[i]
        ai = self.A[i]
        Ei = self.margin(i) - yi
        ri = Ei * yi
        # check KKT conditions?
        if ((ri < -self.tol and ai < self.C) or (ri > self.tol and ai > 0)):
            # check if there's more than one alpha not equal to 0 or C
            if sum([1 if a not in (0, self.C) else 0 for a in self.A]) > 1:
                # find another instance to optimize against
                j = i
                while j == 1: j = random.randint(0, self.N - 1)
                if self.step(i, j): return True
            
            # optimize against other alphas in random order
            # TODO: should be 'starting at a random point'
            shuffled = range(self.N)
            random.shuffle(shuffled)
            for j in shuffled:
                if ai not in (0, self.C):
                    if self.step(i, j): return True

            # optimize against all other alphas
            for j in range(self.N):
                if self.step(i, j): return True

        return False

    def step(self, i, j):
        if i == j: return False

        ai = self.A[i]
        aj = self.A[j]
        yi = self.Y[i]
        yj = self.Y[j]
        Ei = self.margin(i) - yi
        Ej = self.margin(j) - yj
        s = yi * yj

        # platt Eq. 13
        if yi != yj:
            L = max(0, aj - ai)
            H = min(self.C, self.C + aj - ai)
        # platt Eq. 14
        else:
            L = max(0, aj + ai - self.C)
            H = min(self.C, aj + ai)
        if L == H: return False

        eta = self.K[i][i] + self.K[j][j] - 2 * self.K[i][j]
        if eta > 0:
            aj_ = aj + (yj * (Ei - Ej)) / eta
            if aj_ < L: aj_ = L
            elif aj_ > H: aj_ = H
        else:
            print '********* eta <= 0 **********'
            return False
            #f1 = (yi * (Ei + s.b)) - (ai * s.K[i][i]) - (s * aj * s.K[i][j])
            #f2 = (yj * (Ej + s.b)) - (s * ai * s.K[i][j]) - (aj * s.K[j][j])
            #L1 = ai + s * (aj - L)
            #H1 = ai + s * (aj - H)
            #psiL = (L1 * f1) + (L * f2) + (0.5 * (L1 ** 2) * s.K[i][i]) + \
            #       (0.5 * (L ** 2) * s.K[j][j]) + (s * L * L1 * s.K[i][j])
            #psiH = (H1 * f1) + (H * f2) + (0.5 * (H1 ** 2) * s.K[i][i]) + \
            #       (0.5 * (H ** 2) * s.K[j][j]) + (s * H * H1 * s.K[i][j])
            # finish else block...
        
        if aj_ < self.eps: aj_ = 0
        if (self.C - aj_) < self.eps: aj_ = self.C

        if abs(aj_ - aj) < (self.eps * (aj_ + aj + self.eps)):
            return False

        ai_ = ai + s * (aj - aj_)

        if ai_ < self.eps: ai_ = 0
        if (self.C - ai_) < self.eps: ai_ = self.C

        self.A[i] = ai_
        self.A[j] = aj_

        # platt Eq. 20, 21
        b1 = Ei + yi * (ai_ - ai) * self.K[i][i] + \
                  yj * (aj_ - aj) * self.K[i][j] + self.b

        b2 = Ej + yi * (ai_ - ai) * self.K[i][j] + \
                  yj * (aj_ - aj) * self.K[j][j] + self.b

        # TODO: updating bias gives incorrect results for weights?
        #self.b = (b1 + b2) / 2

        return True

    def form_support_vectors(self):
        for i, a in enumerate(self.A):
            if a == 0: continue
            self._support_alphas.append(a)
            self._support_vectors.append(self.X[i])
            self._support_labels.append(self.Y[i])
                
    def form_kernel_matrix(self):
        self.K = [[0 for _ in range(self.N)] for __ in range(self.N)]
        for i, x_i in enumerate(self.X):
            for j, x_j in enumerate(self.X):
                self.K[i][j] = self.kernel(x_i, x_j)

    def bias(self):
        self.b = round(matrix.meanv([y - self.predict(x) for y, x in \
                       zip(self._support_labels, self._support_vectors)]))

    def margin(self, i):
        return self.b + sum([self.A[j] * self.Y[j] * self.K[i][j] \
                             for j in range(self.N)])

    # z -> input vector to classify
    # output -> predicted label for z
    ## ! Currently correct given test.data()
    def predict(self, z):
        if type(z) != list: z = [z]
        result = self.b
        for a, x, y in zip(self._support_alphas, 
                           self._support_vectors,
                           self._support_labels):
            result += a * y * self.kernel(x, z)
        #return result
        if result < 0: return -1
        else: return 1

    # kernel function -> dot product of two vectors
    def _kernel_linear(self, x_i, x_j):
        return matrix.dotv(x_i, x_j)       

    # kernel function -> dot product of two vectors raised to nth degree
    def _kernel_poly(self, x_i, x_j):
        return (matrix.dotv(x_i, x_j) + 1) ** self.degree

    # kernel function -> rbf/gaussian based kernel
    def _kernel_rbf(self, x_i, x_j):
        # exp(-||x_i - x_j||2 / 2 * (sigma ** 2))
        # how to do norm?
        pass

    # kernel function -> sigmoid based kernel
    def _kernel_sigmoid(self, x_i, x_j):
        return math.tanh(self.sigmoid_k * matrix.dotv(x_i, x_j) + self.sigmoid_theta)
