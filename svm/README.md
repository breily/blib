
svm.py
======

* Implements a Support Vector Machine in Python.
* No speed tests done but probably not particularly fast (use scikit-learn if you
  need a fast version).
* Uses the Sequential Minimal Optimization (SMO) algorithm to set the alpha values.

Usage
-----

A very basic example with the defaults of a polynomial kernel function of degree 2,
and C = 100:
    
    import svm

    c = svm.SVM()

    X = [ [1], [2], [4], [5], [6] ]
    Y = [   1,   1,  -1,  -1,   1 ]

    c.train(X, Y)
    z = c.predict([3])

In this case 'z' should be the class -1. 
The support vectors are [2], [5], and [6], with respective alpha values of 2.5, 7.3, and
4.8.  Bias will be equal to 9.

