import svm

X = [ [1], [2], [4], [5], [6] ]
Y = [   1,   1,  -1,  -1,   1 ]

c = svm.SVM()
c.train(X, Y)

z = c.predict([3])

print '-> classifying [3]...'
print '-> predicted class: %s' % z
print '-> actual class: -1'
