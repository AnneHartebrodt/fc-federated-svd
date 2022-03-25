import sys
sys.path.append('/home/anne/Documents/featurecloud/apps/fc-federated-svd/')

import apps.svd.shared_functions as sh
import apps.svd.comparison as co
import pandas as pd
import argparse as ap
import numpy as np
import os as os
import os.path as op
import yaml
import markdown
import apps.svd.markdown_utils as md



def read_and_concatenate_eigenvectors(file_list):
    eigenvector_list=[]
    for f in file_list:
        eig0 = pd.read_csv(f, sep='\t', index_col=args.rownames, header=args.header)
        eig0 = eig0.values
        eigenvector_list.append(eig0)
    eig = np.concatenate(eigenvector_list, axis=0)
    return eig

def read_config(configfile):
    with open(op.join(configfile), 'r') as handle:
        config = yaml.safe_load(handle)
    return config

def read_iterations(iteration_file):
    with open(iteration_file, 'r') as handle:
        iterations = handle.readline().split()[1]
        runtime = round(float(handle.readline().split()[1]), 2)
        print(iterations)
        print(runtime)
    return iterations, runtime




def create_result(left_angles, right_angles, diff, config, run_id='NA', config_path='NA', result_path='NA'):
    l = []
    names = []
    names.append('Run ID')
    names.append('seed')
    names.append('t')

    ar = run_id.split('_')
    for a in ar:
        l.append(a.split('.')[0])


    for key in config:
        names.append(key)
        l.append(config[key])
    for a in range(len(left_angles)):
        names.append('LSV'+str(a+1))
        l.append(left_angles[a])
    for a in range(len(right_angles)):
        names.append('RSV'+str(a+1))
        l.append(right_angles[a])
    for d in range(len(diff)):
        names.append('SV'+str(d+1))
        l.append(diff[d])
    data = pd.DataFrame(l).T
    data.columns = names
    return data




if __name__ == '__main__':
    parser = ap.ArgumentParser(description='Split complete data into test data for federated PCA')
    parser.add_argument('-d', metavar='DIRECTORY', type=str, help='output directory', default='.')
    parser.add_argument('-l', metavar='left eigenvectors', type=str, help='filenames left eigenvectors (only 1)')
    parser.add_argument('-r', metavar='right eigenvectors', type=str, help='filename right eigenvectors ', nargs='+')
    parser.add_argument('-L', metavar='CANONICAL', type=str, help='filename of canonical left solution')
    parser.add_argument('-R', metavar='CANONICAL', type=str, help='filename of canonical right solution')
    parser.add_argument('-s', metavar='eigenvalue', type=str, help='eigenvalue file')
    parser.add_argument('-S', metavar='CANONICAL eigenvalue', type=str, help='eigenvalue file')
    parser.add_argument('-o', metavar='OUTPUT', type=str, help='filename of evaluation output')
    parser.add_argument('-e', metavar='CONFIG', type=str, help='config file')
    parser.add_argument('-i', metavar='ITERATIONS', type=str, help='iteration file')
    parser.add_argument('--header', metavar='HEADER', type=int, help='header (line number)', default=None)
    parser.add_argument('--rownames', metavar='ROW NAMES', type=int, help='row names (column number)', default=None)
    args = parser.parse_args()
    basedir = args.d


    os.makedirs(op.join(basedir, 'test_results'), exist_ok=True)
    federated_eigenvectors = pd.read_csv(args.l, header=args.header, index_col=args.rownames, sep='\t')
    canconical_eigenvectors = pd.read_csv(args.L, header=args.header, index_col=args.rownames, sep='\t')
    print(federated_eigenvectors.index)
    print(canconical_eigenvectors.index)
    d = {k: v for v, k in enumerate(canconical_eigenvectors.index)}
    print(d)
    index = []
    for elem in federated_eigenvectors.index:
        if elem in d:
            index.append(d[elem])
    print('INDEX')
    print(index)
    print(federated_eigenvectors)
    print(canconical_eigenvectors)
    print(pd.DataFrame(canconical_eigenvectors.values[ index, :]))
    left_angles = co.compute_angles(federated_eigenvectors.values, canconical_eigenvectors.values[index,:])
    left_angles = [np.round(a, 2) for a in left_angles]
    print(left_angles)


    federated_eigenvectors = read_and_concatenate_eigenvectors(args.r)
    print(federated_eigenvectors)
    canconical_eigenvectors = pd.read_csv(args.R, header=args.header, index_col=args.rownames, sep='\t').values
    print(canconical_eigenvectors)
    right_angles = co.compute_angles(federated_eigenvectors, canconical_eigenvectors)
    right_angles = [np.round(a, 2) for a in right_angles]

    feigenvalue = pd.read_csv(args.s, sep='\t', header=None, index_col=None).values.flatten()
    ceigenvalue = pd.read_csv(args.S, sep='\t', header=None, index_col=None).values.flatten()
    diff = co.compare_eigenvalues(feigenvalue, ceigenvalue)
    diff = [np.round(d,2) for d in diff]

    config = read_config(configfile=args.e)
    subconf = config['fc_pca']['algorithm']
    subconf['smpc'] = config['fc_pca']['privacy']['use_smpc']


    subconf['iterations'], subconf['runtime'] = read_iterations(args.i)
    #subconf['runtime'] = read_iterations(args.i)[1]

    ouput_table = create_result(left_angles, right_angles, diff, subconf,
                                run_id=args.o,
                                config_path=args.e,
                                result_path = args.R
                                )
    ouput_table.to_csv(op.join(op.join(basedir, 'test_results', args.o)), sep='\t', index=False)





#
# import scipy.linalg as la
# import pandas as pd
# d = pd.read_csv('/home/anne/Documents/featurecloud/test-environment/controller/data/app_test/data/data.tsv', sep='\t', index_col=0)
# d = d.values
# u,s,v = la.svd(d)
#
# index = [1,2,5,0,6,9,8,4,7,3]
# u1,s1,v1 = la.svd(d[:, index])
#
# v11 = v[:, index]
# 4, 7, 2, 1,