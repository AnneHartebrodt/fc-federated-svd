#!/bin/bash
source mnist_config.sh
echo $pydir
echo $basedir
echo $clidir
echo $datafile
echo $outputfolder

k=10

#split the data into batches
batch=False
cross_val=False


center=True
variance=True
log=True
count=0

python $pydir/mnist_import.py -d $mnist_raw_dir -o $mnisttsvdir
python $pydir/generate_splits.py -d $outputfolder -o $dirname -F $outputfolder/data/mnist.tsv -n $sites -s $seed --transpose True --header 0 --rownames 0
python $pydir/generate_config_files.py -d $outputfolder -o $dirname -p 2 --center $center --log_transform log  --variance $variance --count $count --header 0 --rownames 0
