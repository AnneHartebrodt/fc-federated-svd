#clidir=/home/anne/Documents/featurecloud/test-environment/cli
#pydir=/home/anne/Documents/featurecloud/apps/fc-federated-pca/app/test
#basedir=/home/anne/Documents/featurecloud/test-environment/controller/data
#outputfolder=$basedir/app_test_tgca
#seed=1
#datafolder=/home/anne/Documents/featurecloud/data/tcga/cancer_type_site

basedir=$1
clidir=$2
pydir=$3
datafolder=$4
outputfolder=$basedir/$5
seed=$6

echo $pydir
echo $basedir
echo $clidir
echo $datafile
echo $outputfolder
mkdir -p $outputfolder


k=10

for ct in $(ls $datafolder);
do
dirs=($(ls -d $datafolder/$ct/*/data.tsv))
dirs=$(printf "%s " "${dirs[@]}")
# remove trailing comma
#compute canonical solution
echo $dirs
mkdir -p $outputfolder/$ct
mkdir -p $outputfolder/$ct/data
cp -r $datafolder/$ct/* $outputfolder/$ct/data
python $pydir/compute_canonical_solution.py -d $outputfolder/$ct -L $dirs -k $k -s $seed --transpose True --rownames 0


python $pydir/generate_config_files.py -d $outputfolder/$ct -o . -i 1000 -q 0 -s 0 -a True -p True -n 0 -f 'scaled.tsv'
done