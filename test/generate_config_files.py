import yaml
import os.path as op
import os
import argparse as ap


def make_default_config_file(algorithm = 'power_iteration',
                             qr='no_qr',
                             init = 'random',
                             batch=False,
                             train_test=False,
                             maxit=500,
                             use_smpc = True,
                             datafile = 'data.tsv',
                             exponent=3,
                             rownames=True,
                             colnames=True,
                             send_projections=False,
                             subsample=True):

    """
    Default config file generator
    qr: one of 'federated_qr'| 'no_qr'
    :return:
    """
    dict = {'fc_pca':
             {'input':
                  {'data': datafile,
                   'batch': batch,
                   'train_test': train_test},
              'output':
                  {'projections': 'reduced_data.tsv',
                   'left_eigenvectors': 'left_eigenvectors.tsv',
                   'right_eigenvectors': 'right_eigenvectors.tsv',
                   'eigenvalues': 'eigenvalues.tsv'},
              'algorithm':
                  {'pcs': 10,
                   'algorithm': algorithm,
                   'max_iterations': maxit,
                   'qr': qr,
                   'epsilon': 1e-9,
                   'init': init
                   },
              'settings':
                  {'delimiter': '\t',
                   'rownames': rownames,
                   'colnames': colnames},
              'privacy':
                  {'send_projections': send_projections,
                   'subsample_projections': subsample,
                   'encryption': 'no_encryption',
                   'use_smpc': use_smpc,
                   'exponent': exponent},
              'scaling': {
                  'center': False,
                  'highly_variable': False,
                  'variance': False,
                  'perc_highly_var': 0.1,
                  'log_transform': False}
              }
            }
    return dict

def write_config(config, basedir, counter):
    os.makedirs(op.join(basedir,  str(counter)), exist_ok=True)
    with open(op.join(basedir,  str(counter), 'config.yaml'), 'w') as handle:
        yaml.safe_dump(config, handle, default_flow_style=False, allow_unicode=True)


def create_configs_power(output_folder, batch=False, train_test=False, maxit=500,  algorithms=['power_iteration', 'randomized'],   qr = ['federated_qr', 'no_qr'],
                         init=['approximate_pca', 'random'], use_smpc=[True, False], datafile='data.tsv', exponent=3, counter=0,
                         colnames = True, rownames = True, send_projections=[True]):

    for a in algorithms:
        for q in qr:
            for i in init:
                for s in use_smpc:
                    for p in send_projections:
                        config = make_default_config_file(batch=batch,
                                                          algorithm=a,
                                                          qr=q,
                                                          init=i,
                                                          train_test=train_test,
                                                          maxit=maxit,
                                                          use_smpc=s,
                                                          datafile=datafile,
                                                          exponent=exponent,
                                                          rownames=rownames,
                                                          colnames=colnames,
                                                          send_projections=p)
                        write_config(config=config, basedir=output_folder, counter=counter)
                        counter = counter + 1
    return counter



if __name__ == '__main__':
    parser = ap.ArgumentParser(description='Split complete data into test data for federated PCA')
    parser.add_argument('-d', metavar='DIRECTORY', type=str, help='output directory', default='.')
    parser.add_argument('-b', metavar='BATCH', type=bool, help='batch mode', default=False)
    parser.add_argument('-t', metavar='TRAIN_TEST', type=bool, help='batch mode', default=False)
    parser.add_argument('-s', metavar='USE SMPC', type=int, help='0 = no, 1=yes, 2=both', default=0)
    parser.add_argument('-o', metavar='OUTPUT_DIRECTORY_NAME', type=str, help='output directory', default='.')
    parser.add_argument('-i', metavar='ITERATIONS', type=int, help='number of iteratins', default=1000)
    parser.add_argument('-q', metavar='FEDERATED QR', type=int, help='0=no, 1=yes, 2=both', default=0)
    parser.add_argument('-n', metavar='INIT', type=int, help='0=random, 1=approximate, 2=both', default=0)
    parser.add_argument('-f', metavar='FILENAME', type=str, help='filename', default='data.tsv')
    parser.add_argument('-e', metavar='EXPONENT', type=int, nargs='+', help='filename', default=3)
    parser.add_argument('--header', metavar='HEADER', type=int, help='header (line number)', default=None)
    parser.add_argument('--rownames', metavar='ROW NAMES', type=int, help='row names (column number)', default=None)
    parser.add_argument('-p', metavar='SEND_PROJECTIONS', type=int, help='one shot methods', default=0)

    args = parser.parse_args()
    basedir = args.d

    output_folder = op.join(basedir, args.o, 'config_files')
    os.makedirs(output_folder, exist_ok=True)

    if args.q == 0:
        qr = ['no_qr']
    elif args.q == 1:
        qr = ['federated_qr']
    else:
        qr = ['no_qr']

    if args.s == 0:
        smpc = [False]
    elif args.s == 1:
        smpc = [True]
    else:
        smpc = [True, False]

    if args.n == 0:
        init = ['random']
    elif args.n == 1:
        init = ['approximate_pca']
    else:
        init = ['random']

    count = 0

    algo = ['randomized']

    if args.p == 1:
        send_projections = [True]
    elif args.p == 2:
        send_projections = [False]
    elif args.p == 3:
        send_projections = [True, False]
    else:
        send_projections = [False]

    print(send_projections)
    count = create_configs_power(output_folder, batch=args.b, train_test=args.t, maxit=args.i, qr=qr, use_smpc=smpc, init=init,
                                 datafile=args.f, exponent=args.e, counter=count, algorithms=algo, colnames = args.header, rownames = args.rownames,
                                 send_projections=send_projections)


