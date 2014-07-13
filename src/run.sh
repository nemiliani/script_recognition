#!/bin/bash
echo 'create directories'
mkdir classifiers
mkdir graphs
cd data
echo 'unzip data'
unzip TP2-train-tuples.zip
rm train-tuples/*.pgm
rm train-tuples/*.tuple
cd ..
python transform.py -d data/train-tuples/ > data/train-tuples/center.sh
chmod a+x data/train-tuples/center.sh
cd data/train-tuples
echo 'center all images ...'
./center.sh
cd ../../
echo 'create tuples form centered images'
python pgm_to_tuple.py -d data/train-tuples/ -o data/train-tuples
python load.py -d data/train-tuples/ -o data/
echo 'Training ... this might take a while'
python train.py -o graphs/ -s classifiers/ -r data/target_center.pickle -d data/data_center.pickle -t 0.7 -e 500 -l 0.7 -m 6
