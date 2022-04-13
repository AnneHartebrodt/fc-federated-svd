#!/bin/bash
source random_config.sh
echo $basedir
echo $clidir
echo $pydir
echo $outputfolder
mkdir -p $outputfolder


center=True
variance=True
log=True

# generate the data
python $pydir/generate_test_data.py -d $outputfolder -f $datafile -n $samples -m $features -s $seed -b 1 --rownames 1 --colnames 1 --positive True --na 0.5

# split the data
python $pydir/generate_splits.py -d $outputfolder -o $dirname -f $datafile -n $sites -s $seed  --header 0 --transpose True --rownames 0

# generate the config files
python $pydir/generate_config_files.py -d $outputfolder -o $dirname  -p 2 --rownames 0 --header 0 --count 0 \
  --center $center --log_transform log  --variance $variance #--phv $phv -
#
python $pydir/generate_config_files.py -d $outputfolder -o $dirname  -p 2  --rownames 0 --header 0 --count 1 \
  --center $center --variance $variance #--log_transform log #--phv $phv -

python $pydir/generate_config_files.py -d $outputfolder -o $dirname  -p 2  --rownames 0 --header 0 --count 2 \
  --center $center --log_transform log  #--log_transform log #--phv $phv -

python $pydir/generate_config_files.py -d $outputfolder -o $dirname  -p 2  --rownames 0 --header 0 --count 3 \
  --log_transform log  --variance $variance #--log_transform log #--phv $phv -

python $pydir/generate_config_files.py -d $outputfolder -o $dirname  -p 2  --rownames 0 --header 0 --count 4 \
  --center $center #--variance $variance #--log_transform log #--phv $phv -

python $pydir/generate_config_files.py -d $outputfolder -o $dirname  -p 2  --rownames 0 --header 0 --count 5 \
   --variance $variance #--log_transform log #--phv $phv #--center $center

python $pydir/generate_config_files.py -d $outputfolder -o $dirname  -p 2  --rownames 0 --header 0 --count 6 \
    --log_transform log #--phv $phv #--center $center --variance $variance

python $pydir/generate_config_files.py -d $outputfolder -o $dirname  -p 2  --rownames 0 --header 0 --count 7 \
  #--center $center #--variance $variance #--log_transform log #--phv $phv -

phv=0.9
python $pydir/generate_config_files.py -d $outputfolder -o $dirname  -p 2  --rownames 0 --header 0 --count 0 \
  --center $center --log_transform log  --variance $variance --phv $phv
