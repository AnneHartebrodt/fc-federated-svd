#!/bin/bash

source specific_tests/mnist/mnist_config.sh


for od in $(ls $basedir/tests/$app_test/ )
do
    # collect all output files in a string separated variable
  cd $basedir/tests/$app_test/$od
  echo $(pwd)
  # get number of clients
  declare -i clients=$(ls *.zip| wc -l)

  for i in $(seq 0 $(($clients -1)))
  do

    sudo unzip -d client_$i $(ls | grep  client_$i)
  done

  cl=($(ls -l . | egrep '^d' | rev | cut -f1 -d' ' | rev))
  echo 'single mode'
  tests=$(printf "$basedir/tests/$app_test/$od/%s/right_eigenvectors.tsv " "${cl[@]}")

  python $pydir/compute_canonical_solution.py -d $basedir/$baseline -f $datafile -k $k -s $seed  --header 0 \
  --transpose True --rownames 0 --config $basedir/tests/$app_test/$od/$cl/config.yaml
  python $pydir/check_accuracy.py -d $test_report -r $tests -R $basedir/$baseline/eigen.right -l $basedir/tests/$app_test/$od/$cl/left_eigenvectors.tsv \
   -L $basedir/$baseline/eigen.left -o $od"_"$d"_test.tsv" -e $basedir/tests/$app_test/$od/$cl/config.yaml -i $basedir/tests/$app_test/$od/$cl/run_log.txt \
   -S $basedir/$baseline/eigen.values -s $basedir/tests/$app_test/$od/$cl/eigenvalues.tsv --header 0 --rownames 0

  #fi
  cd ..
done

od=($(ls $basedir/tests/$app_test/ ))
tests=$(printf "$basedir/tests/$app_test/%s/$cl/log.txt " "${od[@]}")
ids=$(printf "%s " "${od[@]}")


#python $pydir/runstats.py -d $test_report -o "run_summaries.tsv" -f $tests -i $ids
# generate report
python $pydir/generate_report.py -d $test_report/test_results -r $test_report/report.md
pandoc $test_report/report.md -f markdown -t html -o $test_report/report.html --css $pydir/templates/pandoc.css
