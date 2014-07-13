import argparse
import sys
import os
import pickle

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='Random forests vs AdaBoost+DecisionTrees.')
    parser.add_argument('-d', '--data_dir', type=str, default='.', help='tuples directory')
    parser.add_argument('-o', '--output_dir', type=str, default='.', help='pickle directory')
    args = parser.parse_args()
    
    files = [file_name for file_name in os.listdir(args.data_dir)
                    if file_name.endswith('.tuple')]
    print 'found %d tuple files' % len(files)
    data = []
    target = []
    for fn in files:
        with open(os.path.join(args.data_dir, fn)) as f:
            tup = f.readline().split(',')
        target.append(tup[-1])
        data.append([255 - int(value) for value in tup[:-1]])        
        print '.',
    print '.'
    pickle.dump(data, open(os.path.join(args.output_dir, 'data_center.pickle'), 'wb'))
    pickle.dump(target, open(os.path.join(args.output_dir, 'target_center.pickle'), 'wb'))
    
