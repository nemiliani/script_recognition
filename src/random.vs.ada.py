import argparse
import sys

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
            description='Random forests vs AdaBoost+DecisionTrees.')
    parser.add_argument('-j', '--jobs', type=int, default=4, help='number of pararlel jobs')
    parser.add_argument('-o', '--output_dir', type=str, default='.', help='image output directory')
    parser.add_argument('-e', '--estimators', type=int, default=200, help='number of estimators')
    parser.add_argument('-l', '--learning_rate', type=float, default=1.5, help='learning rate for AdaBoost')
    parser.add_argument('-m', '--max_depth', type=int, default=1, help='max depth for decision trees')
    parser.add_argument('-a', '--ada_boost_alg', type=str, 
                default='SAMME', choices=['SAMME', 'SAMME.R'], help='use SAMME.R instead od SAMME for AdaBoost')    
    parser.add_argument('-q', '--quiet', action='store_true', help='do not show graph at the end')    
    args = parser.parse_args()
    print 'jobs = %d' % args.jobs
    print 'output = %s' % args.output_dir
    print 'estimators = %d' % args.estimators
    print 'learning rate = %.1f' % args.learning_rate
    print 'max depth = %d' % args.max_depth
    print 'ada boost algorithm = %s' % args.ada_boost_alg

    # Standard scientific Python imports
    import pylab as pl

    # Import datasets, classifiers and performance metrics
    from sklearn import datasets, metrics
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.ensemble import AdaBoostClassifier
    from sklearn.metrics import accuracy_score

    # The digits dataset
    digits = datasets.load_digits()

    # To apply an classifier on this data, we need to flatten the image, to
    # turn the data in a (samples, feature) matrix:
    n_samples = len(digits.images)
    data = digits.images.reshape((n_samples, -1))

    # Create a classifier: a support vector classifier
    r_classifier = RandomForestClassifier(n_estimators=args.estimators, max_depth=args.max_depth)
    classifier = AdaBoostClassifier(
        DecisionTreeClassifier(max_depth=args.max_depth),
        n_estimators=args.estimators,
        learning_rate=args.learning_rate,
        algorithm=args.ada_boost_alg)

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

    test_errors_rand = []
    for i in xrange(1, args.estimators + 1):
        print '.',
        r_classifier = RandomForestClassifier(n_estimators=i, n_jobs=args.jobs, max_depth=args.max_depth)
        r_classifier.fit(X_train, y_train)
        r_predicted = r_classifier.predict(X_test)
        test_errors_rand.append(1. - accuracy_score(r_predicted, y_test))
    print '.'

    pl.subplot(1,1,1)
    pl.plot(n_trees, test_errors, c='red', label='AdaBoost')
    pl.plot(n_trees, test_errors_rand, c='blue', label='R.forests')
    pl.legend()
    pl.ylabel('Test Error')
    pl.xlabel('Number of Trees')
    pl.savefig('%s/random.md.%d.est.%d_ada.alg.%s.lr.%.1f.png' % (
        args.output_dir,
        args.max_depth,
        args.estimators,
        args.ada_boost_alg,
        args.learning_rate
    ))
    if not args.quiet :
        pl.show()
