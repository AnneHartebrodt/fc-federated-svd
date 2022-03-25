import sys
sys.path.append('/home/anne/Documents/featurecloud/apps/fc-federated-svd/')
import numpy as np
import scipy as sc
import pandas as pd
import scipy.sparse.linalg as la
import os
import argparse as ap
import os.path as op
import apps.svd.shared_functions as sh

def compute_and_save_canonical(input_file, output_folder,k=10, seed = 11, prefix='singular', header=None, index_col=None,
                               sep='\t', transpose=False):
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
    print('DATA')
    print(data)
    u, s, v, nd = sh.svd_sub(data, ndims=k)
    print('COVARIANCE')
    print(np.cov(data))
    print(np.cov(data).shape)
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

if __name__ == '__main__':
    parser = ap.ArgumentParser(description='Generate sample data for federated PCA')
    parser.add_argument('-d', metavar='DIRECTORY', type=str, help='output directory', default='.')
    parser.add_argument('-f', metavar='INPUT_FILE', type=str, help='filename of data file', default=None)
    parser.add_argument('-F', metavar='INPUT_FILE', type=str, help='filename of data file (full path)', default=None)
    parser.add_argument('-L', metavar='INPUT_FILE LIST', type=str, nargs='+', help='filenames of data file (full path)', default=None)
    parser.add_argument('-o', metavar='OUTPUT_FILE', type=str, help='output file prefix', default='eigen')
    parser.add_argument('-k', metavar='K', type=int, help='Number of dimensions')
    parser.add_argument('-s', metavar='SEED', type=int, help='random seed', default=11)
    parser.add_argument('-b', metavar='BATCH', type = bool, help='batch mode', default=False)
    parser.add_argument('--header', metavar='HEADER', type=int, help='header (line number)', default=None)
    parser.add_argument('--rownames', metavar='ROW NAMES', type=int, help='row names (column number)', default=None)
    parser.add_argument('--separator', metavar='SEPARATOR', type=str, help='separator', default='\t')
    parser.add_argument('--transpose', metavar='TRANSPOSE', type=bool, help='transpose matrices', default=False)
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
    if args.b:
        input_folders = os.listdir(op.join(basedir, 'data'))
        input_folders = [int(i) for i in input_folders]
        for i in input_folders:
            output_folder = op.join(basedir, 'baseline_result', str(i))
            if args.f is not None:
                input_file = op.join(basedir, 'data', str(i), args.f)
            elif args.F is not None :
                input_file = args.F
            else:
                input_file = concatenate_files(args.L, header=header, index_col=index_col, sep=args.separator)

            compute_and_save_canonical(input_file=input_file,
                                           output_folder=output_folder,
                                           seed=i,
                                           prefix=args.o,
                                           k=args.k,
                                           header=header,
                                           index_col=index_col,
                                           sep=args.separator,
                                           transpose=args.transpose)
    else:
        output_folder = op.join(basedir, 'baseline_result')

        if args.f is not None:
            input_file = op.join(basedir, 'data', args.f)
        elif args.F is not None:
            input_file = args.F
        else:
            input_file = concatenate_files(args.L, header=header, index_col=index_col, sep=args.separator)
        compute_and_save_canonical(input_file=input_file,
                                   output_folder=output_folder,
                                   seed=args.s,
                                   prefix=args.o,
                                   k=args.k,
                                   header=header,
                                   index_col=index_col,
                                   sep=args.separator,
                                   transpose=args.transpose
                                   )

