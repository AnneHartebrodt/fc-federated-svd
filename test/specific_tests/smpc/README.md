## SMPC exponents

### Set up test environment
```
testdir=/home/anne/Documents/featurecloud/apps/fc-federated-pca
seed=11
sites=3
test_out=smpc
bash $testdir/app/test/specific_tests/smpc/setup_test_environment_smpc.sh $(pwd)/controller/data $(pwd)/cli $testdir/app/test  $test_out $seed $sites
```

### Run tests

```
split_dir=data_split
suffix_list=( "$test_out/single" )
for d in "${suffix_list[@]}"
do
  bash $testdir/app/test/test.sh $(pwd)/controller/data/ $(pwd)/cli $testdir/app/test $d $split_dir
done

```

### Generate the report

```
outputfolder=smpc-output
mkdir -p $outputfolder
bash $testdir/app/test/generate_report.sh $(pwd)/controller/data/ $(pwd)/cli $testdir/app/test $test_out/single $(pwd)/$outputfolder $seed $test_out/baseline_result
```