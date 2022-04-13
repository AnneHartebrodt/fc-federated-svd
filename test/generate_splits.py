import sys
sys.path.append('/home/anne/Documents/featurecloud/apps/fc-federated-svd/')
from apps.svd.shared_functions import partition_data_horizontally
import os
import os.path as op
import pandas as pd
import numpy
import argparse as ap
import numpy as np


def make_horizontal_splits(input_file, output_folder, splits=3, seed = 11, batch=False, train=False, header=None, index_col=None,
                               sep='\t', transpose=False):
    print(input_file)
    data = pd.read_csv(input_file, sep=sep, header=header, index_col=index_col)
    rownames = data.index.values
    colnames = data.columns.values
    data = data.values
    data_list, choice = partition_data_horizontally(data, splits=splits)
    if transpose:
        c1 = colnames
        colnames = rownames
        rownames = c1
        data_list = [d.T for d in data_list]

    if transpose:
        start = 0
        colnames_l = []
        for d in data_list:
            end = start+d.shape[1]
            colnames_l.append(colnames[start:end])
            start = end
    else:
        start = 0
        rownames_l = []
        for d in data_list:
            end = start + d.shape[0]
            rownames_l.append(rownames[start:end])
            start = end

    for i in range(splits):
        if batch:
            if train:
                for t in ['train', 'test']:
                    os.makedirs(op.join(output_folder, str(i), str(seed), str(t)), exist_ok=True)
                    # basedir/data_splits/client/crossvalidation_split
                    mydata = pd.DataFrame(data_list[i])
                    if transpose:
                        mydata['rownames'] = rownames
                        mydata = mydata.set_index('rownames')
                        mydata.columns = colnames_l[i]
                    else:
                        mydata['rownames'] = rownames_l[i]
                        mydata = mydata.set_index('rownames')
                        mydata.columns = colnames
                    mydata.to_csv(op.join(output_folder, str(i), str(seed), str(t), 'data.tsv'), sep='\t', header=True, index=True)
            else:
                os.makedirs(op.join(output_folder, str(i), str(seed)), exist_ok=True)
                # basedir/data_splits/client/crossvalidation_split
                mydata = pd.DataFrame(data_list[i])
                if transpose:
                    mydata['rownames'] = rownames
                    mydata = mydata.set_index('rownames')
                    mydata.columns = colnames_l[i]
                else:
                    mydata['rownames'] = rownames_l[i]
                    mydata = mydata.set_index('rownames')
                    mydata.columns = colnames
                mydata.to_csv(op.join(output_folder, str(i), str(seed), 'data.tsv'), sep='\t',
                                                  header=True, index=True)

        else:
            os.makedirs(op.join(output_folder, str(i)), exist_ok=True)
            # basedir/data_splits/client/crossvalidation_split
            mydata = pd.DataFrame(data_list[i])
            if transpose:
                mydata['rownames'] = rownames
                mydata = mydata.set_index('rownames')
                mydata.columns = colnames_l[i]
            else:
                mydata['rownames'] = rownames_l[i]
                mydata = mydata.set_index('rownames')
                mydata.columns = colnames

            mydata.to_csv(op.join(output_folder, str(i), 'data.tsv'), sep='\t',
                                              header=True, index=True)


if __name__ == '__main__':

    parser = ap.ArgumentParser(description='Split complete data into test data for federated PCA')
    parser.add_argument('-d', metavar='DIRECTORY', type=str, help='base directory', default='.')
    parser.add_argument('-o', metavar='OUTPUT_DIRECTORY_NAME', type=str, help='output directory', default='.')
    parser.add_argument('-f', metavar='INPUT_FILE', type=str, help='filename of data file')
    parser.add_argument('-F', metavar='INPUT_FILE', type=str, help='filename of data file (full path)', default=None)
    parser.add_argument('-n', metavar='SITES', type=int, help='Number of sites')
    parser.add_argument('-s', metavar='SEED/FOLDER_NAME', type=int, help='random seed.', default=11)
    parser.add_argument('-b', metavar='BATCH', type=bool, help='batch mode', default=False)
    parser.add_argument('-t', metavar='TRAIN', type=bool, help='batch mode', default=False)
    parser.add_argument('--header', metavar='HEADER', type=int, help='header (line number)', default=None)
    parser.add_argument('--rownames', metavar='ROW NAMES', type=int, help='row names (column number)', default=None)
    parser.add_argument('--transpose', metavar='TRANSPOSE', type=bool, help='transpose matrices', default=False)
    parser.add_argument('--separator', metavar='SEPARATOR', type=str, help='separator', default='\t')

    args = parser.parse_args()
    basedir = args.d
    output_folder = op.join(basedir, args.o, 'data_split')

    if args.header is not None:
        header = int(args.header)
    else:
        header=None
    if args.rownames is not None:
        index_col = int(args.rownames)
    else:
        index_col=None


    if args.F is None:
        input_file = op.join(basedir, 'data',  args.f)
    else:
        print('input_file '+args.F)
        input_file =args.F
    make_horizontal_splits(input_file=input_file,
                           output_folder=output_folder,
                           splits=args.n,
                           seed=args.s,
                           batch=False,
                            header=header,
                           index_col=index_col,
                           sep=args.separator,
                           transpose=args.transpose
                           )
