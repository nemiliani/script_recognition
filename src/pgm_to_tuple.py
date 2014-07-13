import argparse
import sys
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='Random forests vs AdaBoost+DecisionTrees.')
    parser.add_argument('-d', '--data_dir', type=str, default='.', help='tuples directory')
    parser.add_argument('-o', '--output_dir', type=str, default='.', help='pickle directory')
    args = parser.parse_args()
    
    files = [file_name for file_name in os.listdir(args.data_dir)
                    if file_name.endswith('.pgm')]
    print 'found %d tuple files' % len(files)
    for fn in files:
        with open(os.path.join(args.data_dir, fn)) as f:
            f.readline()
            f.readline()
            f.readline()
            s = ''
            for line in f:
                s = '%s%s' %(s,line)
            tup = s.strip().split()
            tup.append(fn.split('.')[0].split('-')[1])
            with open(os.path.join(args.output_dir, '%s.tuple' % fn.split('.')[0]), 'w') as t:
                t.write(','.join(tup))
        
    
