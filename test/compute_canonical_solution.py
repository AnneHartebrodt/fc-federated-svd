import sys
sys.path.append('/home/anne/Documents/featurecloud/apps/fc-federated-svd/')
import numpy as np
import scipy as sc
import pandas as pd
import scipy.sparse.linalg as la
import os
import argparse as ap
import yaml
import os.path as op
import apps.svd.shared_functions as sh

def compute_and_save_canonical(input_file, output_folder,k=10, seed = 11, prefix='singular', header=None, index_col=None,
                               sep='\t', transpose=False, center=True, variance=True, log=True, highly_variable=False,
                               perc_hv=0.1
                               ):
    np.random.seed(seed)
    if isinstance(input_file, str):
        data = pd.read_csv(input_file, sep=sep, header=header, index_col=index_col)


    else:
        data = input_file

    if transpose:
        rownames = data.columns.values
        colnames = data.index.values
        data = data.values.T

    else:
        rownames = data.index.values
        colnames =data.columns.values
        data = data.values



    if log:
        print('TRANSFORM')
        data = np.log2(data+1)

    nans = np.sum(np.isnan(data), axis=1)
    print(nans)
    nanfrac = nans / data.shape[1]
    nanindx = np.where(nanfrac <= 1)[0]
    print(nanindx)
    print(data)
    data = data[nanindx, :]

    if center:
        print('center')
        means = np.nanmean(data,  axis=1)
        means = np.atleast_2d(means).T
        data = data-means
        print(means)
        print(data)

    if variance:
        print('scale variance')
        print(np.nansum(np.square(data), axis=1))
        stds = np.nanstd(data, axis=1, ddof=1)
        stds = np.atleast_2d(stds).T
        print(stds)
        data = data/stds


    if highly_variable:
        print('hello')

    print(data.shape)
    data = np.nan_to_num(data, nan=0, posinf=0, neginf=0)

    md = min(data.shape) - 1
    print(md)
    k = min(k, md)
    print(k)
    rownames = rownames[nanindx]

    print(np.cov(data))
    u, s, v, nd = sh.svd_sub(data, ndims=k)

    os.makedirs(output_folder, exist_ok=True)
    pd.DataFrame(u, index=rownames).to_csv(op.join(output_folder, prefix + '.left'), sep='\t')
    pd.DataFrame(s).to_csv(op.join(output_folder, prefix + '.values'), sep='\t', header=False, index=False)
    pd.DataFrame(v, index=colnames).to_csv(op.join(output_folder, prefix + '.right'), sep='\t')

def concatenate_files(filelist, header=None, sep='\t', index_col=None):
    fl = []
    for f in filelist:
        fl.append(pd.read_csv(f, header=header, sep=sep, index_col=index_col))
    fl = pd.concat(fl, axis=0)
    return fl

def read_config(configfile):
    with open(op.join(configfile), 'r') as handle:
        config = yaml.safe_load(handle)
    return config


if __name__ == '__main__':
    parser = ap.ArgumentParser(description='Generate sample data for federated PCA')
    parser.add_argument('-d', metavar='DIRECTORY', type=str, help='output directory', default='.')
    parser.add_argument('-f', metavar='INPUT_FILE', type=str, help='filename of data file', default=None)
    parser.add_argument('-F', metavar='INPUT_FILE', type=str, help='filename of data file (full path)', default=None)
    parser.add_argument('-L', metavar='INPUT_FILE LIST', type=str, nargs='+', help='filenames of data file (full path)', default=None)
    parser.add_argument('-o', metavar='OUTPUT_FILE', type=str, help='output file prefix', default='eigen')
    parser.add_argument('-k', metavar='K', type=int, help='Number of dimensions')
    parser.add_argument('-s', metavar='SEED', type=int, help='random seed', default=11)
    parser.add_argument('--header', metavar='HEADER', type=int, help='header (line number)', default=None)
    parser.add_argument('--rownames', metavar='ROW NAMES', type=int, help='row names (column number)', default=None)
    parser.add_argument('--separator', metavar='SEPARATOR', type=str, help='separator', default='\t')
    parser.add_argument('--transpose', metavar='TRANSPOSE', type=bool, help='transpose matrices', default=False)
    parser.add_argument('--config', metavar='CONFIG_file', type=str, help='center matrices', default=None)

    args = parser.parse_args()
    basedir = args.d
    output_folder = op.join(args.d, 'baseline_results')

    if args.header is not None:
        header = int(args.header)
    else:
        header=None
    if args.rownames is not None:
        index_col = int(args.rownames)
    else:
        index_col=None
    print(index_col)

    output_folder = op.join(basedir)

    if args.f is not None:
        input_file = op.join(basedir, 'data', args.f)
    elif args.F is not None:
        input_file = args.F
    else:
        input_file = concatenate_files(args.L, header=header, index_col=index_col, sep=args.separator)


    config = read_config(args.config)
    center = config['fc_pca']['scaling']['center']
    variance = config['fc_pca']['scaling']['variance']
    log_transform = config['fc_pca']['scaling']['log_transform']
    phv = config['fc_pca']['scaling']['perc_highly_var']
    highly = config['fc_pca']['scaling']['highly_variable']

    print("LOG TRANSFORM" +str(log_transform))
    compute_and_save_canonical(input_file=input_file,
                               output_folder=output_folder,
                               seed=args.s,
                               prefix=args.o,
                               k=args.k,
                               header=header,
                               index_col=index_col,
                               sep=args.separator,
                               transpose=args.transpose,
                               center=center,
                               variance=variance,
                               highly_variable=highly,
                               log=log_transform,
                               perc_hv=phv
                               )

