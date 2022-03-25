## MNIST

### Set up test environment
```
seed=11
sites=3
test_out=mnist
bash fc-federated-pca/app/test/specific_tests/mnist/setup_test_environment_mnist.sh $(pwd)/controller/data $(pwd)/cli $(pwd)/fc-federated-pca/app/test $(pwd)/test-data/mnist/mnnist.tsv $test_out $seed $sites
```

### Run tests

```
split_dir=data_split
suffix_list=( "$test_out/single" )
for d in "${suffix_list[@]}"
do
  bash fc-federated-pca/app/test/test.sh $(pwd)/controller/data/ $(pwd)/cli $(pwd)/fc-federated-pca/app/test $d $split_dir
done

```

### Generate the report

```
mkdir -p mnist-output/$seed/$sites
bash fc-federated-pca/app/test/generate_report.sh $(pwd)/controller/data/ $(pwd)/cli $(pwd)/fc-federated-pca/app/test $test_out  $(pwd)/test-output/$seed/$sites
```

### Batchify

```
for seed in {11..20};
do
for sites in 3 5 10;
do
test_out=mnist/$seed/$sites
echo $test_out
mkdir -p $test_out
# generate data
bash fc-federated-pca/app/test/specific_tests/mnist/setup_test_environment_mnist.sh $(pwd)/controller/data $(pwd)/cli $(pwd)/fc-federated-pca/app/test $(pwd)/test-data/mnist/mnnist.tsv $test_out $seed $sites

# run test
split_dir=data_split
suffix_list=( "$test_out/single" )
for d in "${suffix_list[@]}"
do
echo $d
  bash fc-federated-pca/app/test/test.sh $(pwd)/controller/data/ $(pwd)/cli $(pwd)/fc-federated-pca/app/test $d $split_dir
done
done
done
```


```
for seed in {11..20};
do
for sites in 3 5 10;
do
test_out=mnist/$seed/$sites
echo $test_out
tout=$(pwd)/mnist-output/$seed/$sites/single
mkdir -p $tout 
# seed is empty! Don't put
bash fc-federated-pca/app/test/generate_report.sh $(pwd)/controller/data/ $(pwd)/cli $(pwd)/fc-federated-pca/app/test $test_out/single  $tout $test_out/baseline_result
done
done
```

