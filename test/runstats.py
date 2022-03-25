import sys
sys.path.append('/home/anne/Documents/featurecloud/apps/fc-federated-svd/')


import pandas as pd
import argparse as ap
import numpy as np
import os.path as op


def summarize(files, ids, outfile):
    dfl  = []
    cols = []
    actual_ids = []
    for f in range(len(files)):
        try:
            df = pd.read_csv(files[f], sep='\t', header=None, index_col=None)
            print(df)
            actual_ids.append(ids[f])
            dfl.append(df.iloc[:,1])
            cols = df.iloc[:,0].values
        except:
            print(files[f])
            print('File not found')
    df = pd.concat(dfl, axis=1)
    df = df.transpose().values
    actual_ids= np.array(actual_ids)
    actual_ids = np.atleast_2d(actual_ids).T
    df = np.concatenate([actual_ids, df], axis=1)
    df = pd.DataFrame(df)
    cols = ['Run ID'] + cols.tolist()
    df.columns = cols
    #df = df.round(2)
    df.to_csv(outfile, sep='\t', index = False)




if __name__ == '__main__':
    parser = ap.ArgumentParser(description='Split complete data into test data for federated PCA')
    parser.add_argument('-d', metavar='DIRECTORY', type=str, help='output directory', default='.')
    parser.add_argument('-o', metavar='OUTPUT', type=str, help='filename of evaluation output')
    parser.add_argument('-f', metavar='INPUT file list', type=str, nargs='+', help='config file')
    parser.add_argument('-i', metavar='INPUT ids', type=str, nargs='+', help='config file')

    args = parser.parse_args()
    basedir = args.d
    summarize(args.f, args.i, op.join(args.d, args.o))
