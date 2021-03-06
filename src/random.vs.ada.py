import argparse
import sys

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
            description='Random forests vs AdaBoost+DecisionTrees.')
    parser.add_argument('-j', '--jobs', type=int, default=4, help='number of pararlel jobs')
    parser.add_argument('-o', '--output_dir', type=str, default='.', help='image output directory')
    parser.add_argument('-t', '--train_ratio', type=float, default=0.5, help='training set portion')
    parser.add_argument('-e', '--estimators', type=int, default=200, help='number of estimators')
    parser.add_argument('-l', '--learning_rate', type=float, default=1.5, help='learning rate for AdaBoost')
    parser.add_argument('-m', '--max_depth', type=int, default=1, help='max depth for decision trees')
    parser.add_argument('-a', '--ada_boost_alg', type=str, 
                default='SAMME', choices=['SAMME', 'SAMME.R'], help='use SAMME.R instead od SAMME for AdaBoost')
    parser.add_argument('-b', '--boost', type=str, 
                default='R.Forests', choices=['R.Forests', 'SVC'], help='choices [R.Forests, SVC]')
    parser.add_argument('-g', '--gamma', type=float, default=0.0, help='gamma for SVC')
    parser.add_argument('-c', '--coef', type=float, default=1.0, help='c coeficient for SVC')
    parser.add_argument('-q', '--quiet', action='store_true', help='do not show graph at the end')    
    args = parser.parse_args()
    
    # Standard scientific Python imports
    import pylab as pl

    # Import datasets, classifiers and performance metrics
    from sklearn import datasets, metrics
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.ensemble import AdaBoostClassifier
    from sklearn.metrics import accuracy_score
    from sklearn.svm import SVC

    # The digits dataset
    digits = datasets.load_digits()

    # To apply an classifier on this data, we need to flatten the image, to
    # turn the data in a (samples, feature) matrix:
    n_samples = len(digits.images)
    data = digits.images.reshape((n_samples, -1))

    r_classifier = RandomForestClassifier(n_estimators=args.estimators, max_depth=args.max_depth, n_jobs=args.jobs)

    if args.boost == 'R.Forests':
        clf = DecisionTreeClassifier(max_depth=args.max_depth)
    else:
        clf = SVC(gamma=args.gamma, C=args.coef) 
        
    classifier = AdaBoostClassifier(
        clf,        
        n_estimators=args.estimators,
        learning_rate=args.learning_rate,
        algorithm=args.ada_boost_alg)

    # We learn the digits on the first half of the digits
    X_train = data[:int(n_samples * args.train_ratio)]
    y_train = digits.target[:int(n_samples * args.train_ratio)]

    X_test = data[int(n_samples * args.train_ratio):]
    y_test = digits.target[int(n_samples * args.train_ratio):]

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
    pl.plot(n_trees, test_errors, c='red', label='AdaBoost.%s' % args.boost)
    pl.plot(n_trees, test_errors_rand, c='blue', label='R.forests')
    pl.legend()
    pl.ylabel('Test Error')
    pl.xlabel('Number of Trees')
    if args.boost == 'R.Forests':
        pl.savefig('%s/random.tr.%.2f.md.%d.est.%d_ada.rf.alg.%s.lr.%.1f.png' % (
            args.output_dir,
            args.train_ratio,            
            args.max_depth,
            args.estimators,
            args.ada_boost_alg,
            args.learning_rate
        ))
    else:
        pl.savefig('%s/random.tr.%.2f.md.%d.est.%d_ada.svc.g.%.4f.c%.4f.alg.%s.lr.%.1f.png' % (
                        
            args.output_dir,
            args.train_ratio,
            args.max_depth,
            args.estimators,
            args.gamma,
            args.coef,
            args.ada_boost_alg,
            args.learning_rate
        ))
    if not args.quiet :
        pl.show()
