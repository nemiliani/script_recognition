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

# Create a classifier: a support vector classifier
r_classifier = RandomForestClassifier(n_estimators=200, max_depth=1)
classifier = AdaBoostClassifier(
    DecisionTreeClassifier(max_depth=1),
    n_estimators=200,
    learning_rate=1.5,
    algorithm="SAMME")

# We learn the digits on the first half of the digits
X_train = data[:n_samples / 2]
y_train = digits.target[:n_samples / 2]

X_test = data[n_samples / 2:]
y_test = digits.target[n_samples / 2:]

classifier.fit(X_train, y_train)
r_classifier.fit(X_train, y_train)

# Now predict the value of the digit on the second half:
predicted = classifier.predict(X_test)
r_predicted = r_classifier.predict(X_test)

print("Classification report for classifier %s:\n%s\n"
      % (classifier, metrics.classification_report(y_test, predicted)))
print("Confusion matrix:\n%s" % metrics.confusion_matrix(y_test, predicted))

print("Classification report for classifier %s:\n%s\n"
      % (r_classifier, metrics.classification_report(y_test, r_predicted)))
print("Confusion matrix:\n%s" % metrics.confusion_matrix(y_test, r_predicted))

n_trees = xrange(1, len(classifier) + 1)
test_errors = []
train_errors = []
for p in classifier.staged_predict(X_test):
    test_errors.append(1. - accuracy_score(p, y_test))
for p in classifier.staged_predict(X_train):
    train_errors.append(1. - accuracy_score(p, y_train))

#test_errors_rand = []
#for i in range(1, 200 +1):
#    print 'fitting with %d estimators' % i
#    r_classifier = RandomForestClassifier(n_estimators=i, n_jobs=4, max_depth=10)
#    r_classifier.fit(X_train, y_train)
#    r_predicted = r_classifier.predict(X_test)
#    test_errors_rand.append(1. - accuracy_score(r_predicted, y_test))

pl.subplot(1,1,1)
pl.plot(n_trees, test_errors, c='red', label='SAMME.test')
pl.plot(n_trees, train_errors, c='green', label='SAMME.train')
#pl.plot(n_trees, test_errors_rand, c='blue', label='R.forests')
pl.legend()
pl.ylabel('Test Error')
pl.xlabel('Number of Trees')
pl.savefig('random.ada.200.md10.train.test.png')
