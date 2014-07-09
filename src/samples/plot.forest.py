# Standard scientific Python imports
import pylab as pl

# Import datasets, classifiers and performance metrics
from sklearn import datasets, metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# The digits dataset
digits = datasets.load_digits()

# To apply an classifier on this data, we need to flatten the image, to
# turn the data in a (samples, feature) matrix:
n_samples = len(digits.images)
data = digits.images.reshape((n_samples, -1))

# We learn the digits on the first half of the digits
X_train = data[:n_samples / 2]
y_train = digits.target[:n_samples / 2]

X_test = data[n_samples / 2:]
y_test = digits.target[n_samples / 2:]

test_errors = []
#for i in range(1, 600 +1):
#    print 'fitting with %d estimators' % i
#    r_classifier = RandomForestClassifier(n_estimators=i, n_jobs=4)
#    r_classifier.fit(X_train, y_train)
#    r_predicted = r_classifier.predict(X_test)
#    test_errors.append(1. - accuracy_score(r_predicted, y_test))

r_classifier = RandomForestClassifier(n_estimators=600, n_jobs=4)
r_classifier.fit(X_train, y_train)
for e in r_classifier.estimators_:    
    r_predicted = e.predict(X_test)
    test_errors.append(1. - accuracy_score(r_predicted, y_test))

n_trees = xrange(1, 600 + 1)
    
pl.subplot(1,1,1)
pl.plot(n_trees, test_errors, c='red', label='R.Forest')
pl.legend()
pl.ylabel('Test Error')
pl.xlabel('Number of Trees')
pl.show()
