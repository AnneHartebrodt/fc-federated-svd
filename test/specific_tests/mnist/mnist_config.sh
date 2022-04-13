#!/bin/bash

# General test settings
clidir=/home/anne/Documents/featurecloud/test-environment/cli
pydir=/home/anne/Documents/featurecloud/apps/fc-federated-svd/test
basedir=/home/anne/Documents/featurecloud/test-environment/controller/data
controller_data_test_result=$basedir/tests

# This is where the mnist base data is stored.
mnist_raw_dir=$pydir/test_data/mnist/raw

# This is the general test folder
outputfolder=$basedir/mnist_test
mkdir -p $outputfolder

# This is where the input data is stored once loaded from raw mnist
mnisttsvdir=$basedir/mnist_test/data

# This is the folder containing the data splits and config files
app_test=mnist_test/mnist_out
dirname=mnist_out

# This is where the split data is generated in the data folder
split_dir=data_split

# generate the test report in this folder
test_report=/home/anne/Documents/featurecloud/test-environment/tests/mnist_out

# this is where the baseline result is stored.
baseline=$app_test/baseline_result
datafile=$mnisttsvdir/mnist.tsv


# These are some settings
seed=11
k=10
sites=3

