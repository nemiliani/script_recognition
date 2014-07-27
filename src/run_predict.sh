#!/bin/bash
cd predict_data
echo 'unzip data'
rm -rf __MACOSX
rm -rf train-tuples
unzip TP2-predict-tuples.zip
rm -f train-tuples/*.pgm
rm -f train-tuples/*.tuple
cd ..
python transform.py -d predict_data/train-tuples/ > predict_data/train-tuples/center.sh
chmod a+x predict_data/train-tuples/center.sh
cd predict_data/train-tuples
echo 'center all images ...'
./center.sh
cd ../../
echo 'create tuples form centered images'
python pgm_to_tuple.py -d predict_data/train-tuples/ -o predict_data/train-tuples
python load.py -d predict_data/train-tuples/ -o predict_data/ --no_target
python predict.py -d predict_data/data_center.pickle -n predict_data/names.pickle -c classifiers/ada.tr_0.70.md_6.e_500.lr_0.70.pickle > predictions.txt
