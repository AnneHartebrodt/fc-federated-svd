# Semi-automated testing of FC app

## Set up environment
Prerequisites: Docker and conda installed.
### Featurecloud CLI
```
mkdir fc-app-testing
cd fc-app-testing
git clone git@github.com:FeatureCloud/cli.git
cd cli
# requirements file is for pip
# remove '~' to fit conda
conda create --name cli --file requirements_conda.txt
# additional dependecies
conda activate cli
conda install pyyaml scipy pandoc markdown
cd ..
```

### Controller
For UNIX systems download controller and start controller
```
mkdir controller
cd controller
wget https://featurecloud.ai/assets/scripts/start_controller.sh
bash start_controller.sh
cd ..
```

### FC PCA code
Clone this repository
```
git clone git@github.com:AnneHartebrodt/fc-federated-pca.git
cd fc-federated-pca
#build docker image
docker build . --tag=federated_pca_batch
# add python path 
cd ..
export PYTHONPATH=$(pwd)/fc-federated-pca
```

### Set up test environment with autogenerated toy data
```
seed=11
sites=4
test_out=app_test
bash fc-federated-pca/app/test/setup_test_environment.sh $(pwd)/controller/data/ $(pwd)/cli $(pwd)/fc-federated-pca/app/test $test_out $seed $sites
```
### Run the app
```
split_dir=data_split
#suffix_list=( "$test_out/single" "$test_out/batch_cross" "$test_out/batch")
suffix_list=( "$test_out/single")
for d in "${suffix_list[@]}"
do
  bash fc-federated-pca/app/test/test.sh $(pwd)/controller/data/ $(pwd)/cli $(pwd)/fc-federated-pca/app/test $d $split_dir
done
```

### Generate the report
```
suffix_list=( "$test_out/single" "$test_out/batch_cross" "$test_out/batch")
for d in "${suffix_list[@]}"
do
mkdir -p test-output
bash fc-federated-pca/app/test/generate_report.sh $(pwd)/controller/data/ $(pwd)/cli $(pwd)/fc-federated-pca/app/test $d $(pwd)/test-output $seed $test_out/baseline_result
done
```

## Batchify
```
seed=11
for sites in 3 5 10;
do
test_out=app_test/$seed/$sites
bash fc-federated-pca/app/test/setup_test_environment.sh $(pwd)/controller/data/ $(pwd)/cli $(pwd)/fc-federated-pca/app/test $test_out $seed $sites

split_dir=data_split
suffix_list=( "$test_out/single" "$test_out/batch_cross" "$test_out/batch")
for d in "${suffix_list[@]}"
do
  bash fc-federated-pca/app/test/test.sh $(pwd)/controller/data/ $(pwd)/cli $(pwd)/fc-federated-pca/app/test $d $split_dir $
done
done

```
```
seed=11
for sites in 3 5 10;
do
test_out=app_test/$seed/$sites
split_dir=data_split
suffix_list=( "$test_out/single" "$test_out/batch_cross" "$test_out/batch")
for d in "${suffix_list[@]}"
do
outputfolder=test-output/$seed/$sites
mkdir -p $outputfolder
bash fc-federated-pca/app/test/generate_report.sh $(pwd)/controller/data/ $(pwd)/cli $(pwd)/fc-federated-pca/app/test $d $(pwd)/$outputfolder $seed $test_out/baseline_result
done
done

```
