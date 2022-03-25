import pandas as pd
import numpy as np
import scipy as sc
import os
import os.path as op
import argparse as ap

def read_presplit_data_folders(file_list, basedir):
    data_list = []
    row_list = []
    for file in file_list:
        print(file)
        data = pd.read_csv(os.path.join(basedir,file, 'data.tsv'), sep='\t', index_col=0, engine='python')
        rows = data.index
        row_list.append(rows)
        data = data.values
        data_list.append(data)
    return data_list, row_list, file_list

def save_scaled_data(datasets, data_dirs,basedir, transpose=True):
    for d, name in zip(data_dirs, datasets):
        try:
            # get all file names
            outdir_scaled = op.join(basedir, name)
            os.makedirs(outdir_scaled, exist_ok=True)
            filenames = os.listdir(d)
            data_list, row_list, file_list = read_presplit_data_folders(filenames, d)
            data_list = scale_datasets(data_list)
            if transpose:
                for ds, fl in zip(data_list, file_list):
                    ds = ds.T
                    pd.DataFrame(ds).to_csv(op.join(outdir_scaled, fl, 'scaled.tsv'), header=False, index=False, sep='\t')

        except FileNotFoundError:
            print('File not found')

def scale_datasets(data_list):
    sums = []
    sample_count = 0

    # mean
    sums = [np.sum(d, axis = 0) for d in data_list]
    sums = np.sum(sums, axis=0)
    sample_count = [d.shape[0] for d in data_list]
    total_count = sum(sample_count)
    means = [s/total_count for s in sums]
    for i in range(len(data_list)):
        data_list[i] = data_list[i] - means

    #variance

    vars = [np.sum(np.square(d), axis=0) for d in data_list]
    vars = np.sum(vars, axis = 0)
    vars = vars/(total_count-1)
    # variance  = 0
    delete = np.where(vars==0)
    vars = np.delete(vars, delete)
    for i in range(len(data_list)):
        data_list[i] = np.delete(data_list[i], delete, axis=1)

    for i in range(len(data_list)):
        data_list[i] = data_list[i]/np.sqrt(vars)
    return data_list


if __name__ == '__main__':

    parser = ap.ArgumentParser(description='Generate sample data for federated PCA')
    parser.add_argument('-d', metavar='DIRECTORY', type=str, help='output directory', default='.')
    args = parser.parse_args()


    #basedir = '/home/anne/Documents/featurecloud/data/tcga/cancer_type_site/'
    basedir = args.d
    datasets = os.listdir(basedir)
    data_dirs = [op.join(basedir, d) for d in datasets]

    # save scaled data
    save_scaled_data(datasets, data_dirs, basedir, transpose=True)