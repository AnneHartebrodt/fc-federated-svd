#mydir=$(pwd)

#basedir=$1
#clidir=$2
#pydir=$3
#app_test=$4
#split_dir=$5

clidir=/home/anne/Documents/featurecloud/test-environment/cli
pydir=/home/anne/Documents/featurecloud/apps/fc-federated-svd/app/test
basedir=/home/anne/Documents/featurecloud/test-environment/controller/data
app_test=app_test/single
split_dir=data_split

controller_data_test_result=$basedir/tests

count=1
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
  python $clidir/cli.py start --controller-host http://localhost:8000 --client-dirs $dirs --app-image featurecloud.ai/federated_svd:latest --channel internet --query-interval 0 \
    --download-results $outputdir --generic-dir $app_test/config_files/$configf

done



# make sure the data is downloaded!!!



