import yaml
import os.path as op
import os
import argparse as ap


def make_default_config_file(datafile = 'data.tsv',
                             send_projections=False,
                             subsample=True,
                             center=True,
                             variance=True,
                             highly_variable=True,
                             log_transform=True,
                             perc_hv=0.1):

    """
    Default config file generator
    qr: one of 'federated_qr'| 'no_qr'
    :return:
    """
    dict = {'fc_pca':
             {'input':
                  {'data': datafile,
                   'delimiter': '\t'},
              'output':
                  {'projections': 'reduced_data.tsv',
                   'left_eigenvectors': 'left_eigenvectors.tsv',
                   'right_eigenvectors': 'right_eigenvectors.tsv',
                   'eigenvalues': 'eigenvalues.tsv',
                   'scaled_data_file': 'scaled_data.tsv'
                   },
              'algorithm':
                  {'pcs': 10
                   },
              'privacy':
                  {'send_projections': send_projections,
                   'subsample_projections': subsample},
              'scaling': {
                  'center': center,
                  'highly_variable': highly_variable,
                  'variance': variance,
                  'perc_highly_var': perc_hv,
                  'log_transform': log_transform,
              'max_nan_fraction': 1}
              }
            }
    return dict

def write_config(config, basedir, counter):
    os.makedirs(op.join(basedir,  str(counter)), exist_ok=True)
    with open(op.join(basedir,  str(counter), 'config.yaml'), 'w') as handle:
        yaml.safe_dump(config, handle, default_flow_style=False, allow_unicode=True)


def create_configs_power(output_folder, datafile='data.tsv', counter=0, send_projections=[True], center=True,
                         variance=True,
                         highly_variable=True,
                         log_transform=True,
                         perc_hv=0.1
                         ):


    for p in send_projections:
        config = make_default_config_file(datafile=datafile,
                                          send_projections=p,
                                          center=center,
                                          variance=variance,
                                          highly_variable=highly_variable,
                                          log_transform=log_transform,
                                          perc_hv=perc_hv
                                          )
        write_config(config=config, basedir=output_folder, counter=counter)
        counter = counter + 1
    return counter



if __name__ == '__main__':
    parser = ap.ArgumentParser(description='Split complete data into test data for federated PCA')
    parser.add_argument('-d', metavar='DIRECTORY', type=str, help='output directory', default='.')
    parser.add_argument('-o', metavar='OUTPUT_DIRECTORY_NAME', type=str, help='output directory', default='.')
    parser.add_argument('-f', metavar='FILENAME', type=str, help='filename', default='data.tsv')
    parser.add_argument('--header', metavar='HEADER', type=int, help='header (line number)', default=None)
    parser.add_argument('--rownames', metavar='ROW NAMES', type=int, help='row names (column number)', default=None)
    parser.add_argument('-p', metavar='SEND_PROJECTIONS', type=int, help='one shot methods', default=0)
    parser.add_argument('--center', metavar='CENTER', type=bool, help='center matrices', default=False)
    parser.add_argument('--variance', metavar='VARIANCE', type=bool, help='scale matrices to unit variance', default=False)
    parser.add_argument('--log_transform', metavar='LOG', type=bool, help='center matrices', default=False)
    parser.add_argument('--phv', metavar='PERCENT_HIGHLY_VARIABLE', type=float, help='center matrices', default=None)
    parser.add_argument('--count', metavar='COUNTER', type=int, help='center matrices', default=None)
    args = parser.parse_args()
    basedir = args.d

    output_folder = op.join(basedir, args.o, 'config_files')
    os.makedirs(output_folder, exist_ok=True)



    if args.count is None:
        count = 0
    else:
        count = args.count


    if args.p == 1:
        send_projections = [True]
    elif args.p == 2:
        send_projections = [False]
    elif args.p == 3:
        send_projections = [True, False]
    else:
        send_projections = [False]

    print(send_projections)
    if args.phv is not None:
        highly=False
    else:
        highly=True


    count = create_configs_power(output_folder,
                                 datafile=args.f, counter=count,
                                 send_projections=send_projections, center=args.center,
                                 variance=args.variance,
                                 highly_variable=highly,
                                 log_transform=args.log_transform,
                                 perc_hv=args.phv
                                 )


