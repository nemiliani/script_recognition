import argparse
import sys
import pickle

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
            description='Script recognition trainer.')
    parser.add_argument('-o', '--output_dir', type=str, default='.', help='graph output directory')
    parser.add_argument('-s', '--classifier_dir', type=str, default='.', help='classifier output directory')    
    parser.add_argument('-r', '--target_file', type=str, default='target.pickle', help='pickle file with the targets')
    parser.add_argument('-d', '--data_file', type=str, default='data.pickle', help='pickle file with the data instances')
    parser.add_argument('-t', '--train_ratio', type=float, default=0.5, help='training set portion (0.0, 1.0]')
    parser.add_argument('-e', '--estimators', type=int, default=200, help='number of estimators')
    parser.add_argument('-l', '--learning_rate', type=float, default=1.5, help='learning rate for AdaBoost')
    parser.add_argument('-m', '--max_depth', type=int, default=1, help='max depth for decision trees')
    parser.add_argument('-a', '--ada_boost_alg', type=str, 
                default='SAMME', choices=['SAMME', 'SAMME.R'], help='use SAMME.R instead od SAMME for AdaBoost')
    parser.add_argument('-b', '--boost', type=str, 
                default='Trees', choices=['Trees', 'SVC'], help='choices [Trees, SVC]')
    parser.add_argument('-g', '--gamma', type=float, default=0.0, help='gamma for SVC')
    parser.add_argument('-c', '--coef', type=float, default=1.0, help='c coeficient for SVC')
    parser.add_argument('-q', '--quiet', action='store_true', help='do not show graph at the end')
    parser.add_argument('--printg', action='store_true', help='do not render graphs')    
    args = parser.parse_args()
    
    # Standard scientific Python imports
    import pylab as pl

    # Import datasets, classifiers and performance metrics
    from sklearn import datasets, metrics
    from sklearn.tree import DecisionTreeClassifier, ExtraTreeClassifier
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.ensemble import AdaBoostClassifier
    from sklearn.metrics import accuracy_score
    from sklearn.svm import SVC

    data = pickle.load(open(args.data_file,'rb'))
    target = pickle.load(open(args.target_file,'rb'))
    n_samples = len(data)

    if args.boost == 'Trees':
        clf = DecisionTreeClassifier(
                    criterion='gini',
                    splitter='best',
                    max_features='sqrt',
                    min_samples_split=2,
                    max_depth=args.max_depth)
    else:
        clf = SVC(gamma=args.gamma, C=args.coef)
    classifier = AdaBoostClassifier(
        clf,        
        n_estimators=args.estimators,
        learning_rate=args.learning_rate,
        algorithm=args.ada_boost_alg)

    # We learn the digits on the first half of the digits
    X_train = data[:int(n_samples * args.train_ratio)]
    y_train = target[:int(n_samples * args.train_ratio)]

    X_test = data[int(n_samples * args.train_ratio):]
    y_test = target[int(n_samples * args.train_ratio):]

    classifier.fit(X_train, y_train)

    # Now predict the value of the digit on the second half:
    predicted = classifier.predict(X_test)

    print("Classification report for classifier %s:\n%s\n"
          % (classifier, metrics.classification_report(y_test, predicted)))
    print("Confusion matrix:\n%s" % metrics.confusion_matrix(y_test, predicted))

    classifier_fn = '%s/ada.tr_%.2f.md_%d.e_%d.lr_%.2f.pickle' % (       
            args.classifier_dir,
            args.train_ratio,
            args.max_depth,
            args.estimators,
            args.learning_rate)
    pickle.dump(classifier, open(classifier_fn, 'wb'))

    if not args.printg:
        sys.exit(0)

    n_trees = xrange(1, len(classifier) + 1)
    test_errors = []
    train_errors = []
    for p in classifier.staged_predict(X_test):
        test_errors.append(1. - accuracy_score(p, y_test))
    for p in classifier.staged_predict(X_train):
        train_errors.append(1. - accuracy_score(p, y_train))

    pl.subplot(1,1,1)
    pl.plot(n_trees, test_errors, c='red', label='AdaBoost.%s' % args.boost)
    pl.legend()
    pl.ylabel('Test Error')
    pl.xlabel('Number of Trees')
    if args.boost == 'Trees':
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
