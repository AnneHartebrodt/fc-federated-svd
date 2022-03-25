

#basedir=$1
#clidir=$2
#pydir=$3
#test_out=$4
#test_report=$5
#seed=$6
#baseline=$7

clidir=/home/anne/Documents/featurecloud/test-environment/cli
pydir=/home/anne/Documents/featurecloud/apps/fc-federated-svd/test
basedir=/home/anne/Documents/featurecloud/test-environment/controller/data
test_report=/home/anne/Documents/featurecloud//test-environment/tests/app_test/single
test_out=app_test/single
baseline=app_test/baseline_result
seed='11'

for od in $(ls $basedir/tests/$test_out/ )
do
    # collect all output files in a string separated variable
  cd $basedir/tests/$test_out/$od
  echo $(pwd)
  # get number of clients
  declare -i clients=$(ls *.zip| wc -l)

  for i in $(seq 0 $(($clients -1)))
  do

    sudo unzip -d client_$i $(ls | grep  client_$i)
  done

  cl=($(ls -l . | egrep '^d' | rev | cut -f1 -d' ' | rev))
  #collect the relevant files

#  if [ $(grep -e 'batch: true' $cl/config.yaml -c) = 1 ]
#    then
#      # batch mode
#      # check of train/test
#      dirs=($(ls -l $cl | egrep '^d' | rev | cut -f1 -d' ' | rev))
#      for d in "${dirs[@]}"
#      do
#      if [ -d $cl/$d/test ]
#      then
#        echo 'batch & cross validation'
#        tests=$(printf "$basedir/tests/$test_out/$od/%s/$d/test/right_eigenvectors.tsv " "${cl[@]}")
#        trains=$(printf "$basedir/tests/$test_out/$od/%s/$d/train/right_eigenvectors.tsv " "${cl[@]}");
#        python $pydir/check_accuracy.py -d $test_report -r $tests -R $basedir/$baseline/$d/eigen.right -l $basedir/tests/$test_out/$od/$cl/$d/test/left_eigenvectors.tsv \
#       -L $basedir/$baseline/$d/eigen.left -o $od"_"$d"_test.tsv" -e $basedir/tests/$test_out/$od/$cl/config.yaml -i $basedir/tests/$test_out/$od/$cl/$d/test/run_log.txt \
#       -S $basedir/$baseline/$d/eigen.values -s $basedir/tests/$test_out/$od/$cl/$d/test/eigenvalues.tsv
#       python $pydir/check_accuracy.py -d $test_report -r $trains -R $basedir/$baseline/$d/eigen.right -l $basedir/tests/$test_out/$od/$cl/$d/test/left_eigenvectors.tsv \
#       -L $basedir/$baseline/$d/eigen.left -o $od"_"$d"_train.tsv" -e $basedir/tests/$test_out/$od/$cl/config.yaml -i $basedir/tests/$test_out/$od/$cl/$d/test/run_log.txt \
#       -S $basedir/$baseline/$d/eigen.values -s $basedir/tests/$test_out/$od/$cl/$d/test/eigenvalues.tsv
#      else
#        echo 'only batch'
#        tests=$(printf "$basedir/tests/$test_out/$od/%s/$d/right_eigenvectors.tsv " "${cl[@]}")
#        python $pydir/check_accuracy.py -d $test_report -r $tests -R $basedir/$baseline/$d/eigen.right -l $basedir/tests/$test_out/$od/$cl/$d/left_eigenvectors.tsv \
#       -L $basedir/$baseline/$d/eigen.left -o $od"_"$d"_test.tsv" -e $basedir/tests/$test_out/$od/$cl/config.yaml -i $basedir/tests/$test_out/$od/$cl/$d/run_log.txt \
#       -S $basedir/$baseline/$d/eigen.values -s $basedir/tests/$test_out/$od/$cl/$d/eigenvalues.tsv
#      fi
#      done
#
#    else
    echo 'single mode'
    tests=$(printf "$basedir/tests/$test_out/$od/%s/right_eigenvectors.tsv " "${cl[@]}")
    echo $tests
    python $pydir/check_accuracy.py -d $test_report -r $tests -R $basedir/$baseline/eigen.right -l $basedir/tests/$test_out/$od/$cl/left_eigenvectors.tsv \
     -L $basedir/$baseline/eigen.left -o $od"_"$d"_test.tsv" -e $basedir/tests/$test_out/$od/$cl/config.yaml -i $basedir/tests/$test_out/$od/$cl/run_log.txt \
     -S $basedir/$baseline/eigen.values -s $basedir/tests/$test_out/$od/$cl/eigenvalues.tsv --header 0 --rownames 0

    #fi
  cd ..
done

od=($(ls $basedir/tests/$test_out/ ))
tests=$(printf "$basedir/tests/$test_out/%s/$cl/log.txt " "${od[@]}")
ids=$(printf "%s " "${od[@]}")
echo $tests
echo $ids
echo "runstats"
#python $pydir/runstats.py -d $test_report -o "run_summaries.tsv" -f $tests -i $ids
# generate report
python $pydir/generate_report.py -d $test_report/test_results -r $test_report/report.md
pandoc $test_report/report.md -f markdown -t html -o $test_report/report.html --css $pydir/templates/pandoc.css
