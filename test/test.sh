#!/bin/bash

#source specific_tests/mnist/mnist_config.sh
source specific_tests/random/random_config.sh

outdirs=()

echo $app_test
# loop over all configuration files
for configf in $(ls $basedir/$app_test/config_files)
do
  # start run
  # collect all directories in a string separated variable
  cd $basedir
  echo $(pwd)
  dirs=($(ls -d $app_test/$split_dir/*))
  dirs=$(printf "%s," "${dirs[@]}")
  # remove trailing comma
  dirs=$(echo $dirs | sed 's/,*$//g')
  cd $mydir

  # generate a random string to use as the output directory
  outputdir=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 13 ; echo '')
  outputdir=$app_test/$outputdir
  outdirs[${#outdirs[@]}]=$outputdir
  sudo mkdir -p $controller_data_test_result/$app_test


  #echo $dirs
  echo python $clidir/cli.py start --controller-host http://localhost:8000 --client-dirs $dirs --app-image federated_svd:latest --channel internet --query-interval 0 \
    --download-results $outputdir --generic-dir $app_test/config_files/$configf
  python $clidir/cli.py start --controller-host http://localhost:8000 --client-dirs $dirs --app-image featurecloud.ai/federated_svd:latest --channel local --query-interval 0 \
    --download-results $outputdir --generic-dir $app_test/config_files/$configf

done


