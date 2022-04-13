#!/bin/bash

# Folder with the command line interface
clidir=/home/anne/Documents/featurecloud/test-environment/cli

# fully qualified path to this directory
pydir=/home/anne/Documents/featurecloud/apps/fc-federated-svd/test

# data directory of your controller instance
basedir=/home/anne/Documents/featurecloud/test-environment/controller/data

# generate the test report in this folder
test_report=/home/anne/Documents/featurecloud/test-environment/tests/random_out


datafile=data.tsv
outputfolder=$basedir/app_test

features=500
samples=5000
sites=3
k=10

# General test settings
controller_data_test_result=$basedir/tests


# This is the general test folder
outputfolder=$basedir/random_test
mkdir -p $outputfolder


# This is the folder containing the data splits and config files
app_test=random_test/random_out
dirname=random_out
# This is where the split data is generated in the data folder
split_dir=data_split


# this is where the baseline result is stored.
baseline=$app_test/baseline_result
datafile=data.tsv


# These are some settings
seed=11
k=10
sites=3

