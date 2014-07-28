import argparse
import sys
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='Create center script')
    parser.add_argument('-d', '--data_dir', type=str, default='.', help='png directory')
    args = parser.parse_args()
    
    files = [file_name for file_name in os.listdir(args.data_dir)
                    if file_name.endswith('.png')]
    print '#!/bin/bash'
    for fn in files:
        print 'convert %s -trim trim_%s' % (fn, fn)
        print 'convert trim_%s -resize 64x16 -background white -gravity center -extent 64x16 center_%s' % (fn, fn)
#        print 'convert center_%s -crop 1x1-0-0@ +repage crop_%%d_%s' % (fn, fn)
#        print 'convert crop_0_%s -sharpen 0x3 sharp_%s' % (fn, fn)
        print 'convert center_%s -compress none %s.pgm' % (fn, fn.split('.')[0])
