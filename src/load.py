import argparse
import sys
import os
import pickle

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='Create pickles with data')
    parser.add_argument('-d', '--data_dir', type=str, default='.', help='tuples directory')
    parser.add_argument('-o', '--output_dir', type=str, default='.', help='pickle directory')
    parser.add_argument('--no_target', action='store_true', help='do not pickle targets')
    parser.add_argument('--no_names', action='store_true', help='do not pickle targets')    
    args = parser.parse_args()
    
    files = [file_name for file_name in os.listdir(args.data_dir)
                    if file_name.endswith('.tuple')]
    print 'found %d tuple files' % len(files)
    data = []
    target = []
    names = []
    for fn in files:
        with open(os.path.join(args.data_dir, fn)) as f:
            tup = f.readline().split(',')
        if not args.no_names:
            names.append(fn)
        if not args.no_target:
            target.append(tup[-1])
        data.append([255 - int(value) for value in tup[:-1]])        
        print '.',
    print '.'
    pickle.dump(data, open(os.path.join(args.output_dir, 'data_center.pickle'), 'wb'))
    if not args.no_target:    
        pickle.dump(target, open(os.path.join(args.output_dir, 'target_center.pickle'), 'wb'))
    if not args.no_names:    
        pickle.dump(names, open(os.path.join(args.output_dir, 'names.pickle'), 'wb'))
