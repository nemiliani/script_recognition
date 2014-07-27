import argparse
import pickle

if __name__ == '__main__' :
    parser = argparse.ArgumentParser(
            description='Script recognition predictor.')
    parser.add_argument('-d', '--data_file', type=str, default='.', help='pickled data file')
    parser.add_argument('-n', '--name_file', type=str, default='.', help='pickled names file')
    parser.add_argument('-c', '--classifier', type=str, default='.', help='pickled classifier')
    args = parser.parse_args()
    
    clf = pickle.load(open(args.classifier, 'rb'))
    data = pickle.load(open(args.data_file, 'rb'))
    names = pickle.load(open(args.name_file, 'rb'))
    
    target = clf.predict(data)
    for i in range(len(target)):
        print '%s,%s' % (names[i], target[i])
    
